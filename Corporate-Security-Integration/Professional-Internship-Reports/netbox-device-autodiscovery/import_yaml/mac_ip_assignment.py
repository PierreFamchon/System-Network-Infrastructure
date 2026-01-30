import yaml
import requests
import re

NETBOX_URL = "http://192.168.100.160:8000/api/"
NETBOX_TOKEN = "04946ef59ffeb57bc7a0e7c6ac73f787eb272c57"

HEADERS = {
    "Authorization": f"Token {NETBOX_TOKEN}",
    "Content-Type": "application/json",
}

# Fonction pour valider le format de l'adresse MAC
def is_valid_mac(mac_address):
    """
    Vérifie que l'adresse MAC est bien au format XX:XX:XX:XX:XX:XX
    """
    return bool(re.fullmatch(r"([0-9A-F]{2}:){5}[0-9A-F]{2}", mac_address))

# Fonction pour créer une adresse MAC dans NetBox
def create_mac_address(mac_address):
    if not mac_address:
        print(f"❌ Adresse MAC invalide : {mac_address}")
        return None

    if not is_valid_mac(mac_address):
        print(f"❌ Format incorrect pour l'adresse MAC : {mac_address}")
        return None

    payload = {
        "mac_address": mac_address,
        "status": "active"
    }

    print(f"🔁 Création de l'adresse MAC {mac_address}...")
    response = requests.post(f"{NETBOX_URL}dcim/mac-addresses/", headers=HEADERS, json=payload)

    if response.status_code == 201:
        mac_data = response.json()
        print(f"✅ Adresse MAC {mac_address} ajoutée avec l'ID {mac_data['id']}.")
        return mac_data['id']
    else:
        print(f"❌ Erreur lors de la création de la MAC {mac_address}: {response.status_code}")
        print("Réponse complète:", response.text)
        return None

# Chargement du fichier YAML
def load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"❌ Le fichier {file_path} n'a pas été trouvé.")
        return {}
    except yaml.YAMLError as e:
        print(f"❌ Erreur lors du chargement du fichier YAML : {e}")
        return {}

# Traitement des équipements
def process_equipements(equipements):
    if not equipements:
        print("❌ Aucun équipement trouvé dans le fichier YAML.")
        return

    for nom, equipement in equipements.items():
        print(f"\n🛠️ Traitement de l'équipement: {nom}")

        mac_address = equipement.get('mac_address')
        ip_address = equipement.get('ip_address')

        if mac_address:
            print(f"🔧 Interface - MAC : {mac_address} - IP : {ip_address}")
            create_mac_address(mac_address)
        else:
            print(f"❌ Aucune adresse MAC trouvée pour l'équipement {nom}")

# Point d’entrée du script
if __name__ == "__main__":
    equipements = load_yaml('./ap-si.yaml')
    process_equipements(equipements)

