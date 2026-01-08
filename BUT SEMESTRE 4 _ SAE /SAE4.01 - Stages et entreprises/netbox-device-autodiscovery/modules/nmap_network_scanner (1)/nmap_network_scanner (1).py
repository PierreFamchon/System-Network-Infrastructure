import re
import json
import xmltodict
import subprocess
from collections import defaultdict
import ipaddress
from itertools import groupby
from typing import List, Optional

from nmap import PortScanner, PortScannerError

from logger import log
from .active_recognition import recognize_by_http, recognize_by_snmp
from shared_objects import nb, Device, netbox_template
from utils import remove_duplicates


def args2str(args: List[str], sep=' ') -> str:
    """Converts list of command line arguments into a string"""
    return sep.join(args)


def integer_ranges(integers: List[int], sep=',') -> str:
    """Compress list of integers into ranges"""
    ranges = []
    for _, i in groupby(enumerate(sorted(integers)), lambda pair: pair[1] - pair[0]):
        t = list(i)
        x, y = t[0][1], t[-1][1]
        ranges.append(str(x) if x == y else f'{x}-{y}')
    return sep.join(ranges)


def filter_networks(networks: List[str], ip_addresses: List[str]) -> List[str]:
    """Exclude given IP addresses from the given IP networks and return list of networks and addresses"""
    ip_addrs = [ipaddress.ip_address(ip) for ip in ip_addresses]
    results = []
    for net in networks:
        network = ipaddress.ip_network(net)
        ips = [ip for ip in network if ip not in ip_addrs]
        if ips == list(network):
            # The network does not intersect with the IP addresses
            results.append(net)
            continue
        # Compress list of the target IP addresses into Nmap compact target specification
        for first_octets, included_ips in groupby(map(str, ips), lambda ip: ip.rsplit('.', maxsplit=1)[0]):
            last_octet_ranges = integer_ranges([int(ip.rsplit('.', maxsplit=1)[1]) for ip in included_ips])
            results.append(f'{first_octets}.{last_octet_ranges}')
    return results

class Module:
    def __init__(self, config: dict):
        self.config = config

    def run(self) -> Optional[dict]:
        """Returns dictionary of NetBox objects to verify, and create or update"""
        # Obtaining IP prefixes to scan, excluding prefixes with "Do not autodiscover" tag
        autodiscovery_disabled_tag = nb.extras.tags.get(slug='do-not-autodiscover')
        target_prefixes = [p.prefix for p in nb.ipam.prefixes.all() if autodiscovery_disabled_tag not in p.tags]

        # Filter out VMWare vCenter IPs
        vcenter_tag = nb.extras.tags.get(name='vCenter')
        vcenter_ips = [ip.address.split('/')[0] for ip in nb.ipam.ip_addresses.all() if vcenter_tag in ip.tags]
        log.debug('vCenter IP addresses to exclude from scan: %s', vcenter_ips)
        target_hosts = filter_networks(target_prefixes, vcenter_ips)

        # Scan networks
        hosts = self.scan_networks(target_hosts)
        if not hosts:
            log.error("A critical error occurred while scanning the network, stopping")
            return

        # NetBox objects to verify, and create or update
        nb_objects = self.process_scan_results(hosts)
        return nb_objects

    def scan_networks(self, target_list: List[str]) -> Optional[dict]:
        try:
            # Initialisation de Nmap
            nmap = PortScanner()
        except Exception as e:
            log.error(f"Erreur d'initialisation de Nmap: {e}")
            return None

        # Préparer les arguments Nmap
        nmap_arguments = '-sS -O'
        if self.config.get('nmap_guess_os'):
            nmap_arguments += ' --osscan-guess'
        nmap_arguments += ' ' + self.config['nmap_additional_args'] 
        log.info('Network scanning started')
        log.debug('Scan targets: %s', target_list)
        log.debug('Nmap arguments: %s', nmap_arguments)

        try:
                # Exécution du scan Nmap
                scan_results = nmap.scan(hosts='192.168.50.0/24', arguments=nmap_arguments)
                log.debug(f"Résultat brut de Nmap : {json.dumps(scan_results, indent=2)}")
                log.info('Nmap scan completed successfully')
                return scan_results['scan']
        except Exception as e:
                log.error(f"Erreur pendant le scan: {e}")
                return None


    def recognize_general_purpose_device(self, os_class, os_name):
        """
        Recognizes a general-purpose device based on the provided OS class and name.

        :param os_class: OS class information from Nmap scan result
        :param os_name: OS name from Nmap scan result
        :return: Device object
        """
        # Your logic to recognize general-purpose devices
        return Device("General", os_name, os_class['osfamily'], os_class.get('osgen'))

    def recognize_device(self, ip_addr: str, open_ports: List[int], os_matches: List[dict]):
        """
        Recognizes device model, operating system, based on the result of scanning the host.

        :param ip_addr: IP address of the host
        :param open_ports: List of open TCP ports
        :param os_matches: Nmap OS detection results
        """
        if not os_matches:
            log.warning(f"No OS matches found for {ip_addr}")
            return Device("Unknown", "Unknown", "Unknown", "Unknown")

        os_match = os_matches[0]
        os_name = os_match['name']
        if int(os_match['accuracy']) < 85:
            log.info(f"OS match accuracy too low {os_match['accuracy']}, OS fingerprint rejected for {ip_addr}")
            return Device("Unknown", "Unknown", "Unknown", "Unknown")

        for os_class in os_match['osclass']:
            os_class_type = os_class['type']

            if os_class_type == 'general purpose':
                return self.recognize_general_purpose_device(os_class, os_name)  # Utilisation de 'self' ici
            # Ajouter d'autres types comme "switch", "router", "printer", etc. selon le besoin.

        return Device("Unknown", "Unknown", "Unknown", "Unknown")


    def active_device_recognition(self, ip_addr: str, open_ports: List[int]) -> Optional[Device]:
        """
        Recognizes device model based on active interaction with it using available protocols.

        :param ip_addr: IP addresses of the host
        :param open_ports: List of open TCP ports
        """
        if 80 in open_ports:
            if device := recognize_by_http(ip_addr, 80):
                return device
        if self.config['snmp_recognition_enabled']:
            for snmp_community in self.config['shared_snmp_communities']:
                if device := recognize_by_snmp(ip_addr, 161, snmp_community, retries=self.config['snmp_recognition_retries']):
                    return device

    def process_scan_results(self, nmap_results: dict) -> dict:
        """Converts the results of an Nmap network scan to NetBox entities"""
        log.info('Converting Nmap scan results to NetBox objects…')
        nb_objects = defaultdict(list)
        for ip, scan_results in nmap_results.items():
            log.info(f'Recognition of the device with IP {ip} is started…')
            open_ports = [port for port, qualities in scan_results['tcp'].items() if
                          qualities['state'] == 'open'] if 'tcp' in scan_results else []
            recognized_device = None
            if scan_results['osmatch']:
                # Try to use Nmap TCP/IP OS fingerprint recognition
                recognized_device = self.recognize_device(ip, open_ports, scan_results['osmatch'])
            if not recognized_device:
                # Try to use active recognition
                recognized_device = self.active_device_recognition(ip, open_ports)
            if not recognized_device:
                # Generic cases
                if 515 in open_ports:
                    recognized_device = Device('Generic', 'printer', 'Printer', None)

            if not recognized_device:
                log.info('Failed to recognize the device, skipped')
                continue

            nb_objects['manufacturers'].append(netbox_template.manufacturer(recognized_device.manufacturer))
            nb_objects['device_types'].append(
                netbox_template.device_type(recognized_device.manufacturer, recognized_device.model)
            )
            if recognized_device.platform:
                nb_objects['platforms'].append(netbox_template.platform(recognized_device.platform))

            # Use IP address as the device name
            device_name = ip
            nb_objects['devices'].append(
                netbox_template.device(
                    name=device_name, device_role=recognized_device.role, manufacturer=recognized_device.manufacturer,
                    model=recognized_device.model, platform=recognized_device.platform
                ))
            nb_objects['interfaces'].append(netbox_template.device_interface(device=device_name, name='vNIC0'))
            dns_name = scan_results['hostnames'][0]['name'] if scan_results['hostnames'][0] else None
            nb_objects['ip_addresses'].append(
                netbox_template.ip_address(ip + '/32', device=device_name, interface='vNIC0')
            )
            log.info(
                'Device recognized: {}'.format(
                    ', '.join('='.join((k, str(v))) for k, v in recognized_device._asdict().items())
                )
            )
        return {k: remove_duplicates(v) for k, v in nb_objects.items()}
