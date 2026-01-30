import requests
import yaml
import json

# Configurer l'URL de l'API NetBox et le token d'accès
NETBOX_URL = "http://192.168.100.160:8000/api/"
NETBOX_TOKEN = "04946ef59ffeb57bc7a0e7c6ac73f787eb272c57"

# En-têtes de l'API (ajoute ton token d'authentification ici)
HEADERS = {
    "Authorization": f"Token {NETBOX_TOKEN}",
    "Content-Type": "application/json",
}

# Fonction pour récupérer l'ID du type de périphérique
def get_device_type_id(device_type_name):
    response = requests.get(f"{NETBOX_URL}dcim/device-types/?model={device_type_name}", headers=HEADERS)
    
    if response.status_code == 200:
        device_types = response.json()['results']
        if device_types:
            return device_types[0]['id']
    print(f"Erreur lors de la récupération de l'ID du type de périphérique {device_type_name}")
    return None

# Fonction pour vérifier si un périphérique existe déjà
def device_exists(device_name):
    response = requests.get(f"{NETBOX_URL}dcim/devices/?name={device_name}", headers=HEADERS)
    
    if response.status_code == 200:
        devices = response.json()['results']
        if devices:
            return devices[0]  # L'équipement existe, on retourne l'objet
    return None

# Fonction pour obtenir l'ID du rôle d'équipement
def get_device_role(device_name):
    if device_name.startswith("sw"):
        return "switch"  # Si l'équipement commence par 'sw', c'est un switch
    return "other"  # Sinon, rôle générique

# Fonction pour créer ou mettre à jour un périphérique dans NetBox
def create_or_update_device(device_data):
    device_name = device_data.get("name")
    device_ip = device_data.get("ip_address")
    device_type_name = device_data.get("type")
    device_description = device_data.get("description")
    device_ports = device_data.get("ports")

    # Récupérer l'ID du type de périphérique
    device_type_id = get_device_type_id(device_type_name)
    if not device_type_id:
        print(f"Le type de périphérique {device_type_name} n'a pas pu être trouvé.")
        return

    # Assigner tous les équipements au site avec l'ID 1
    site_id = 1  # Site par défaut (ID = 1)

    # Récupérer le rôle de l'équipement en fonction du nom
    device_role = get_device_role(device_name)

    # Vérifier si l'équipement existe déjà
    existing_device = device_exists(device_name)

    device_payload = {
        "name": device_name,
        "device_type": device_type_id,
        "device_role": device_role,  # Assigner le rôle
        "site": site_id,  # Site ID 1
        "description": device_description,
    }

    if existing_device:
        # Mettre à jour l'équipement existant
        device_id = existing_device["id"]
        response = requests.patch(f"{NETBOX_URL}dcim/devices/{device_id}/", headers=HEADERS, data=json.dumps(device_payload))
        if response.status_code == 200:
            print(f"Équipement mis à jour : {device_name}")
        else:
            print(f"Erreur de mise à jour pour l'équipement {device_name}: {response.status_code}")
    else:
        # Créer un nouvel équipement
        response = requests.post(f"{NETBOX_URL}dcim/devices/", headers=HEADERS, data=json.dumps(device_payload))
        if response.status_code == 201:
            print(f"Équipement créé : {device_name}")
            device_id = response.json()['id']
        else:
            print(f"Erreur de création pour l'équipement {device_name}: {response.status_code}")

    # Créer les interfaces pour cet équipement
    if device_ports:
        # Si la plage de ports est spécifiée sous la forme Fa0/1-12, créer chaque interface individuellement
        port_range = device_ports.split('-')
        if len(port_range) == 2:
            # Extraire le numéro de port sans la partie Fa0/
            start_port = int(port_range[0].strip()[3:])  # Récupérer le premier numéro de port après 'Fa0/'
            end_port = int(port_range[1].strip()[3:])  # Récupérer le dernier numéro de port après 'Fa0/'
            for port_num in range(start_port, end_port + 1):
                interface_name = f"Fa0/{port_num}"  # Créer le nom de l'interface
                create_interface(device_id, interface_name)
        else:
            # Si un seul port est spécifié (par exemple, Fa0/1), on le crée directement
            create_interface(device_id, device_ports)

    # Assigner l'adresse IP à l'équipement (à l'interface principale)
    if device_ip:
        # Vérifie si l'équipement possède des interfaces
        interfaces = get_device_interfaces(device_id)
        if interfaces:
            # Utilise la première interface (ou tu pourrais choisir une autre logique pour le port spécifique)
            interface_id = interfaces[0]['id']
            ip_payload = {
                "address": device_ip,
                "interface": interface_id,
                "dns_name": device_name,
                "assigned_object_type": "dcim.device",
                "assigned_object_id": device_id,
                "is_primary": True,
            }
            response = requests.post(f"{NETBOX_URL}ipam/ip-addresses/", headers=HEADERS, data=json.dumps(ip_payload))
            if response.status_code == 201:
                print(f"Adresse IP {device_ip} assignée à l'équipement {device_name}")
            else:
                print(f"Erreur lors de l'assignation de l'IP à {device_name}: {response.status_code}")
        else:
            print(f"Aucune interface trouvée pour l'équipement {device_name} pour assigner l'IP.")

# Fonction pour créer l'interface dans NetBox
def create_interface(device_id, interface_name):
    interface_payload = {
        "name": interface_name,
        "device": device_id,
        "type": "physical",  # Type d'interface, tu peux ajuster si nécessaire
    }
    response = requests.post(f"{NETBOX_URL}dcim/interfaces/", headers=HEADERS, data=json.dumps(interface_payload))
    if response.status_code == 201:
        print(f"Interface {interface_name} créée avec succès")
    else:
        print(f"Erreur lors de la création de l'interface {interface_name}: {response.status_code}")

# Fonction pour obtenir les interfaces d'un périphérique
def get_device_interfaces(device_id):
    response = requests.get(f"{NETBOX_URL}dcim/interfaces/?device_id={device_id}", headers=HEADERS)
    if response.status_code == 200:
        return response.json()['results']
    return []

# Fonction pour charger et traiter les fichiers YAML
def load_and_process_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    for switch_name, switch_data in data['switches'].items():
        print(f"Traitement du switch: {switch_name}")
        switch_data['name'] = switch_name  # Ajouter le nom de l'équipement
        create_or_update_device(switch_data)

# Appel de la fonction pour traiter un fichier YAML
load_and_process_yaml('network_devices/switches/sw-cr.yaml')
