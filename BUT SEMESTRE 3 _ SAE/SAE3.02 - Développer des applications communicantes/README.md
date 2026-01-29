<div align="center">

  <img src="https://cdn-icons-png.flaticon.com/512/1005/1005141.png" alt="Logo Code Dev" width="120" height="120">

  # SAE 3.02 - Développer des applications communicantes
  
  **Application de Recherche Multi-Formats par Mot-Clé**

  ![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
  ![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?style=for-the-badge&logo=flask&logoColor=black)
  ![CSS3](https://img.shields.io/badge/CSS3-Style-orange?style=for-the-badge&logo=css3&logoColor=white)
  ![IUT](https://img.shields.io/badge/School-IUT%20R%26T-red?style=for-the-badge)

  <br>

  [Description](#-description-du-projet) •
  [Fonctionnalités](#-fonctionnalités-clés) •
  [Stack Technique](#-technologies-utilisées) •
  [Structure](#-structure-du-dépôt) •
  [Installation](#-installation-et-démarrage)•
  [Phases du projet](#-déroulement-du-projet) •
  [Bilan](#-conclusion) •
  [Auteurs](#-auteurs) 
  
</div>

---

## 📝 Description du Projet

Ce projet a été réalisé dans le cadre de la **SAE 3.02 "Développer des applications communicantes"** de l'IUT R&T.

L'objectif principal est de développer une application web légère basée sur **Flask (Python)**. Elle permet d'indexer et d'effectuer une recherche de mots-clés dans divers types de documents stockés localement. L'application offre une interface conviviale pour saisir un mot-clé, filtrer par type de fichier (texte, PDF, HTML, Excel) et visualiser le contexte précis des correspondances.

---

## ✨ Fonctionnalités Clés

* **🎨 Interface Web Intuitive**
    * Formulaire de recherche épuré et résultats lisibles.
    * Stylisé avec une charte graphique cohérente (couleur principale : orange `#FF7F00`).

* **📂 Recherche Multi-Format**
    * Support natif pour :
        * 📄 Fichiers texte (`.txt`)
        * 📕 Documents PDF (`.pdf`)
        * 🌐 Fichiers HTML (`.html`)
        * 📊 Fichiers Excel (`.xlsx`)

* **⚙️ Recherche Avancée**
    * Recherche textuelle standard (insensible à la casse).
    * Support des **Expressions Régulières (RegEx)** pour des requêtes complexes.

* **👁️ Résultats Contextualisés**
    * Affichage précis incluant :
        * Le nom du fichier.
        * La localisation (numéro de ligne, page ou cellule).
        * L'extrait du texte contenant le mot-clé.

---

## 🛠 Technologies Utilisées

Ce projet s'appuie sur une stack Python robuste pour le backend et les standards du web pour le frontend.

### Backend & Logique

![Python](https://img.shields.io/badge/LANGUAGE-PYTHON%203-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/FRAMEWORK-FLASK-000000?style=for-the-badge&logo=flask&logoColor=white)
![Regex](https://img.shields.io/badge/LOGIC-REGEX%20(RE)-404040?style=for-the-badge&labelColor=7c4dff)

### Parsing & Extraction de Données

![PyPDF2](https://img.shields.io/badge/PDF-PYPDF2-e04e39?style=for-the-badge&labelColor=404040&logo=adobeacrobatreader&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/HTML-BEAUTIFULSOUP-404040?style=for-the-badge&labelColor=3776ab)
![Openpyxl](https://img.shields.io/badge/EXCEL-OPENPYXL-1D6F42?style=for-the-badge&labelColor=404040&logo=microsoftexcel&logoColor=white)

### Frontend & Interface

![HTML5](https://img.shields.io/badge/MARKUP-HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Jinja2](https://img.shields.io/badge/TEMPLATE-JINJA2-B41717?style=for-the-badge&logo=jinja&logoColor=white)
![CSS3](https://img.shields.io/badge/STYLE-CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

---

## 📂 Structure du Dépôt

Voici l'organisation détaillée des fichiers du projet :

```text
📁 SAE3.02 - Développer des applications communicantes/
├── 📄 app.py                      # Le cœur de l'application Flask
├── 📄 requirements.txt            # Liste des dépendances Python
├── 📁 static/
│   └── 📁 css/
│       └── 📄 style.css           # Styles CSS du frontend
├── 📁 templates/
│   ├── 📄 index.html              # Formulaire de recherche (page d'accueil)
│   └── 📄 results.html            # Gabarit d'affichage des résultats
├── 📁 text_files/                 # Dossier pour les fichiers .txt à indexer
│   ├── 📄 test1.txt
│   └── 📄 test2.txt
├── 📁 pdf_files/                  # Dossier pour les fichiers .pdf à indexer
│   ├── 📄 R302_Cours_BGP_vf.pdf
│   └── ...
├── 📁 html_files/                 # Dossier pour les fichiers .html à indexer
│   ├── 📄 test1.html
│   └── ...
└── 📁 excel_files/                # Dossier pour les fichiers .xlsx à indexer
    └── 📄 rap.xlsx
```
---

## 🚀 Installation et Démarrage

Suivez ces étapes pour lancer l'application sur votre machine.

### 1. Prérequis
Assurez-vous d'avoir [Python 3](https://www.python.org/downloads/) installé sur votre système.

### 2. Cloner le Dépôt
Récupérez le code source via Git :

```bash
git clone git clone https://github.com/PierreFamchon/RT2-Projets.git](https://github.com/PierreFamchon/RT2-Projets.git)
cd RT2-Projets
cd "BUT SEMESTRE 3 _ SAE"
cd "SAE3.02 - Développer des applications..."
```

### 3. Installer les Dépendances
Installez les bibliothèques nécessaires listées dans `requirements.txt` :

```bash
pip install -r requirements.txt
```
### 4. Exécuter l'Application
Lancez le serveur Flask :

```bash
python app.py
```
Le terminal devrait afficher que le serveur tourne sur http://127.0.0.1:5000.

### 5. Utilisation

Ouvrez votre navigateur web préféré et accédez à l'adresse http://127.0.0.1:5000 pour commencer à rechercher dans vos documents.

---

## 📅 Déroulement du Projet
Le développement de l'application a suivi une approche incrémentale, séparant la logique métier de l'interface utilisateur.

### Phase 1 : Scripting & Parsing (Backend)
* Création des scripts Python pour ouvrir et lire les différents formats de fichiers.
* Intégration des bibliothèques spécifiques (PyPDF2 pour le PDF, openpyxl pour Excel).
* Mise au point de la logique d'extraction de texte (nettoyage des balises HTML avec BeautifulSoup).

### Phase 2 : Moteur de Recherche (Core Logic)
* Développement de l'algorithme de parcours de dossiers.
* Implémentation du module re pour gérer les recherches par Expressions Régulières.
* Gestion du contexte : récupération des lignes précédant et suivant le mot-clé trouvé pour l'affichage.

### Phase 3 : Interface Web (Flask)
* Mise en place du serveur Flask et des routes (GET pour l'accueil, POST pour la recherche).
* Liaison entre le moteur de recherche Python et les vues web.
* Gestion des erreurs (fichiers illisibles, aucun résultat trouvé).

### Phase 4 : Frontend & UX
* Création des templates HTML avec Jinja2 pour afficher dynamiquement les résultats.
* Stylisation CSS (Design Responsive, palette de couleurs IUT).

---

## 🔚 Conclusion
Cette SAE 3.02 a permis de mettre en pratique les compétences de programmation dans un contexte web moderne.

### Acquis principaux :

* ✅ Maîtrise du framework Flask et du pattern MVC (Modèle-Vue-Contrôleur).
* ✅ Manipulation avancée de fichiers et de structures de données en Python.
* ✅ Compréhension et utilisation des Expressions Régulières pour le traitement de texte.
* ✅ Création d'une interface utilisateur fonctionnelle et esthétique.

---

## 👥 Auteurs
Projet réalisé par l'équipe :

| Nom | Rôle |
| :--- | :--- |
| **Pierre Famchon** | Lead Network / Config Cisco |
| **Michel Bauchart** | Services Windows / AD |
| **Baptiste Duval** | Services Linux / Web |
| **Nicolas Edouard** | Documentation / Tests |
