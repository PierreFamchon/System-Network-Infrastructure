# SAE 3.03 - Conception d'un réseau informatique multi-sites

Ce projet porte sur la conception et la mise en œuvre d'une architecture réseau complète pour une entreprise disposant d'un **Siège** et d'une **Succursale**, avec une extension potentielle vers un site **Pépinière**. Il intègre à la fois le déploiement de l'infrastructure réseau (routage, VLANs, VPN) et la configuration des services applicatifs associés.

## 📋 Table des Matières

1. [Description du Projet](#description-du-projet)
2. [Structure du Dépôt](#structure-du-dépôt)
3. [Architecture Réseau](#architecture-réseau)
4. [Installation et Configuration des Services](#installation-et-configuration-des-services)
    - [Services Web et Base de Données](#services-web-et-base-de-données)
    - [Active Directory et DNS](#active-directory-et-dns)
    - [Service Mail (Postfix)](#service-mail-postfix)
    - [Proxy et Sécurité](#proxy-et-sécurité)
    - [Streaming Vidéo](#streaming-vidéo)
5. [Auteurs](#auteurs)

## 📖 Description du Projet

L'objectif est de déployer un réseau d'entreprise robuste et sécurisé interconnectant plusieurs sites géographiques.

**Points clés :**
* **Réseau :** Routage OSPF, segmentation par VLANs (10 à 50), redondance via HSRP, et interconnexion de sites via Tunnels (GRE/IPSec).
* **Services :** Hébergement Web (Flask/MySQL), Annuaire centralisé (AD), Messagerie, Proxy web et Streaming vidéo.
* **Équipements :** Routeurs et commutateurs de couche 3 (Cisco), Serveurs Linux (Ubuntu/Debian) et Windows Server.

## 📂 Structure du Dépôt

L'arborescence du projet est organisée comme suit :

```text
.
├── Documentation/
│   ├── NAT.docx                    # Documentation sur la configuration NAT
│   ├── Tunnel GRE.docx             # Mise en place du tunnel inter-sites
│   ├── Windows-server 1.docx       # Installation et config Active Directory
│   ├── lancer le serveur video.docx # Procédure pour le streaming
│   ├── packet de tracer.docx       # Notes sur la simulation
│   ├── routeur.docx                # Configs spécifiques aux routeurs
│   ├── switch.docx                 # Configs spécifiques aux switchs
│   └── utile.docx                  # Commandes et mémos divers
├── Fichier de config/
│   ├── Réseau/                     # Configurations brutes (Cisco IOS)
│   └── Services/                   # Scripts de services (Web, DB, etc.)
├── README.md                       # Ce fichier
├── Rapport final.docx              # Rapport de projet (format Word)
├── Rapport final.pdf               # Rapport de projet (format PDF)
├── Schéma.drawio                   # Schéma éditable (Draw.io)
├── Schéma.jpg                      # Image de la topologie réseau
└── SchémaPackettracer.pkt          # Fichier de simulation Cisco Packet Tracer
