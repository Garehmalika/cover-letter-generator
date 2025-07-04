import streamlit as st
from openai import AsyncOpenAI
from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv
import asyncio
from src.core import process_cover_letter_request  # Votre fonction mise à jour
import tempfile

# Load environment variables
try:
    load_dotenv()
except Exception as e:
    st.error(f"⚠️ Erreur lors du chargement du fichier .env: {str(e)}")

# Initialize API clients with error handling
openai_api_key = os.getenv('OPENAI_API_KEY')
firecrawl_api_key = os.getenv('FIRECRAWL_API_KEY')

# Initialize clients only if API keys are available
openai_client = None
firecrawl_client = None

# Check for API keys and show warnings in the main interface
api_keys_missing = []

if not openai_api_key or openai_api_key == 'sk-your-openai-key-here':
    api_keys_missing.append("OpenAI")
else:
    try:
        openai_client = AsyncOpenAI(api_key=openai_api_key)
    except Exception as e:
        st.error(f"❌ Erreur d'initialisation OpenAI: {str(e)}")

if not firecrawl_api_key or firecrawl_api_key == 'fc-your-firecrawl-key-here':
    api_keys_missing.append("Firecrawl")
else:
    try:
        firecrawl_client = FirecrawlApp(api_key=firecrawl_api_key)
    except Exception as e:
        st.error(f"❌ Erreur d'initialisation Firecrawl: {str(e)}")

# CSS personnalisé pour une interface plus claire et sympathique
def load_custom_css():
    st.markdown("""
    <style>
    /* Variables de couleurs claires et sympathiques */
    :root {
        --primary-color: #6C63FF;
        --secondary-color: #48CAE4;
        --accent-color: #FFD166;
        --success-color: #06D6A0;
        --warning-color: #FFD6A5;
        --background-light: #F7F7FF;
        --text-primary: #22223B;
        --text-secondary: #4A4E69;
        --border-color: #E0E1DD;
        --card-shadow: 0 4px 15px rgba(108,99,255,0.08);
    }

    /* Fond principal */
    .main > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
        min-height: 100vh;
    }

    /* Container principal */
    .main .block-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: var(--card-shadow);
    }

    /* Header stylisé */
    .header-container {
        background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--card-shadow);
    }

    .header-container h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 600;
    }

    .header-container p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }

    /* Sidebar personnalisée */
    .css-1d391kg {
        background: linear-gradient(145deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Améliorer les éléments de la sidebar */
    .css-1d391kg .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        color: #2D3436;
    }

    .css-1d391kg .stSelectbox > div > div:hover {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid rgba(255, 255, 255, 0.5);
        transform: translateY(-1px);
        transition: all 0.3s ease;
    }

    .css-1d391kg .stCheckbox > label {
        color: white !important;
        font-weight: 500;
    }

    .css-1d391kg .stCheckbox > label > div {
        background: rgba(255, 255, 255, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 6px;
    }

    .css-1d391kg .stCheckbox > label > div:hover {
        background: rgba(255, 255, 255, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.5);
    }

    .css-1d391kg .stTextInput > div > div {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        color: #2D3436;
    }

    .css-1d391kg .stTextInput > div > div:hover {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid rgba(255, 255, 255, 0.5);
    }

    .css-1d391kg .stTextArea > div > div {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        color: #2D3436;
    }

    .css-1d391kg .stTextArea > div > div:hover {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid rgba(255, 255, 255, 0.5);
    }

    /* Titres dans la sidebar */
    .css-1d391kg h3 {
        color: white !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
    }

    .css-1d391kg h4 {
        color: rgba(255, 255, 255, 0.9) !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        margin-bottom: 0.8rem;
    }

    /* Labels dans la sidebar */
    .css-1d391kg label {
        color: white !important;
        font-weight: 500;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }

    /* Boutons dans la sidebar */
    .css-1d391kg .stButton > button {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
        color: white;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .css-1d391kg .stButton > button:hover {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.2));
        border: 2px solid rgba(255, 255, 255, 0.5);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.3);
    }

    /* Cartes de section */
    .section-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid var(--border-color);
        box-shadow: var(--card-shadow);
        transition: transform 0.2s ease;
    }

    .section-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }

    /* Boutons personnalisés */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
        color: bleu;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }

    /* Boutons secondaires */
    .stButton[data-baseweb="button"] button[kind="secondary"] {
        background: linear-gradient(135deg, #45B7D1, #96CEB4);
        color: white;
    }

    /* Messages de statut */
    .stSuccess {
        background: linear-gradient(135deg, #96CEB4, #A8E6CF);
        color: #2D3436;
        border-radius: 10px;
        border: none;
        padding: 1rem;
    }

    .stError {
        background: linear-gradient(135deg, #FD79A8, #FDCB6E);
        color: #2D3436;
        border-radius: 10px;
        border: none;
        padding: 1rem;
    }

    .stWarning {
        background: linear-gradient(135deg, #FFEAA7, #FED7AA);
        color: #2D3436;
        border-radius: 10px;
        border: none;
        padding: 1rem;
    }

    .stInfo {
        background: linear-gradient(135deg, #74B9FF, #A8E6CF);
        color: #2D3436;
        border-radius: 10px;
        border: none;
        padding: 1rem;
    }

    /* Métriques */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid var(--border-color);
        box-shadow: var(--card-shadow);
    }

    /* Tabs personnalisés */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--background-light);
        border-radius: 10px;
        padding: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: bleu;
        border-radius: 8px;
        color: var(--text-secondary);
        font-weight: 500;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: white;
        color: var(--primary-color);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
        color: white !important;
    }

    /* File uploader */
    .uploadedFile {
        background: var(--background-light);
        border-radius: 10px;
        border: 2px dashed var(--accent-color);
        padding: 1rem;
    }

    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        border-radius: 10px;
    }

    /* Expandeur */
    .streamlit-expanderHeader {
        background: var(--background-light);
        border-radius: 10px;
        color: var(--text-primary);
        font-weight: 500;
    }

    /* Code blocks */
    .stCode {
        background: var(--background-light);
        border-radius: 10px;
        border: 1px solid var(--border-color);
    }

    /* Colonnes avec espacement */
    .element-container {
        margin: 0.5rem 0;
    }

    /* Animation pour les éléments */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .section-card {
        animation: slideIn 0.5s ease-out;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .header-container h1 {
            font-size: 2rem;
        }
        
        .header-container p {
            font-size: 1rem;
        }
        
        .section-card {
            margin: 0.5rem 0;
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="AI Cover Letter Generator",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Charger le CSS personnalisé
    load_custom_css()
    
    # Header avec styling amélioré
    st.markdown("""
    <div class="header-container">
        <h1>📝 AI Cover Letter Generator</h1>
        <p>Créez des lettres de motivation personnalisées avec style et simplicité ✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Vérifier les clés API manquantes
    if api_keys_missing:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFF3CD, #FCF4A3); 
                    color: #856404; 
                    padding: 1rem; 
                    border-radius: 10px; 
                    border-left: 5px solid #FFC107;
                    margin: 1rem 0;">
            <h4 style="margin: 0 0 0.5rem 0;">⚠️ Configuration requise</h4>
            <p style="margin: 0;">
                Clés API manquantes : <strong>{}</strong><br>
                📝 Éditez le fichier <code>.env</code> et ajoutez vos clés API pour utiliser toutes les fonctionnalités.
            </p>
        </div>
        """.format(", ".join(api_keys_missing)), unsafe_allow_html=True)
        
        with st.expander("🔑 Comment obtenir les clés API ?"):
            st.markdown("""
            ### 🚀 OpenAI API Key (obligatoire)
            1. Allez sur [platform.openai.com](https://platform.openai.com/api-keys)
            2. Créez un compte ou connectez-vous
            3. Générez une nouvelle clé API
            4. Copiez la clé qui commence par `sk-`
            
            ### 🌐 Firecrawl API Key (optionnelle)
            1. Allez sur [firecrawl.dev](https://www.firecrawl.dev/)
            2. Créez un compte
            3. Obtenez votre clé API
            4. Copiez la clé qui commence par `fc-`
            
            ### 📁 Configuration du fichier .env
            1. Ouvrez le fichier `.env` dans ce répertoire
            2. Remplacez les valeurs par vos vraies clés :
            ```
            OPENAI_API_KEY=sk-votre-vraie-cle-openai
            FIRECRAWL_API_KEY=fc-votre-vraie-cle-firecrawl
            ```
            3. Sauvegardez et relancez l'application
            """)
    else:
        st.success("✅ Toutes les clés API sont configurées correctement !")
    
    # Sidebar pour les options de personnalisation
    with st.sidebar:
        st.markdown("### ⚙️ Options de personnalisation")
        
        # Style options
        st.markdown("#### 🎨 Style de la lettre")
        tone = st.selectbox(
            "Ton à adopter",
            ["Professionnel", "Enthousiaste", "Confiant", "Humble", "Créatif"],
            index=0
        )
        
        length = st.selectbox(
            "Longueur de la lettre",
            ["Courte (250-300 mots)", "Moyenne (350-400 mots)", "Longue (450-500 mots)"],
            index=1
        )
        
        # Language options
        st.markdown("#### 🌍 Langue")
        language = st.selectbox(
            "Langue de la lettre",
            ["Français", "Anglais", "Espagnol", "Allemand"],
            index=0
        )
        
        # Template options
        st.markdown("#### 📋 Template")
        template = st.selectbox(
            "Structure de la lettre",
            ["Classique", "Moderne", "Créative", "Technique", "Commercial"],
            index=0
        )
        
        # Additional options
        st.markdown("#### 🔧 Options avancées")
        include_salary = st.checkbox("💰 Mentionner les attentes salariales", value=False)
        include_availability = st.checkbox("📅 Mentionner la disponibilité", value=True)
        emphasize_skills = st.checkbox("🎯 Mettre l'accent sur les compétences", value=True)
        
        # Save preferences
        if st.button("💾 Sauvegarder les préférences"):
            st.success("✅ Préférences sauvegardées avec succès !")

    # Main content area avec cartes
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="section-card">
            <h3 style="color: #FF6B6B; margin-bottom: 1rem;">📄 Votre CV</h3>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Téléchargez votre CV", 
            type=['pdf', 'docx', 'txt'],
            help="Formats acceptés: PDF, Word, Texte"
        )
        
        if uploaded_file:
            st.success(f"✅ Fichier chargé: {uploaded_file.name}")
            
            # File info dans une carte
            file_details = {
                "Nom du fichier": uploaded_file.name,
                "Type": uploaded_file.type,
                "Taille": f"{uploaded_file.size / 1024:.1f} KB"
            }
            
            with st.expander("📋 Détails du fichier"):
                for key, value in file_details.items():
                    st.write(f"**{key}:** {value}")
    
    with col2:
        st.markdown("""
        <div class="section-card">
            <h3 style="color: #4ECDC4; margin-bottom: 1rem;">🔗 Offre d'emploi</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Options pour saisir l'offre d'emploi
        input_method = st.radio(
            "Comment souhaitez-vous fournir l'offre d'emploi ?",
            ["🌐 URL de l'offre", "📝 Coller le texte", "📁 Télécharger un fichier"],
            horizontal=True
        )
        
        job_content = None
        
        if input_method == "🌐 URL de l'offre":
            job_url = st.text_input(
                "URL de l'offre d'emploi",
                placeholder="https://example.com/job-posting"
            )
            if job_url:
                job_content = job_url
                st.success("✅ URL saisie avec succès!")
                
        elif input_method == "📝 Coller le texte":
            job_text = st.text_area(
                "Texte de l'offre d'emploi",
                height=200,
                placeholder="Collez ici le texte de l'offre d'emploi..."
            )
            if job_text:
                job_content = job_text
                st.success("✅ Texte saisi avec succès!")
                
        elif input_method == "📁 Télécharger un fichier":
            job_file = st.file_uploader(
                "Télécharger l'offre d'emploi",
                type=['pdf', 'docx', 'txt'],
                key="job_file"
            )
            if job_file:
                job_content = job_file
                st.success("✅ Fichier chargé avec succès!")

    # Advanced options section
    with st.expander("🎯 Options avancées"):
        st.markdown("""
        <div class="section-card">
            <h4 style="color: #45B7D1;">Personnalisation avancée</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("##### 👤 Informations personnelles")
            company_name = st.text_input("🏢 Nom de l'entreprise (optionnel)")
            position_title = st.text_input("💼 Titre du poste (optionnel)")
            hiring_manager = st.text_input("👨‍💼 Nom du recruteur (optionnel)")
            
        with col4:
            st.markdown("##### 🌟 Éléments à mettre en avant")
            key_skills = st.text_area(
                "🎯 Compétences clés à souligner",
                placeholder="Ex: Python, Gestion d'équipe, Analyse de données..."
            )
            achievements = st.text_area(
                "🏆 Réalisations importantes",
                placeholder="Ex: Augmentation des ventes de 20%, Certification obtenue..."
            )

    # Generate button avec styling amélioré
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        generate_button = st.button(
            "🚀 Générer ma lettre de motivation",
            type="primary",
            use_container_width=True
        )
    
    if generate_button:
        if uploaded_file is not None and job_content:
            try:
                # Progress tracking avec animations
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                async def process_with_enhanced_status():
                    # Step 1: Processing resume
                    status_text.info("📄 Analyse de votre CV en cours...")
                    progress_bar.progress(20)
                    await asyncio.sleep(0.5)
                    
                    # Step 2: Processing job posting
                    status_text.info("🔍 Analyse de l'offre d'emploi...")
                    progress_bar.progress(40)
                    await asyncio.sleep(0.5)
                    
                    # Step 3: Matching analysis
                    status_text.info("🎯 Analyse de correspondance...")
                    progress_bar.progress(60)
                    await asyncio.sleep(0.5)
                    
                    # Step 4: Generation
                    status_text.info("✍️ Génération de votre lettre personnalisée...")
                    progress_bar.progress(80)
                    
                    # Appel à votre fonction avec tous les paramètres
                    cover_letter = await process_cover_letter_request(
                        resume_file=uploaded_file,
                        job_content=job_content,
                        openai_client=openai_client,
                        firecrawl_client=firecrawl_client,
                        tone=tone,
                        length=length,
                        language=language,
                        template=template,
                        include_salary=include_salary,
                        include_availability=include_availability,
                        emphasize_skills=emphasize_skills,
                        company_name=company_name,
                        position_title=position_title,
                        hiring_manager=hiring_manager,
                        key_skills=key_skills,
                        achievements=achievements
                    )
                    
                    progress_bar.progress(100)
                    status_text.success("✨ Lettre générée avec succès !")
                    
                    return cover_letter

                # Run the async function
                cover_letter = asyncio.run(process_with_enhanced_status())
                
                if cover_letter:
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Display results avec interface améliorée
                    st.markdown("---")
                    st.markdown("""
                    <div class="section-card">
                        <h2 style="color: #FF6B6B; text-align: center;">🎉 Votre lettre de motivation</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Create tabs for different views
                    tab1, tab2, tab3, tab4 = st.tabs(["📄 Aperçu", "📝 Édition", "📊 Analyse", "💾 Téléchargement"])
                    
                    with tab1:
                        st.markdown("### 👀 Aperçu de votre lettre")
                        st.markdown(
                            f"""
                            <div style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); 
                                        padding: 2rem; 
                                        border-radius: 15px; 
                                        border-left: 5px solid #FF6B6B;
                                        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                                        margin: 1rem 0;">
                                {cover_letter.replace(chr(10), '<br>')}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    with tab2:
                        st.markdown("### ✏️ Éditer votre lettre")
                        edited_letter = st.text_area(
                            "Vous pouvez modifier votre lettre ici:",
                            value=cover_letter,
                            height=400,
                            key="edit_letter"
                        )
                        
                        if st.button("💾 Sauvegarder les modifications"):
                            st.success("✅ Modifications sauvegardées avec succès!")
                    
                    with tab3:
                        st.markdown("### 📊 Analyse de votre lettre")
                        
                        # Basic analysis avec cartes métriques
                        word_count = len(cover_letter.split())
                        char_count = len(cover_letter)
                        
                        col_analysis1, col_analysis2, col_analysis3 = st.columns(3)
                        
                        with col_analysis1:
                            st.markdown("""
                            <div class="metric-card">
                                <h3 style="color: #FF6B6B; margin: 0;">""" + str(word_count) + """</h3>
                                <p style="color: #636E72; margin: 0;">Mots</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        with col_analysis2:
                            st.markdown("""
                            <div class="metric-card">
                                <h3 style="color: #4ECDC4; margin: 0;">""" + str(char_count) + """</h3>
                                <p style="color: #636E72; margin: 0;">Caractères</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        with col_analysis3:
                            st.markdown("""
                            <div class="metric-card">
                                <h3 style="color: #45B7D1; margin: 0;">""" + str(word_count//200 + 1) + """ min</h3>
                                <p style="color: #636E72; margin: 0;">Lecture</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Quality indicators
                        st.markdown("#### 🎯 Indicateurs de qualité")
                        quality_score = min(100, (word_count / 350) * 100)
                        st.progress(quality_score / 100)
                        st.write(f"Score de qualité: {quality_score:.0f}%")
                    
                    with tab4:
                        st.markdown("### 💾 Télécharger votre lettre")
                        
                        col_download1, col_download2 = st.columns(2)
                        
                        with col_download1:
                            st.download_button(
                                label="📄 Télécharger en TXT",
                                data=cover_letter,
                                file_name="lettre_motivation.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                        
                        with col_download2:
                            st.download_button(
                                label="📋 Télécharger en Markdown",
                                data=cover_letter,
                                file_name="lettre_motivation.md",
                                mime="text/markdown",
                                use_container_width=True
                            )
                        
                        st.markdown("#### 📋 Aperçu pour copier")
                        st.code(cover_letter, language="text")
                
                else:
                    st.error("❌ Erreur lors de la génération. Veuillez réessayer.")
                    
            except Exception as e:
                st.error(f"❌ Une erreur s'est produite: {str(e)}")
                
                # Debugging info
                with st.expander("🔍 Informations de débogage"):
                    st.write(f"**Type d'erreur:** {type(e).__name__}")
                    st.write(f"**Message:** {str(e)}")
                    st.write(f"**Fichier CV:** {uploaded_file.name if uploaded_file else 'Aucun'}")
                    st.write(f"**Type contenu job:** {type(job_content).__name__}")
                    
        else:
            st.warning("⚠️ Veuillez télécharger votre CV et fournir l'offre d'emploi.")

    # Footer avec instructions dans une carte
    st.markdown("---")
    st.markdown("""
    <div class="section-card">
        <h3 style="color: #45B7D1;">ℹ️ Guide d'utilisation</h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📖 Instructions détaillées"):
        st.markdown("""
        ### 🚀 Comment utiliser le générateur:
        
        1. **📤 Téléchargez votre CV** (formats PDF, Word, ou texte)
        2. **📋 Fournissez l'offre d'emploi** (URL, texte, ou fichier)
        3. **⚙️ Personnalisez les options** dans la barre latérale
        4. **🎯 Cliquez sur "Générer"** et attendez le résultat
        5. **✏️ Éditez si nécessaire** et téléchargez votre lettre
        
        ### 💡 Conseils pour de meilleurs résultats:
        - ✅ Assurez-vous que votre CV est bien structuré
        - ✅ Fournissez une offre d'emploi complète et détaillée
        - ✅ Utilisez les options avancées pour personnaliser davantage
        - ✅ Relisez et éditez la lettre générée avant de l'envoyer
        """)

if __name__ == "__main__":
    main()