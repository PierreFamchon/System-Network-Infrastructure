import requests
from netbox_config import DEBUG_MODE
from icecream import ic

if not DEBUG_MODE:
    ic.disable()

from netbox_config import NETBOX_URL, HEADERS
from utils import format_slug

# Fonction pour récupérer l'ID d'une interface par son nom
def get_interface_id_by_name(device_id, interface_name):
    """
    Récupère l'ID de l'interface par son nom pour un périphérique donné.
    """
    response = requests.get(f"{NETBOX_URL}dcim/interfaces/?device_id={device_id}&name={interface_name}", headers=HEADERS)
    if response.status_code == 200 and response.json()["count"] > 0:
        return response.json()["results"][0]["id"]
    return None
    
def device_exists(device_name):
    response = requests.get(f"{NETBOX_URL}dcim/devices/?name={device_name}", headers=HEADERS)
    if response.status_code == 200 and response.json()["count"] > 0:
        return response.json()["results"][0]
    return None

def create_or_update_device(payload, existing_device=None):
    if existing_device:
        device_id = existing_device["id"]
        response = requests.patch(f"{NETBOX_URL}dcim/devices/{device_id}/", headers=HEADERS, json=payload)
        if response.status_code in (200, 204):
            print(f"✅ Équipement mis à jour : {payload['name']}")
            return device_id
        else:
            print(f"❌ Échec mise à jour {payload['name']} : {response.status_code}")
            return None
    else:
        response = requests.post(f"{NETBOX_URL}dcim/devices/", headers=HEADERS, json=payload)
        if response.status_code == 201:
            print(f"✅ Équipement créé : {payload['name']}")
            return response.json()["id"]
        else:
            print(f"❌ Échec création {payload['name']} : {response.status_code}")
            return None

def get_device_type_id(device_type_name):
    if not device_type_name:
        return None
    slug = format_slug(device_type_name)
    response = requests.get(f"{NETBOX_URL}dcim/device-types/?slug={slug}", headers=HEADERS)
    if response.status_code == 200 and response.json()["count"] > 0:
        return response.json()["results"][0]["id"]

def get_site_id(site_name):
    if not site_name:
        return None
    response = requests.get(f"{NETBOX_URL}dcim/sites/?name={site_name}", headers=HEADERS)
    if response.status_code == 200 and response.json()["count"] > 0:
        return response.json()["results"][0]["id"]

def get_interface_id_by_name(device_id, interface_name):
    response = requests.get(f"{NETBOX_URL}dcim/interfaces/?device_id={device_id}&name={interface_name}", headers=HEADERS)
    if response.status_code == 200 and response.json()["count"] > 0:
        return response.json()["results"][0]["id"]

def create_interfaces(device_id, port_list, mgmt_only):
    interface_ids = {}

    for port_name in port_list:
        # Vérifie si l'interface existe déjà
        response = requests.get(
            f"{NETBOX_URL}dcim/interfaces/",
            headers=HEADERS,
            params={"device_id": device_id, "name": port_name}
        )
        results = response.json().get("results", [])
        if results:
            interface_id = results[0]["id"]
            ic(f"🔁 Interface existante récupérée : {port_name} -> {interface_id}")
        else:
            # Crée l'interface
            payload = {
                "device": device_id,
                "name": port_name,
                "type": "1000base-t",  # ou autre si nécessaire
                "mgmt_only": mgmt_only or False,
            }
            response = requests.post(f"{NETBOX_URL}dcim/interfaces/", headers=HEADERS, json=payload)
            response.raise_for_status()
            interface_id = response.json()["id"]
            ic(f"🆕 Interface créée : {port_name} -> {interface_id}")

        interface_ids[port_name] = interface_id

    return interface_ids

def assign_mac_to_interface(interface_id, mac_address):
    import requests

    url = f"{NETBOX_URL}/dcim/mac-addresses/"

    # Vérifier si la MAC existe déjà
    existing = requests.get(url, headers=HEADERS, params={"mac_address": mac_address}).json()

    if existing["count"] > 0:
        # Si elle existe, mettre à jour avec l'interface si non assignée
        mac_entry = existing["results"][0]
        if mac_entry.get("interface") is None:
            update_url = f"{url}{mac_entry['id']}/"
            response = requests.patch(update_url, headers=HEADERS, json={"interface": interface_id})
            if response.status_code in [200, 204]:
                print(f"✅ MAC {mac_address} assignée à l'interface {interface_id}")
            else:
                print(f"❌ Erreur lors de l'assignation de la MAC à l'interface : {response.text}")
        else:
            print(f"⚠️ Adresse MAC {mac_address} déjà associée à une interface.")
    else:
        # Créer la MAC avec l'interface directement
        payload = {
            "mac_address": mac_address,
            "interface": interface_id,
        }
        response = requests.post(url, headers=HEADERS, json=payload)
        if response.status_code in [200, 201]:
            print(f"✅ MAC {mac_address} créée et assignée à l'interface {interface_id}")
        else:
            print(f"❌ Erreur lors de la création de la MAC : {response.text}")


def format_mac_address(mac_address):
    mac = mac_address.replace(".", "").replace("-", "").replace(":", "").strip().upper()
    if len(mac) != 12:
        print(f"❌ Adresse MAC invalide : {mac_address}")
        return None
    return ":".join([mac[i:i+2] for i in range(0, 12, 2)])

def assign_ip_to_device(device_id, ip_address):
    response = requests.get(f"{NETBOX_URL}ipam/ip-addresses/?address={ip_address}", headers=HEADERS)
    if response.status_code == 200 and response.json()["count"] > 0:
        ip_id = response.json()["results"][0]["id"]
    else:
        payload = {"address": ip_address}
        response = requests.post(f"{NETBOX_URL}ipam/ip-addresses/", headers=HEADERS, json=payload)
        if response.status_code == 201:
            ip_id = response.json()["id"]
        else:
            print(f"❌ Erreur ajout IP {ip_address}: {response.status_code}")
            return None

    interface_response = requests.get(f"{NETBOX_URL}dcim/interfaces/?device_id={device_id}", headers=HEADERS)
    if interface_response.status_code == 200 and interface_response.json()["count"] > 0:
        interface_id = interface_response.json()["results"][0]["id"]
    else:
        print(f"❌ Pas d’interface trouvée pour device {device_id}")
        return None

    payload = {"assigned_object_type": "dcim.interface", "assigned_object_id": interface_id}
    assign_response = requests.patch(f"{NETBOX_URL}ipam/ip-addresses/{ip_id}/", headers=HEADERS, json=payload)

    if assign_response.status_code in (200, 204):
        print(f"✅ Adresse IP {ip_address} assignée à l’interface {interface_id}")
        return interface_id
    else:
        print(f"❌ Erreur assignation IP {ip_address}: {assign_response.status_code}")
        return None

