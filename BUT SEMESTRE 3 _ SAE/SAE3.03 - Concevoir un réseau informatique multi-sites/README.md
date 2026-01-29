<div align="center">

  <img src="https://cdn-icons-png.flaticon.com/512/2282/2282186.png" alt="Logo Server Infrastructure" width="120" height="120">
  
  # SAE 3.03 - Architecture Réseau Multi-Sites
  
  **Conception, déploiement et administration d'un réseau d'entreprise interconnecté.**

  ![Status](https://img.shields.io/badge/Status-Termin%C3%A9-success?style=for-the-badge)
  ![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge)
  ![School](https://img.shields.io/badge/%C3%89cole-IUT-orange?style=for-the-badge)

  <br>

  [Description](#-description-du-projet) •
  [Stack Technique](#-stack-technique) •
  [Structure](#-structure-du-dépôt) •
  [Installation](#installation) •
  [Phase du Projet](#-déroulement-du-projet) •
  [Bilan](#-conclusion) •
  [Auteurs](#-auteurs)

</div>

---

## 📖 Description du Projet

Ce projet vise à concevoir une infrastructure réseau complète pour une entreprise disposant d'un **Siège** et d'une **Succursale**, avec une extension vers une **Pépinière**. Il couvre les couches réseaux (L2/L3) ainsi que la couche applicative (Services).

**Objectifs principaux :**
* 🌐 **Interconnexion** sécurisée des sites (VPN/Tunneling).
* 🛡️ **Sécurité** et segmentation (VLANs, ACL, Proxy).
* 🔄 **Haute Disponibilité** de la passerelle (HSRP).
* 💻 **Services** d'entreprise (AD, Web, Mail, Streaming).

---

## 🛠 Stack Technique

### Infrastructure & Réseau
![Cisco](https://img.shields.io/badge/Cisco-1BA0D7?style=for-the-badge&logo=cisco&logoColor=white)
![OSPF](https://img.shields.io/badge/Routing-OSPF-critical?style=for-the-badge)
![HSRP](https://img.shields.io/badge/Redundancy-HSRP-critical?style=for-the-badge)
![VLAN](https://img.shields.io/badge/Switching-VLAN-blueviolet?style=for-the-badge)
![VPN](https://img.shields.io/badge/Tunneling-GRE%20%2F%20IPSec-important?style=for-the-badge)

### Système & Services
![Windows Server](https://img.shields.io/badge/Windows%20Server-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Active Directory](https://img.shields.io/badge/Active%20Directory-0078D4?style=for-the-badge&logo=windows&logoColor=white)
![Postfix](https://img.shields.io/badge/Mail-Postfix-orange?style=for-the-badge)
![Squid](https://img.shields.io/badge/Proxy-Squid-green?style=for-the-badge)

### Application Web & Données
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

---

## 📂 Structure du Dépôt

Voici l'organisation détaillée des fichiers du projet :

```text
.
├── 📁 Documentation/
│   ├── 📄 NAT.docx                    # Configuration du NAT
│   ├── 📄 Tunnel GRE.docx             # Mise en place du tunnel inter-sites
│   ├── 📄 Windows-server 1.docx       # Installation Active Directory & DNS
│   ├── 📄 lancer le serveur video.docx # Procédure Streaming
│   ├── 📄 packet de tracer.docx       # Notes sur la simulation
│   ├── 📄 routeur.docx                # Configs spécifiques routeurs
│   ├── 📄 switch.docx                 # Configs spécifiques switches
│   └── 📄 utile.docx                  # Mémos commandes Cisco/Linux
│
├── 📁 Fichier de config/
│   ├── 📂 Réseau/
│   │   ├── 📄 routeur_pepiniaire.txt     # Config Routeur Pépinière
│   │   ├── 📄 routeur_siege.txt          # Config Routeur Siège (NAT, GRE)
│   │   ├── 📄 routeur_succursale.txt     # Config Routeur Succursale
│   │   ├── 📄 switch_couche3_1_siège.txt # Switch L3 Principal (HSRP 105)
│   │   └── 📄 switch_couche3_2_siège.txt # Switch L3 Secours (HSRP 95)
│   │
│   └── 📂 Services/
│       ├── 📂 Mail/                      # Config Postfix
│       ├── 📂 Proxy/                     # Config Squid
│       ├── 📂 Vidéo/                     # Scripts ffmpeg
│       ├── 📂 Web/                       # App Flask + Dockerfile
│       └── 📂 Wifi/                      # Config Contrôleur
│
├── 📄 Rapport final.docx              # Rapport complet (Word)
├── 📄 Rapport final.pdf               # Rapport complet (PDF)
├── 📄 README.md                       # Ce fichier
├── 📄 Schéma.drawio                   # Topologie éditable
├── 🖼️ Schéma.jpg                      # Image Topologie
└── 🔌 SchémaPackettracer.pkt          # Simulation Cisco Packet Tracer
```
---

## ⚙️ <a name="installation"></a>Installation et Configuration
### 🐳 Services Web (Docker)
L'application Web et la base de données sont conteneurisées.

* Accédez au dossier : Fichier de config/Services/Web
* Lancez la stack :
  
```bash
docker-compose up -d
```
* Accès via navigateur : http://localhost:80 (ou port configuré).

### 🪟 Active Directory (Windows)
* Domaine : societeX.pepiniere.rt
* Utilisateurs : Scripts PowerShell disponibles dans la documentation pour générer l'arborescence (UO Admin, Prod, Perso).
* GPO : Mappage lecteur réseau et restrictions configurés.

### 🎥 Streaming Vidéo
Utilisation de ffmpeg pour diffuser un flux UDP.

* Serveur (Diffusion) :

```bash
ffmpeg -stream_loop -1 -i CatHuh.mp4 -f mpegts udp://172.31.20.156:5000
```

* Client (Lecture) :
```bash
ffplay -i udp://172.31.20.156:5000
```

### 🔒 Proxy (Squid)
Modification de la politique de sécurité dans /etc/squid/squid.conf :

```bash
# Autoriser le trafic (par défaut deny)
http_access allow all
```
---

## 📅 Déroulement du Projet
Le projet a été mené en plusieurs phases successives, de l'infrastructure physique aux services applicatifs.

### Phase 1 : Architecture & Adressage
* Définition du plan d'adressage IP (VLSM) pour optimiser les sous-réseaux.
* Segmentation logique par VLANs (10 à 50) pour séparer les flux (Admin, Prod, VoIP, etc.).

### Phase 2 : Commutation & Redondance (LAN)
* Configuration des switches de couche 3 au Siège.
* Mise en place du HSRP (Hot Standby Router Protocol) :
  * Switch 1 : Active (Priorité 105)
  * Switch 2 : Standby (Priorité 95)
  * Objectif : Assurer une passerelle virtuelle résiliente pour les utilisateurs.

### Phase 3 : Routage & WAN
* Configuration du protocole OSPF (Area 0) pour le routage dynamique interne.
* Mise en place du NAT/PAT pour l'accès Internet via le routeur de bordure.
* Création d'un Tunnel GRE (encapsulé ou non dans IPSec) pour relier le LAN du Siège à celui de la Succursale de manière transparente.

### Phase 4 : Déploiement des Services
Une fois le réseau stable, les services ont été installés sur des serveurs (VMs et Docker) :

* Infrastructure : Contrôleur de domaine (AD DS), DNS, DHCP.
* Web : Déploiement de l'application Flask via docker-compose.
* Proxy : Configuration des ACLs Squid pour filtrer le web.
* Multimédia : Tests de streaming vidéo UDP multicast/unicast.

---

## 🔚 Conclusion
🔚 Conclusion
Ce projet SAE 3.03 nous a permis de consolider nos compétences d'administrateurs réseaux et systèmes. Nous avons réussi à :

* ✅ Interconnecter des sites distants via des technologies WAN standards.
* ✅ Sécuriser l'accès et la disponibilité du réseau (HSRP, VLANs).
* ✅ Intégrer des services hétérogènes (Linux/Windows/Cisco) dans un environnement unifié.

Les défis principaux ont résidé dans la cohérence du routage inter-VLANs et la configuration fine du Tunnel GRE à travers le NAT.

---

## 👥 Auteurs
Projet réalisé par l'équipe :

| Nom | Rôle |
| :--- | :--- |
| **Pierre Famchon** | Lead Network / Config Cisco |
| **Michel Bauchart** | Services Windows / AD |
| **Baptiste Duval** | Services Linux / Web |
| **Nicolas Edouard** | Documentation / Tests |
