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

| Catégorie | Technologies |
| :--- | :--- |
| **Réseau** | Cisco IOS, ASA Firewall, OSPF, HSRP, SSHv2 |
| **Système** | Windows Server (DNS Manager), Linux (Ubuntu) |
| **Web** | Nginx (Reverse Proxy/WAF), Python (Flask), MySQL |
| **Outils Pentest** | Kali Linux, OWASP ZAP, Bettercap, SQLMap, Nmap |

---

## 📂 Structure

L'arborescence du projet est organisée comme suit :

```text
SAE-Cyber-Security/
├── Network_Config/
[cite_start]│   ├── Routers/           # Configs R1, R2, R3 (OSPF, Tunnel) [cite: 165]
[cite_start]│   ├── Switches/          # Configs L3_Siege, L3_Succu (VLANs, HSRP) [cite: 384]
[cite_start]│   └── Firewalls/         # Configs ASA (Policies, NAT) [cite: 620]
├── Web_Server/
[cite_start]│   ├── Nginx/             # Fichiers .conf (SSL, Headers sécurité) [cite: 1008]
[cite_start]│   ├── App_Flask/         # Code Python (app.py) et Templates HTML [cite: 853]
[cite_start]│   └── Database/          # Script SQL création users [cite: 953]
└── Documentation/
    ├── Rapport_Projet.pdf # Rapport complet
    └── ANSSI_Compliance/  # Matrice de conformité ANSSI
```
