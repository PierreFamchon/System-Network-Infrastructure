# SAE 3.01 : Étude et Mise en œuvre d'un Système de Transmission SDR

![Banner Project](https://via.placeholder.com/1000x200?text=SDR+Project+Adalm+Pluto+GNU+Radio)
Ce dépôt contient les travaux, schémas GNU Radio et résultats du projet **SAE 3.01** réalisé dans le cadre de la 2ème année de BUT R&T (Réseaux et Télécommunications).

Le projet porte sur l'exploration de la **Radio Logicielle (SDR)**, de l'analyse spectrale à la mise en œuvre d'une chaîne complète de transmission vidéo via le module **Adalm Pluto**.

---

## 📋 Table des Matières

1. [Auteurs et Contexte](#-auteurs-et-contexte)
2. [Matériel et Logiciels Utilisés](#-matériel-et-logiciels-utilisés)
3. [Phase 1 : Prise en main et Analyse Spectrale](#-phase-1--prise-en-main-et-analyse-spectrale)
4. [Phase 2 : Simulation et Modulation AM sur GNU Radio](#-phase-2--simulation-et-modulation-am-sur-gnu-radio)
5. [Phase 3 : Réception FM et RDS](#-phase-3--réception-fm-et-rds)
6. [Phase 4 : Émission/Réception Audio (Duplex)](#-phase-4--émissionréception-audio-duplex)
7. [Projet Final : Transmission Vidéo (Streaming)](#-projet-final--transmission-vidéo-streaming)
8. [Conclusion](#-conclusion)

---

## 👥 Auteurs et Contexte

* **Auteurs :** Pierre Famchon & Michel Bauchart
* **Formation :** BUT R&T - IUT de Béthune
* **Année :** 2024-2025
* **Objectif :** Comprendre les concepts de la transmission numérique/analogique et maîtriser la chaîne de traitement SDR.

---

## 🛠 Matériel et Logiciels Utilisés

### Matériel
* **SDR :** [Analog Devices ADALM-PLUTO](https://www.analog.com/en/design-center/evaluation-hardware-and-software/evaluation-boards-kits/adalm-pluto.html) (325 MHz - 3.8 GHz).
* **Analyseur de Spectre :** Spectran HF-6065 V4.
* **Antenne :** HyperLOG 7060 (Directionnelle Log-périodique, 700 MHz - 6 GHz).

### Logiciels
* **GNU Radio Companion :** Pour la création des diagrammes de flux de traitement du signal.
* **MCS Spectrum Analyzer :** Pour l'interface avec le Spectran V4.
* **VLC Media Player :** Pour le streaming vidéo via UDP.
* **Pilotes :** PlutoSDR-M2k-USB-Drivers.

---

## 📡 Phase 1 : Prise en main et Analyse Spectrale

Avant de transmettre, nous avons analysé l'environnement radiofréquence à l'aide du **Spectran V4** et du logiciel **MCS**.

**Analyses réalisées :**
* **GSM 900 / 1800 :** Identification des opérateurs (Vodafone, Telekom, O2, E-Plus) et mesure des puissances (ex: Vodafone ~ -36 dBm).
* **LTE (2.1 GHz) :** Visualisation des bandes de fréquences 4G.
* **WiFi (2.4 GHz & 5 GHz) :** Observation des canaux 802.11b/g/n.

*Note : Les fichiers de mesures `.mdr` sont disponibles dans le dossier `/measurements` (si vous les uploadez).*

---

## 🎛 Phase 2 : Simulation et Modulation AM sur GNU Radio

Découverte de l'environnement GNU Radio via la création de signaux et l'analyse de la transformée de Fourier (FFT).

### Concepts Clés
* **Échantillonnage :** Relation entre `samp_rate` et `freq_var`.
* **Résolution Fréquentielle :** Vérification de la formule $\Delta f = \frac{samp\_rate}{FFT\_Size}$.
    * *Exemple :* Pour une FFT de 32768 points à 32kHz, $\Delta f \approx 0.97 Hz$.
* **Modulation AM :** Multiplication de deux signaux cosinus (porteuse et modulant) et observation des bandes latérales.

`![Flowgraph AM](path/to/am_flowgraph.png)`

---

## 📻 Phase 3 : Réception FM et RDS

Mise en œuvre d'un récepteur FM analogique commercial (88-108 MHz) avec l'Adalm Pluto.

* **Station testée :** Skyrock (106.93 MHz).
* **Architecture :** Source Pluto -> Filtre Passe-Bas -> Démodulation FM -> Sortie Audio.
* **Décodage RDS :** Tentative d'utilisation de la librairie `gr-rds` pour extraire les informations numériques (Nom de la station, Traffic Info).
    * *Défis :* Installation complexe de la librairie et réception du signal RDS parfois difficile selon le placement de l'antenne.

---

## 🎙 Phase 4 : Émission/Réception Audio (Duplex)

Réalisation d'un système de communication vocale entre deux binômes équipés de PlutoSDR.

1.  **Simplex :** Un émetteur et un récepteur.
2.  **Full Duplex :** Communication bidirectionnelle simultanée.

**Configuration technique :**
* Utilisation de blocs `UDP Sink/Source` remplacés par `PlutoSDR Sink/Source`.
* Modulation FM de la voix (48kHz) sur une porteuse à 2.4 GHz.
* **Résultat :** Communication fonctionnelle, synchronisation du signal observée sur l'analyseur de spectre (FFT).

---

## 🎥 Projet Final : Transmission Vidéo (Streaming)

L'objectif final était de transmettre un flux vidéo MP4 d'un PC à un autre en passant par les ondes via les modules SDR.

### Architecture du Système

1.  **Émission (PC 1 + Pluto A) :**
    * **VLC :** Lecture du fichier MP4 -> Streaming vers UDP (Port 5679).
    * **GNU Radio :** `UDP Source` (Port 5679) -> Modulation -> `PlutoSDR Sink` (Porteuse 2.4 GHz).

2.  **Transmission :** Signal radio à 2.4 GHz.

3.  **Réception (Pluto B + PC 2) :**
    * **GNU Radio :** `PlutoSDR Source` -> Démodulation -> `UDP Sink` (vers IP cible, Port 5680).
    * **VLC :** Lecture du flux réseau `udp://@:5680`.

### Résultats
* Vidéo transmise avec succès (Codec H.265 + MP3).
* Qualité fluide, pas d'interférences majeures notées lors du test final.
* Démonstration de la capacité du PlutoSDR à gérer des flux de données continus.

`![Transmission Vidéo VLC](path/to/vlc_result.png)`

---

## 🔚 Conclusion

Ce projet a permis de valider les compétences suivantes :
* Configuration et calibration de matériel RF (SDR et Antennes).
* Traitement du signal numérique avec GNU Radio.
* Compréhension des protocoles de transmission (UDP, Modulation Analogique/Numérique).
* Débogage de chaînes de transmission complexes.

---

*Ce projet a été réalisé avec les ressources de l'IUT de Béthune.*
