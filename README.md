# 📝 AI Cover Letter Generator

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.29.0-FF4B4B.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT4-00A67E.svg)](https://openai.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered tool that generates customized cover letters by analyzing your resume and job postings.

### **Objectif**
Application web interactive qui génère automatiquement des lettres de motivation personnalisées en analysant le CV de l'utilisateur et l'offre d'emploi ciblée, en utilisant l'intelligence artificielle.

## 🏗️ Architecture technique

### **Technologies utilisées**
- **Frontend** : Streamlit (interface web Python)
- **Backend** : Python avec APIs asynchrones
- **IA** : OpenAI GPT (génération de texte)
- **Web Scraping** : Firecrawl (extraction d'offres d'emploi depuis URLs)
- **Configuration** : dotenv pour les variables d'environnement

### **Structure du projet**
```
sandbox/cover-letter-generator/
├── app.py                 # Application principale Streamlit
├── src/
│   └── core.py           # Logique métier (fonction process_cover_letter_request)
├── .env.example          # Template pour les clés API
└── requirements.txt      # Dépendances Python
```

## ⚙️ Fonctionnalités principales
https://github.com/user-attachments/assets/923934fa-2e84-4bf1-aa38-347696570eaf

*Responsive** : Adapté mobile/desktop
### **1. Interface utilisateur moderne**
- **Design** : Interface colorée avec dégradés et animations CSS
- **Sidebar personnalisée** : Fond dégradé violet-bleu avec éléments semi-transparents
- **Thème** : Couleurs harmonieuses avec effets glassmorphism

### **2. Gestion des fichiers CV**
- **Formats supportés** : PDF, DOCX, TXT
- **Upload drag-and-drop** : Interface intuitive
- **Validation** : Vérification automatique des fichiers

### **3. Saisie des offres d'emploi (3 méthodes)**
- **URL** : Extraction automatique via Firecrawl
- **Texte** : Copier-coller direct
- **Fichier** : Upload de documents d'offre

### **4. Personnalisation avancée**
**Style et ton :**
- 5 tons : Professionnel, Enthousiaste, Confiant, Humble, Créatif
- 3 longueurs : Courte (250-300 mots), Moyenne (350-400), Longue (450-500)
- 4 langues : Français, Anglais, Espagnol, Allemand
- 5 templates : Classique, Moderne, Créative, Technique, Commercial

**Options avancées :**
- Informations entreprise (nom, poste, recruteur)
- Compétences clés à souligner
- Réalisations importantes à mentionner
- Options salariales et disponibilité

### **5. Génération IA intelligente**
- **Analyse comparative** : CV vs offre d'emploi
- **Matching intelligent** : Adaptation automatique du contenu
- **Personnalisation contextuelle** : Selon l'entreprise et le poste

### **6. Interface de résultats sophistiquée**
**4 onglets :**
- **📄 Aperçu** : Rendu final avec mise en forme
- **📝 Édition** : Modification en temps réel
- **📊 Analyse** : Métriques (mots, caractères, temps de lecture, score qualité)
- **💾 Téléchargement** : Export TXT/Markdown + copie

### **7. Gestion d'erreurs robuste**
- **Validation des clés API** : Messages d'erreur explicites
- **Gestion des timeouts** : Interface de progression
- **Debugging** : Informations détaillées en cas d'erreur

## 🎨 Design et UX

### **Palette de couleurs**
- **Primaire** : #FF6B6B (rouge coral)
- **Secondaire** : #4ECDC4 (turquoise)
- **Accent** : #45B7D1 (bleu ciel)
- **Sidebar** : Dégradé #667eea → #764ba2 → #f093fb

### **Éléments visuels**
- **Cartes** : Ombres douces, coins arrondis
- **Boutons** : Dégradés avec animations de survol
- **Inputs** : Style glassmorphism dans la sidebar
- **Progress bars** : Animations fluides

## 🔧 Configuration requise

### **Variables d'environnement**
```env
OPENAI_API_KEY=your_openai_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
```

### **Dépendances Python**
- `streamlit` : Interface web
- `openai` : API GPT
- `firecrawl` : Web scraping
- `python-dotenv` : Variables d'environnement
- `asyncio` : Traitement asynchrone

## 🚀 Utilisation

### **Workflow utilisateur**
1. **Upload CV** → Analyse automatique
2. **Saisie offre** → Extraction des critères
3. **Personnalisation** → Options dans sidebar
4. **Génération** → Traitement IA avec progress bar
5. **Édition/Export** → Interface multi-onglets

### **Avantages**
- **Rapidité** : Génération en quelques secondes
- **Qualité** : Analyse intelligente CV/offre
- **Flexibilité** : Nombreuses options de personnalisation
- **Simplicité** : Interface intuitive
- **Professionnalisme** : Design moderne et soigné

## 🎯 Public cible
- Demandeurs d'emploi
- Étudiants en recherche de stage
- Professionnels en reconversion
- Consultants RH
- Centres de formation/placement

Ce projet combine efficacement l'IA moderne avec une interface utilisateur sophistiquée pour résoudre un besoin concret du marché de l'emploi.



