import requests
import json
from netbox_config import DEBUG_MODE
from icecream import ic

if not DEBUG_MODE:
    ic.disable()
    
from netbox_config import NETBOX_URL, HEADERS



# Fonction pour récupérer l'ID d'un type de périphérique par son nom (ex: "cisco-switch")
def get_device_type_id(device_type_name):
    response = requests.get(
        f"{NETBOX_URL}dcim/device-types/?model={device_type_name}",
        headers=HEADERS
    )
    if response.status_code == 200:
        device_types = response.json()['results']
        ic(device_types)
        if device_types:
            return device_types[0]['id']
    print(f"❌ Erreur: type de périphérique introuvable : {device_type_name}")
    return None

# Vérifie si un périphérique existe déjà par son nom
def device_exists(device_name):
    response = requests.get(
        f"{NETBOX_URL}dcim/devices/?name={device_name}",
        headers=HEADERS
    )
    if response.status_code == 200:
        devices = response.json()['results']
        if devices:
            return devices[0]
    return None

# Récupère l'ID du rôle "Switch"
def get_device_role():
    role_name = "Wi-Fi AP"
    response = requests.get(
        f"{NETBOX_URL}dcim/device-roles/?name={role_name}",
        headers=HEADERS
    )
    if response.status_code == 200:
        roles = response.json()['results']
        if roles:
            return roles[0]['id']
    print(f"❌ Erreur: rôle '{role_name}' introuvable dans NetBox.")
    return None

# Récupère l'ID du site à partir de son nom (description dans YAML)
def get_site_id(site_name):
    if not site_name:
        return None
    response = requests.get(
        f"{NETBOX_URL}dcim/sites/?name={site_name}",
        headers=HEADERS
    )
    if response.status_code == 200 and response.json()["count"] > 0:
        return response.json()["results"][0]["id"]
    else:
        print(f"🏷️ Site '{site_name}' non trouvé dans NetBox.")
        return None

# Crée ou met à jour un périphérique avec le rôle bon role
def create_or_update_device(device_payload, existing_device=None):
    device_role_id = get_device_role()
    if not device_role_id:
        print("❌ Rôle 'VPN' introuvable, arrêt.")
        return None

    # ✅ On ajoute bien le rôle ici, AVANT de sortir de la fonction
    device_payload['role'] = device_role_id

    if existing_device:
        device_id = existing_device["id"]
        response = requests.patch(
            f"{NETBOX_URL}dcim/devices/{device_id}/",
            headers=HEADERS,
            data=json.dumps(device_payload)
        )
        if response.status_code == 200:
            print(f"✅ Équipement mis à jour : {device_payload['name']}")
            return device_id
        else:
            print(f"❌ Erreur MAJ {device_payload['name']}: {response.status_code} - {response.text}")
            return None
    else:
        response = requests.post(
            f"{NETBOX_URL}dcim/devices/",
            headers=HEADERS,
            data=json.dumps(device_payload)
        )
        if response.status_code == 201:
            print(f"✅ Équipement créé : {device_payload['name']}")
            return response.json()['id']
        else:
            print(f"❌ Erreur création {device_payload['name']}: {response.status_code} - {response.text}")
            return None


# Récupère l'ID d'un rôle de périphérique par son nom (générique)
def get_device_role_id(role_name):
    response = requests.get(
        f"{NETBOX_URL}dcim/device-roles/?name={role_name}",
        headers=HEADERS
    )
    if response.status_code == 200:
        roles = response.json().get("results", [])
        if roles:
            return roles[0]["id"]
    print(f"❌ Rôle '{role_name}' introuvable dans NetBox.")
    return None
