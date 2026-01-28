# 📡 SAE 3.02 - Développer des applications communicantes

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?style=for-the-badge&logo=flask&logoColor=black)
![CSS3](https://img.shields.io/badge/CSS3-Style-orange?style=for-the-badge&logo=css3&logoColor=white)

## 🔎 Application de Recherche Multi-Formats par Mot-Clé

### 📝 Description du Projet

Ce projet a été réalisé dans le cadre de la **SAE 3.02 "Développer des applications communicantes"** de l'IUT R&T.

L'objectif principal est de développer une application web légère basée sur **Flask (Python)**. Elle permet d'indexer et d'effectuer une recherche de mots-clés dans divers types de documents stockés localement. L'application offre une interface conviviale pour saisir un mot-clé, filtrer par type de fichier (texte, PDF, HTML, Excel) et visualiser le contexte précis des correspondances.

---

### ✨ Fonctionnalités Clés

* **🎨 Interface Web Intuitive :** Formulaire de recherche épuré et résultats lisibles, stylisés avec une charte graphique cohérente (couleur principale : orange `#FF7F00`).
* **📂 Recherche Multi-Format :** Support natif pour :
    * 📄 Fichiers texte (`.txt`)
    * 📕 Documents PDF (`.pdf`)
    * 🌐 Fichiers HTML (`.html`)
    * 📊 Fichiers Excel (`.xlsx`)
* **⚙️ Recherche Avancée :**
    * Recherche textuelle standard (insensible à la casse).
    * Support des **Expressions Régulières (RegEx)** pour des requêtes complexes.
* **👁️ Résultats Contextualisés :** Affichage précis incluant :
    * Le nom du fichier.
    * La localisation (numéro de ligne, page ou cellule).
    * L'extrait du texte contenant le mot-clé.

---

### 🛠 Technologies Utilisées

| Catégorie | Technologie | Rôle |
| :--- | :--- | :--- |
| **Backend** | `Python 3` | Langage de programmation principal. |
| **Backend** | `Flask` | Framework web pour la gestion des routes (`/`, `/search`). |
| **Parsing** | `PyPDF2` | Extraction de texte des fichiers PDF. |
| **Parsing** | `BeautifulSoup` | Extraction de texte brut des fichiers HTML. |
| **Parsing** | `openpyxl` | Lecture des fichiers Excel (`.xlsx`). |
| **Logique** | `re` (module) | Gestion des expressions régulières. |
| **Frontend** | `HTML5 / Jinja2` | Structure des pages et templating. |
| **Frontend** | `CSS3` | Mise en forme (`style.css`). |

---

### 📂 Structure du Dépôt

Voici l'organisation des fichiers du projet :

```text
SAE3.02 - Développer des applications communicantes/
├── app.py                      # Le cœur de l'application Flask
├── requirements.txt            # Liste des dépendances Python
├── static/
│   └── css/
│       └── style.css           # Styles CSS du frontend
├── templates/
│   ├── index.html              # Formulaire de recherche (page d'accueil)
│   └── results.html            # Gabarit d'affichage des résultats
├── text_files/                 # Dossier pour les fichiers .txt à indexer
│   ├── test1.txt
│   └── test2.txt
├── pdf_files/                  # Dossier pour les fichiers .pdf à indexer
│   ├── R302_Cours_BGP_vf.pdf
│   └── ...
├── html_files/                 # Dossier pour les fichiers .html à indexer
│   ├── test1.html
│   └── ...
└── excel_files/                # Dossier pour les fichiers .xlsx à indexer
    └── rap.xlsx
```
---

### 🚀 Installation et Démarrage

Suivez ces étapes pour lancer l'application sur votre machine.

#### 1. Prérequis
Assurez-vous d'avoir [Python 3](https://www.python.org/downloads/) installé sur votre système.

#### 2. Cloner le Dépôt
Récupérez le code source via Git :

git clone [https://github.com/PierreFamchon/portfolio-rt.git](https://github.com/PierreFamchon/portfolio-rt.git)
```bash
git clone  [https://github.com/PierreFamchon/RT2-Projets/BUT_SEMESTRE_3_SAE/SAE3.02_-_](https://github.com/PierreFamchon/portfolio-rt.git)
cd <NOM_DU_DOSSIER>
```

#### 3. Installer les Dépendances
Installez les bibliothèques nécessaires listées dans `requirements.txt` :

```bash
pip install -r requirements.txt
```
#### 4. Exécuter l'Application
Lancez le serveur Flask :

```bash
python app.py
```
Le terminal devrait afficher que le serveur tourne sur http://127.0.0.1:5000.

#### 5. Utilisation

Ouvrez votre navigateur web préféré et accédez à l'adresse http://127.0.0.1:5000 pour commencer à rechercher dans vos documents.

