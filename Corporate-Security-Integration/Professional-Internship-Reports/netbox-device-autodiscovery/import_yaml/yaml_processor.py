import yaml
from netbox_config import DEBUG_MODE
from icecream import ic

if not DEBUG_MODE:
    ic.disable()

from netbox_api import (
    get_device_type_id,
    get_device_role,
    device_exists,
    create_or_update_device,
    get_site_id,
)
from device_manager import create_interfaces, assign_ip_to_device, assign_mac_to_interface
from utils import format_mac

def load_and_process_yaml(file_path):
    ic(file_path)
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    for device_name, device_info in data.items():
        ic(device_name, device_info)

        device_type_name = device_info.get("type")
        ip_address = device_info.get("ip_address")
        mac_address = device_info.get("mac_address")
        role_name = device_info.get("role")
        raw_ports = device_info.get("ports")

        if mac_address:
            mac_address = format_mac(mac_address)

        device_type_id = get_device_type_id(device_type_name)

        device_role_id = None
        if role_name:
            device_role_id = get_device_role(role_name)

        existing_device = device_exists(device_name)

        device_payload = {
            "name": device_name,
            "device_type": device_type_id,
            "site": get_site_id("Roberval"),
        }


        if device_role_id:
            device_payload["device_role"] = device_role_id

        if "description" in device_info:
            device_payload["description"] = device_info["description"]

        device_id = create_or_update_device(device_payload, existing_device)

        port_list = []
        if raw_ports:
            for part in raw_ports.split(","):
                part = part.strip()
                if "-" in part:
                    base = part[:part.index("/") + 1]
                    range_part = part.split("/")[1]
                    start, end = map(int, range_part.split("-"))
                    for i in range(start, end + 1):
                        port_list.append(f"{base}{i}")
                else:
                    port_list.append(part)

        # Crée les interfaces ET récupère les IDs
        interface_map = {}
        if port_list:
            interface_map = create_interfaces(device_id, port_list, None)

        # Assigne l'IP
        if ip_address:
            interface_id = assign_ip_to_device(device_id, ip_address)

            # Utilise l'interface IP aussi pour la MAC (optionnel)
            if interface_id and mac_address:
                assign_mac_to_interface(interface_id, mac_address)

        # Sinon, assigne la MAC à G0/1 par défaut si dispo
        elif mac_address and "G0/1" in interface_map:
            assign_mac_to_interface(interface_map["G0/1"], mac_address)


