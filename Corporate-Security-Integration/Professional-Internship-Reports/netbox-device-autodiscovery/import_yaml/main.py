import os
from yaml_processor import load_and_process_yaml  # Importation correcte de ton module

def main():
    # Chemin relatif du fichier YAML dans le sous-dossier network_devices
    yaml_path = "network_devices/access-points/ap-rob.yaml"
    print("🚀 Démarrage de l'importation des équipements vers NetBox...")
    load_and_process_yaml(yaml_path)  # Appel de la fonction de traitement
    print("✅ Importation terminée.")

if __name__ == "__main__":
    main()
