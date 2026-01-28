# 📡 Network Discovery & Inventory Automation (SoT)

[![NetBox](https://img.shields.io/badge/NetBox-v4.0+-blue.svg)](https://github.com/netbox-community/netbox)
[![NetDisco](https://img.shields.io/badge/NetDisco-v2-green.svg)](https://github.com/netdisco/netdisco)
[![Python](https://img.shields.io/badge/Python-3.x-yellow.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)

Ce projet a été réalisé dans le cadre d'un stage à la **Direction des Systèmes d'Information (DSI) de l'Université de Technologie de Compiègne (UTC)**. 

L'objectif principal est de fournir une "Source de Vérité" (SoT) fiable pour l'infrastructure réseau en couplant la découverte automatique de **NetDisco** avec la gestion rigoureuse de **NetBox** via des scripts d'automatisation Python.

---

## 📋 Table des Matières
- [Contexte et Objectifs](#-contexte-et-objectifs)
- [Architecture de la Solution](#-architecture-de-la-solution)
- [Prérequis](#-prérequis)
- [Installation et Déploiement](#-installation-et-déploiement)
  - [1. NetBox (IPAM/DCIM)](#1-netbox-ipamdcim)
  - [2. NetDisco (Discovery)](#2-netdisco-discovery)
- [Scripts d'Automatisation](#-scripts-dautomatisation)
  - [Structure du projet](#structure-du-projet)
  - [Configuration](#configuration)
- [Utilisation](#-utilisation)
- [Auteur](#-auteur)

---

## 🎯 Contexte et Objectifs

Suite à une refonte de l'infrastructure réseau, il était nécessaire de disposer d'un inventaire précis et centralisé des équipements (Switchs, Routeurs, APs) et des ressources virtuelles (IPs, VLANs).

**Fonctionnalités clés :**
* **Découverte automatique** des équipements via SNMP (v2c/v3) et LLDP.
* **Inventaire centralisé** (IPAM & DCIM) dans NetBox.
* **Synchronisation automatisée** : Script Python qui peuple NetBox à partir des données découvertes (ou fichiers YAML/CSV).
* **Gestion des doublons** : Vérification de l'existence des devices avant création/mise à jour (Idempotence).

---

## 🏗 Architecture de la Solution

La solution repose sur des conteneurs Docker pour assurer la portabilité et l'isolation.

1.  **NetDisco** scanne le réseau et stocke les données dans PostgreSQL.
2.  **Extraction** des données (CSV) ou définition manuelle (YAML).
3.  **Scripts Python** traitent les données et interagissent avec l'API REST de NetBox.
4.  **NetBox** sert d'interface de gestion finale.

---

## ⚙ Prérequis

* OS : Linux (Ubuntu recommandé)
* Docker & Docker Compose (v2)
* Python 3.x avec les librairies : `requests`, `pyyaml`, `icecream`

---

## 🚀 Installation et Déploiement

### 1. NetBox (IPAM/DCIM)

Installation via `netbox-docker` :

```bash
# Cloner le dépôt officiel
git clone [https://github.com/netbox-community/netbox-docker.git](https://github.com/netbox-community/netbox-docker.git)
cd netbox-docker

# Créer un override pour exposer le port web (8000)
echo 'services:
  netbox:
    ports:
      - "8000:8080"' > docker-compose.override.yml

# Lancer les conteneurs
sudo docker compose pull
sudo docker compose up -d

# Créer un super-utilisateur
sudo docker exec -it netbox-docker-netbox-1 python3 /opt/netbox/netbox/manage.py createsuperuser
```

---

### 2. NetDisco (Discovery)

Installation pour la découverte SNMP :

```bash
git clone [https://github.com/netdisco/netdisco.git](https://github.com/netdisco/netdisco.git)
cd netdisco

# Permissions nécessaires pour les logs et configs
mkdir logs config nd-site-local
chmod 777 logs config nd-site-local

# Configuration SNMP (exemple partiel de deployment.yml)
# Editer config/deployment.yml pour ajouter vos communautés SNMP / Users v3

# Lancement :
sudo docker compose up -d
```
---

## 🐍 Scripts d'Automatisation

Les scripts permettent d'importer massivement les données dans NetBox via l'API.

### Structure du projet : 

```text
netbox-device-autodiscovery/
├── network_devices/       # Dossier contenant les fichiers YAML/CSV sources [cite: 323-326]
│   ├── access-points/
│   ├── switches/
├── import_yaml/           # Scripts Python [cite: 357]
│   ├── main.py            # Point d'entrée
│   ├── device_manager.py  # Logique de création (Devices, Interfaces, IPs)
│   ├── netbox_api.py      # Fonctions utilitaires API (GET IDs)
│   ├── netbox_config.py   # Configuration (URL, Token)
│   └── yaml_processor.py  # Traitement des fichiers sources
```

### Configuration

Editez le fichier netbox_config.py avec vos accès :

```text
# netbox_config.py
NETBOX_URL = "[http://192.168.100.160:8000/api/](http://192.168.100.160:8000/api/)"
NETBOX_TOKEN = "votre_token_api_genere_dans_netbox" # ex: 04946ef59...
HEADERS = {
    "Authorization": f"Token {NETBOX_TOKEN}",
    "Content-Type": "application/json",
}
DEBUG_MODE = True
```
---

## 💻 Utilisation

### Étape 1 : Préparation des données

Vous pouvez soit utiliser des fichiers YAML structurés, soit exporter les données de NetDisco en CSV via une commande SQL dans le conteneur Postgres .

Exemple d'export CSV depuis NetDisco:

```bash
sudo docker exec -it netdisco-postgresql psql -U netdisco netdisco -c "\copy (SELECT d.name, d.model, d.serial FROM device d) TO '/tmp/devices.csv' WITH (FORMAT CSV, HEADER);"
```

### Étape 2 : Exécution du script

Lancez le script principal pour démarrer l'importation :

```bash
cd netbox-device-autodiscovery/import_yaml
python3 main.py
```
<br> 

Le script va effectuer les actions suivantes :

  * Lire le fichier source.
  * Vérifier si le Type de Device existe (ex: Cisco Catalyst).
  * Vérifier si le Device existe déjà (Mise à jour via PATCH ou Création via POST).
  * Créer les Interfaces associées.
  * Assigner les Adresses IP et MAC.

---

## 👤 Auteur

Pierre Famchon
  * Étudiant en BUT R&T (Réseaux et Télécommunications) - IUT de Béthune.
  * Stage réalisé au service Système et Réseau de l'UTC.

---

## 📚 Références

  * Documentation NetBox
  * Documentation NetDisco
