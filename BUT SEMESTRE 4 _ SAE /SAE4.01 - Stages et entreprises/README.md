<div align="center">

# 📡 Network Discovery & Inventory Automation
## SOURCE OF TRUTH (SoT)

<p align="center">
  <img src="https://img.shields.io/badge/NetBox-v4.0+-blue?style=for-the-badge&logo=netbox&logoColor=white" alt="NetBox"/>
  <img src="https://img.shields.io/badge/NetDisco-v2-green?style=for-the-badge&logo=network&logoColor=white" alt="NetDisco"/>
  <img src="https://img.shields.io/badge/Python-3.x-yellow?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/Database-PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
</p>

[Description](#-description) •
[Matériel & Stack Technique](#-matériel--stack-technique) •
[Structure du Projet](#-structure-du-projet) • 
[Installation & Utilisation](#installation) •
[Phases du Projet](#-phases-du-projet) •
[Bilan](#-bilan) •
[Auteurs](#-auteurs)

</div>

---

## 📝 Description

Ce projet a été réalisé dans le cadre d'un stage à la **Direction des Systèmes d'Information (DSI)** de l'UTC.

Suite à une refonte de l'infrastructure, l'objectif était de créer une **Source de Vérité (SoT)** centralisée et fiable. Le projet couple la puissance de découverte automatique de **NetDisco** (via SNMP/LLDP) avec la gestion rigoureuse de **NetBox** (IPAM/DCIM). Des scripts Python assurent la synchronisation entre les deux entités pour garantir un inventaire toujours à jour sans intervention humaine.

---

## 💻 Matériel & Stack Technique

La solution repose sur une architecture conteneurisée pour assurer portabilité et isolation.

### Infrastructure & Virtualisation

![Linux](https://img.shields.io/badge/OS-UBUNTU-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Docker](https://img.shields.io/badge/CONTAINER-DOCKER-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Compose](https://img.shields.io/badge/ORCHESTRATION-DOCKER%20COMPOSE-2496ED?style=for-the-badge&labelColor=404040&logo=docker&logoColor=white)

### Applications Core

![NetBox](https://img.shields.io/badge/IPAM%20%2F%20DCIM-NETBOX-00ADD8?style=for-the-badge&logo=netbox&logoColor=white)
![NetDisco](https://img.shields.io/badge/SCANNER-NETDISCO-7cb342?style=for-the-badge&labelColor=404040)
![Protocols](https://img.shields.io/badge/PROTOCOL-SNMP%20%2F%20LLDP-404040?style=for-the-badge)

### Automatisation & Scripts

![Python](https://img.shields.io/badge/LANGUAGE-PYTHON%203.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/LIB-REQUESTS-3776AB?style=for-the-badge&labelColor=404040)
![PyYAML](https://img.shields.io/badge/LIB-PYYAML-3776AB?style=for-the-badge&labelColor=404040)
![Icecream](https://img.shields.io/badge/LIB-ICECREAM-3776AB?style=for-the-badge&labelColor=404040)

---

## 📂 Structure du Projet

L'architecture des scripts est organisée pour séparer les données sources de la logique de traitement.

```text
📁 netbox-device-autodiscovery/
├── 📁 network_devices/       # Dossier contenant les sources de données
│   ├── 📁 access-points/     # Fichiers YAML/CSV pour les APs
│   └── 📁 switches/          # Fichiers YAML/CSV pour les Switchs
├── 📁 import_yaml/           # Cœur de l'automatisation Python
│   ├── 📄 main.py            # Point d'entrée du programme
│   ├── 📄 device_manager.py  # Logique de création (Devices, Interfaces, IPs)
│   ├── 📄 netbox_api.py      # Wrapper pour les appels API REST (GET/POST/PATCH)
│   ├── 📄 netbox_config.py   # Fichier de configuration (URL, Token, Headers)
│   └── 📄 yaml_processor.py  # Traitement et parsing des fichiers sources
```
---

## ⚙️ <a name="installation"></a>Installation & Utilisation

### Déploiement Docker

* **A. NetBox (IPAM/DCIM)**

```bash
git clone [https://github.com/netbox-community/netbox-docker.git](https://github.com/netbox-community/netbox-docker.git)
cd netbox-docker

# Exposition du port web (Override)
echo 'services:
  netbox:
    ports:
      - "8000:8080"' > docker-compose.override.yml

# Démarrage et création SuperUser
sudo docker compose pull && sudo docker compose up -d
sudo docker exec -it netbox-docker-netbox-1 python3 /opt/netbox/netbox/manage.py createsuperuser
```

* **B. NetDisco (Discovery)**

```bash
git clone [https://github.com/netdisco/netdisco.git](https://github.com/netdisco/netdisco.git)
cd netdisco

# Permissions pour logs et configs
mkdir logs config nd-site-local
chmod 777 logs config nd-site-local

# Configuration SNMP : éditer config/deployment.yml pour ajouter vos communautés
# Lancement
sudo docker compose up -d
```

### Configuration des Scripts
Editez le fichier netbox-device-autodiscovery/import_yaml/netbox_config.py avec vos accès :

```bash
# netbox_config.py
NETBOX_URL = "[http://192.168.100.160:8000/api/](http://192.168.100.160:8000/api/)"
NETBOX_TOKEN = "votre_token_api_genere_dans_netbox" # ex: 04946ef59...
HEADERS = {
    "Authorization": f"Token {NETBOX_TOKEN}",
    "Content-Type": "application/json",
}
DEBUG_MODE = True
```
### Utilisation / Exécution

* **Étape A :**
  Préparation des données (Export NetDisco) Si vous n'utilisez pas de fichiers YAML manuels, exportez les données découvertes par NetDisco en CSV directement depuis la base de données :

```bash
sudo docker exec -it netdisco-postgresql psql -U netdisco netdisco -c "\copy (SELECT d.name, d.model, d.serial FROM device d) TO '/tmp/devices.csv' WITH (FORMAT CSV, HEADER);"
```

* **Étape B :**
  Lancement de l'automatisation Lancez le script principal pour parser les données et peupler NetBox :

```bash
cd netbox-device-autodiscovery/import_yaml
python3 main.py
```
* (Note : Le script vérifie l'existence du device (Idempotence), crée le modèle s'il est inconnu, configure les interfaces et assigne les IPs de management.)

---

## 🚀 Phases du Projet

* Architecture : Mise en place de l'écosystème Docker et communication inter-conteneurs.
* Découverte : Configuration de NetDisco (SNMP/LLDP) pour remonter automatiquement l'inventaire brut.
* Automatisation : Développement des scripts Python pour transformer les données brutes en objets structurés NetBox (Patch vs Post).

---

## 📊 Bilan

La mise en place de cette Source of Truth (SoT) a permis :

* ✅ Centralisation : Un inventaire unique et fiable pour toute la DSI.
* ✅ Automatisation : Fin de la double saisie et réduction drastique des erreurs humaines.
* ✅ Visibilité : Découverte proactive des nouveaux équipements connectés au réseau.

---

## 👥 Auteurs

* Pierre Famchon
  * Étudiant BUT R&T (IUT Béthune)
  * Stagiaire DSI - Université de Technologie de Compiègne
