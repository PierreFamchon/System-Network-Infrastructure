<div align="center">

  <img src="https://cdn-icons-png.flaticon.com/512/3253/3253239.png" alt="Logo SDR Project" width="120" height="120">

  # SAE 3.01 : Système de Transmission SDR
  
  **Étude, Analyse Spectrale et Transmission Vidéo via Adalm Pluto**

  ![GNU Radio](https://img.shields.io/badge/GNU%20Radio-3.10-orange?style=for-the-badge&logo=gnu-radio&logoColor=white)
  ![Adalm Pluto](https://img.shields.io/badge/Hardware-Adalm%20Pluto-blue?style=for-the-badge&logo=analogdevices&logoColor=white)
  ![Signal Processing](https://img.shields.io/badge/Signal-Processing-success?style=for-the-badge)
  ![VLC](https://img.shields.io/badge/Stream-VLC-E86900?style=for-the-badge&logo=vlc&logoColor=white)

  <br>

  [Description](#-contexte-du-projet) •
  [Matériel](#-matériel-et-logiciels) •
  [Installation](#-installation-et-configuration) •
  [Phases du Projet](#-déroulement-du-projet) •
  [Projet Final](#projet-final) •
  [Bilan](#-conclusion) •
  [Auteurs](#-auteurs) 

</div>

---

## 📖 Contexte du Projet

Ce dépôt regroupe les travaux, schémas GNU Radio (`.grc`) et résultats du projet **SAE 3.01** réalisé dans le cadre de la 2ème année de BUT R&T (Réseaux et Télécommunications).

Le projet porte sur l'exploration approfondie de la **Radio Logicielle (SDR)**. Il débute par l'analyse spectrale de l'environnement, passe par la simulation de modulations analogiques, et aboutit à la mise en œuvre d'une **chaîne complète de transmission vidéo** via le module **Adalm Pluto**.

---

## 🛠 Matériel et Logiciels

## 🛠 Stack Technique

### 🧰 Équipement Hardware

![SDR](https://img.shields.io/badge/SDR-ADALM%20PLUTO-005f9e?style=for-the-badge&logo=analogdevices&logoColor=white)
![Analyzer](https://img.shields.io/badge/ANALYZER-SPECTRAN%20HF--6065-404040?style=for-the-badge&labelColor=e04e39)
![Antenna](https://img.shields.io/badge/ANTENNA-HYPERLOG%207060-404040?style=for-the-badge&labelColor=7c4dff)

### 💻 Environnement Software

![GNU Radio](https://img.shields.io/badge/SIGNAL-GNU%20RADIO-e86900?style=for-the-badge&logo=gnu-radio&logoColor=white)
![MCS](https://img.shields.io/badge/ANALYSIS-MCS%20SPECTRUM-0078d7?style=for-the-badge&labelColor=404040)
![VLC](https://img.shields.io/badge/STREAM-VLC%20PLAYER-ff8800?style=for-the-badge&logo=vlc&logoColor=white)
![Drivers](https://img.shields.io/badge/DRIVERS-PLUTOSDR%20USB-555555?style=for-the-badge&logo=usb&logoColor=white)

---

## 🚀 Installation et Configuration

Pour reproduire ces expérimentations, suivez les étapes d'installation ci-dessous.

### 1. Prérequis Système
* Un PC sous **Linux (Ubuntu recommandé)** ou **Windows 10/11**.
* Ports USB 2.0 ou 3.0 disponibles.

### 2. Installation des Pilotes Adalm Pluto
Téléchargez et installez les pilotes nécessaires pour la reconnaissance du périphérique USB :
* [Télécharger les drivers PlutoSDR](https://wiki.analog.com/university/tools/pluto/drivers/windows)

### 3. Installation de GNU Radio
L'environnement principal de développement est GNU Radio.
* **Windows :** Utilisez l'installateur [Radioconda](https://github.com/ryanvolz/radioconda).
* **Linux :**
  ```bash
  sudo apt-get update
  sudo apt-get install gnuradio
   ```
### 4. Récupération du Projet
Clonez ce dépôt pour accéder aux fichiers .grc (GNU Radio Companion) :

  ```bash
git clone [https://github.com/PierreFamchon/RT2-Projets.git](https://github.com/PierreFamchon/RT2-Projets.git)
cd BUT SEMESTRE 3_SAE
cd SAE3.01 - Etude et mise en oeuvre d’un système de transmission
   ```
### 5. Connexion 
Connectez l'Adalm Pluto en USB. Vérifiez qu'il est reconnu comme un périphérique réseau (généralement 192.168.2.1).

---

## 📡 Déroulement du Projet

### Phase 1 : Prise en main et Analyse Spectrale
Avant toute transmission, une analyse de l'environnement radiofréquence a été réalisée avec le Spectran V4 et le logiciel MCS

* GSM 900 / 1800 : Identification des opérateurs (ex: Vodafone ~ -36 dBm).
* LTE (2.1 GHz) : Visualisation des bandes 4G.
* WiFi (2.4 & 5 GHz) : Observation des canaux 802.11.

Note : Les fichiers .mdr sont disponibles dans le dossier /measurements.

### Phase 2 : Simulation et Modulation AM
Découverte de GNU Radio via la création de signaux et l'analyse FFT.

* Échantillonnage : Étude de la relation samp_rate / freq_var.
* Résolution Fréquentielle : Delta f = samp_rate / FFT_Size
  * Exemple : Pour 32768 points à 32kHz → Delta f ≈ 0.97 Hz.
* Modulation AM : Multiplication Porteuse $\times$ Modulant et observation des bandes latérales.

### Phase 3 : Réception FM et RDS
Mise en œuvre d'un récepteur FM (88-108 MHz) via l'Adalm Pluto.

* Cible : Skyrock (106.93 MHz).
* Architecture : Source Pluto → Filtre Passe-Bas → Démod WBFM → Audio Sink.
* RDS : Utilisation de gr-rds pour l'extraction des métadonnées (Nom station, Traffic).

### Phase 4 : Émission/Réception Audio (Duplex)
Communication vocale bidirectionnelle entre deux binômes.

*  Technique : Modulation FM de la voix (48kHz) sur porteuse 2.4 GHz.
*  Flux : Remplacement des blocs UDP par PlutoSDR Sink/Source.
*  Résultat : Full Duplex fonctionnel vérifié par analyseur de spectre.

---

## 🎥 <a name="projet-final"></a>Projet Final : Transmission Vidéo (Streaming)
L'objectif ultime : transmettre un flux vidéo MP4 d'un PC à un autre par ondes radio.

### Architecture du Système

* Émission (PC A + Pluto A)
     * VLC : Lecture MP4 → Stream vers UDP :5679.
     * GNU Radio : UDP Source → Modulation GMSK/FM → Pluto Sink (2.4 GHz).

* Transmission
     * Signal RF à 2.4 GHz via antennes.

* Réception (Pluto B + PC B)
     * GNU Radio : Pluto Source → Démodulation → UDP Sink (IP Cible:5680).
     * VLC : Lecture flux réseau udp://@:5680.

### Résultats Obtenus
* ✅ Vidéo transmise (Codec H.265 + Audio MP3).
* ✅ Fluidité correcte et faible latence.
* ✅ Validation de la capacité de débit du PlutoSDR.

---

## 🔚 Conclusion
Ce projet a permis de valider des compétences clés en télécommunications :

* 🔧 Hardware : Calibration SDR et manipulation d'antennes.
* 📶 Signal : Traitement numérique (DSP) avec GNU Radio.
* 🔄 Protocoles : Compréhension des chaînes de transmission (UDP, Modulation).
* 🐞 Debug : Résolution de problèmes sur une chaîne complexe.

---

## 👥 Auteurs

* **Auteurs :** Pierre Famchon & Michel Bauchart
* **Formation :** BUT R&T - IUT de Béthune
* **Année :** 2024-2025
* **Objectif :** Comprendre les concepts de la transmission numérique/analogique et maîtriser la chaîne de traitement SDR.
