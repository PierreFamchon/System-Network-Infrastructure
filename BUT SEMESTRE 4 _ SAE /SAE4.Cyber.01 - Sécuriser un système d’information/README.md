<div align="center">

  <img src="https://cdn-icons-png.flaticon.com/512/2092/2092663.png" alt="Logo Cyber Project" width="120" height="120">

  # SAE 4.01 : Sécuriser un Système d'Information
  
  **Durcissement d'infrastructure, DNSSEC & Web Application Firewall (WAF)**

  ![Cisco](https://img.shields.io/badge/Network-Cisco_IOS-blue?style=for-the-badge&logo=cisco&logoColor=white)
  ![Nginx](https://img.shields.io/badge/Web-Nginx_Secured-green?style=for-the-badge&logo=nginx&logoColor=white)
  ![Python](https://img.shields.io/badge/Backend-Python_Flask-yellow?style=for-the-badge&logo=python&logoColor=white)
  ![DNSSEC](https://img.shields.io/badge/Protocol-DNSSEC-red?style=for-the-badge&logo=security&logoColor=white)

  <br>

  [Description](#-description) •
  [Fonctionnalités](#-fonctionnalités) •
  [Stack Technique](#-stack-technique) •
  [Structure](#-structure) •
  [Installation](#-installation) •
  [Phases du Projet](#-phases-du-projet) •
  [Bilan](#-bilan) •
  [Auteurs](#-auteurs) 

</div>

---

## 📝 Description

Ce projet vise à **renforcer la sécurité d'une infrastructure réseau multi-sites** (Siège et Succursale) reliés par un tunnel IPSEC. [cite_start]L'objectif est de protéger le système d'information contre des attaques courantes telles que l'empoisonnement de cache DNS, les attaques MITM et les injections Web [cite: 129-130].

L'architecture est segmentée en trois zones distinctes pour limiter la surface d'attaque :
* **Admin (VLAN 10) :** Serveurs critiques (DNS, Web).
* **Production (VLAN 20) :** Systèmes industriels.
* [cite_start]**Service (VLAN 30) :** Utilisateurs standards [cite: 142-145].

---

## ✨ Fonctionnalités

### 🛡️ Sécurité Réseau
* [cite_start]**Segmentation & Filtrage :** Cloisonnement par VLANs et filtrage strict via ACLs (ex: interdiction ping Prod <-> Service) [cite: 479-482].
* [cite_start]**Pare-feux ASA :** Inspection de paquets (DPI) et gestion de zones de sécurité (Inside 100, Outside 0, DMZ 50) [cite: 631-641].
* [cite_start]**Redondance :** Haute disponibilité des passerelles via protocole **HSRP**[cite: 449].
* [cite_start]**Confidentialité :** Tunnel VPN IPSEC pour les communications inter-sites[cite: 178].

### 🔐 Services Sécurisés
* [cite_start]**DNSSEC :** Signature cryptographique de la zone `societe2.pepiniere.rt` (clés KSK/ZSK) pour garantir l'authenticité des réponses [cite: 821-830].
* [cite_start]**Web Application Firewall (WAF) :** Configuration Nginx avancée (HSTS, Anti-XSS, Anti-Clickjacking) [cite: 1018-1028].
* [cite_start]**Authentification Forte :** Application Flask avec hashage des mots de passe (Werkzeug) et **CAPTCHA dynamique** fait maison pour contrer le brute-force[cite: 857, 1098].

---

## 🛠 Stack Technique

### Infrastructure & Réseau

![Cisco](https://img.shields.io/badge/CISCO-IOS-00bceb?style=for-the-badge&logo=cisco&logoColor=white)
![Firewall](https://img.shields.io/badge/FIREWALL-CISCO%20ASA-00bceb?style=for-the-badge&labelColor=404040&logo=cisco&logoColor=white)
![Routing](https://img.shields.io/badge/ROUTING-OSPF-e04e39?style=for-the-badge&labelColor=404040)
![Redundancy](https://img.shields.io/badge/REDUNDANCY-HSRP-e04e39?style=for-the-badge&labelColor=404040)
![Security](https://img.shields.io/badge/SECURITY-SSHv2-7c4dff?style=for-the-badge&labelColor=404040)

### Système & Services

![Windows Server](https://img.shields.io/badge/WINDOWS-DNS%20MANAGER-0078d7?style=for-the-badge&logo=windows&logoColor=white)
![Linux](https://img.shields.io/badge/LINUX-UBUNTU-fcc624?style=for-the-badge&logo=linux&logoColor=black)
![Protocol](https://img.shields.io/badge/PROTOCOL-DNSSEC-crimson?style=for-the-badge&labelColor=404040&logo=security&logoColor=white)

### Application Web & Données

![Nginx](https://img.shields.io/badge/WEB-NGINX%20(WAF)-009639?style=for-the-badge&labelColor=404040&logo=nginx&logoColor=white)
![Python](https://img.shields.io/badge/BACKEND-PYTHON-3776ab?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/FRAMEWORK-FLASK-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/DATABASE-MYSQL-4479a1?style=for-the-badge&logo=mysql&logoColor=white)

### Outils de Pentest

![Kali](https://img.shields.io/badge/OS-KALI%20LINUX-557C94?style=for-the-badge&logo=kali-linux&logoColor=white)
![Scanner](https://img.shields.io/badge/SCANNING-NMAP-1679A7?style=for-the-badge&labelColor=404040)
![Audit](https://img.shields.io/badge/AUDIT-OWASP%20ZAP-4B5CC4?style=for-the-badge&labelColor=404040&logo=owasp&logoColor=white)
![Injection](https://img.shields.io/badge/INJECTION-SQLMAP-e04e39?style=for-the-badge&labelColor=404040)
![MITM](https://img.shields.io/badge/ATTACK-BETTERCAP-crimson?style=for-the-badge&labelColor=404040)
---

## 📂 Structure

L'arborescence du projet est organisée comme suit :

```text
📁 SAE-Cyber-Security/
├── 📁 Network_Config/
│   ├── 📁 Routers/           # Configs R1, R2, R3 (OSPF, Tunnel)
|   ├── 📁 Switches/          # Configs L3_Siege, L3_Succu (VLANs, HSRP)
|   └── 📁 Firewalls/         # Configs ASA (Policies, NAT)
├── 📁 Web_Server/
├── 📁 Nginx/             # Fichiers .conf (SSL, Headers sécurité)
│   ├── 📁 App_Flask/         # Code Python (app.py) et Templates HTML 
│   └── 📁 Database/          # Script SQL création users 
└── 📁 Documentation/
    ├── 📄 Rapport_Projet.pdf # Rapport complet
    └── 📁 ANSSI_Compliance/  # Matrice de conformité ANSSI
```
---

## ⚙ Installation
### Phase 1 : Configuration Réseau (Cisco)

Charger les configurations sur les équipements respectifs. Assurez-vous d'activer le chiffrement des mots de passe :

```cisco
service password-encryption
username admin privilege 15 secret 5 $1$mERr$tN2nmMK5hNorN4zAZEGGz.
ip ssh version 2
```
### Phase 2 : Serveur DNS (Windows)

* Installer le rôle Serveur DNS.
* Créer la zone societe2.pepiniere.rt.
* Signer la zone via DNSSEC (RSA/SHA-256, 2048 bits).

### Phase 3 : Serveur Web (Linux)

Installer Nginx et Python, puis configurer le WAF dans /etc/nginx/sites-available/flask_app :

```nginx
# Force HTTPS & Sécurité
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-XSS-Protection "1; mode=block" always;
```
Générer les certificats SSL auto-signés via OpenSSL.

---

## 🚀 Phases du Projet

* Architecture & Adressage : Définition des VLANs et du plan d'adressage IP .
* Mise en œuvre Réseau : Configuration du routage OSPF, du Tunnel GRE/IPSEC et des ACLs.
* Sécurisation DNS : Déploiement de DNSSEC pour empêcher le DNS Spoofing.
* Sécurisation Web : Développement de l'app Flask sécurisée et durcissement Nginx.
* Pentesting : Tests d'intrusion pour valider les défenses.

---

## 📊 Bilan

Les tests de sécurité offensifs ont validé l'efficacité des mesures :

* ✅ DNS Spoofing : Attaque via Bettercap échouée (la validation DNSSEC rejette la réponse falsifiée).
* ✅ Injections SQL : Bloquées par l'utilisation de requêtes préparées et filtrage.
* ✅ Brute-Force : Echec grâce au CAPTCHA et à la politique de bannissement.
* ✅ Scan de Ports : Nmap confirme que seuls les ports 80/443 sont exposés.

---

## 👥 Auteurs

Projet réalisé dans le cadre de la formation R&T (2024-2025) par :

* Pierre FAMCHON - Tests de sécurité & Rapport
* Michel BACHART - Sécurisation DNS
* Baptiste DUVAL - Sécurisation Web
* Nicolas EDOUARD - Recommandations ANSSI
