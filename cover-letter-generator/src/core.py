# src/core.py - Version mise à jour
import asyncio
from typing import Dict, Any, Optional, Union
import tempfile
import os

async def process_cover_letter_request(
    resume_file, 
    job_content, 
    openai_client, 
    firecrawl_client,
    # Nouveaux paramètres optionnels avec valeurs par défaut
    tone: str = "Professionnel",
    length: str = "Moyenne (350-400 mots)",
    language: str = "Français",
    template: str = "Classique",
    include_salary: bool = False,
    include_availability: bool = True,
    emphasize_skills: bool = True,
    company_name: str = "",
    position_title: str = "",
    hiring_manager: str = "",
    key_skills: str = "",
    achievements: str = "",
    **kwargs  # Pour capturer d'autres paramètres non prévus
) -> str:
    """
    Génère une lettre de motivation personnalisée basée sur le CV et l'offre d'emploi.
    
    Args:
        resume_file: Fichier CV uploadé
        job_content: Contenu de l'offre d'emploi (URL, texte, ou fichier)
        openai_client: Client OpenAI pour la génération
        firecrawl_client: Client Firecrawl pour l'extraction web
        tone: Ton de la lettre (Professionnel, Enthousiaste, etc.)
        length: Longueur souhaitée de la lettre
        language: Langue de la lettre
        template: Template à utiliser
        include_salary: Inclure les attentes salariales
        include_availability: Inclure la disponibilité
        emphasize_skills: Mettre l'accent sur les compétences techniques
        company_name: Nom de l'entreprise
        position_title: Titre du poste
        hiring_manager: Nom du recruteur
        key_skills: Compétences clés à souligner
        achievements: Réalisations importantes
        
    Returns:
        str: Lettre de motivation générée
    """
    
    try:
        # Étape 1: Traitement du CV
        resume_content = await extract_resume_content(resume_file)
        
        # Étape 2: Traitement de l'offre d'emploi
        job_description = await extract_job_content(job_content, firecrawl_client)
        
        # Étape 3: Génération de la lettre avec les paramètres personnalisés
        cover_letter = await generate_personalized_cover_letter(
            resume_content=resume_content,
            job_description=job_description,
            openai_client=openai_client,
            generation_params={
                'tone': tone,
                'length': length,
                'language': language,
                'template': template,
                'include_salary': include_salary,
                'include_availability': include_availability,
                'emphasize_skills': emphasize_skills,
                'company_name': company_name,
                'position_title': position_title,
                'hiring_manager': hiring_manager,
                'key_skills': key_skills,
                'achievements': achievements
            }
        )
        
        return cover_letter
        
    except Exception as e:
        print(f"Erreur dans process_cover_letter_request: {str(e)}")
        raise e


async def extract_resume_content(resume_file) -> str:
    """
    Extrait le contenu du CV selon le format du fichier.
    """
    try:
        if resume_file.type == "application/pdf":
            return await extract_pdf_content(resume_file)
        elif resume_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                                 "application/msword"]:
            return await extract_word_content(resume_file)
        elif resume_file.type == "text/plain":
            return resume_file.getvalue().decode("utf-8")
        else:
            raise ValueError(f"Format de fichier non supporté: {resume_file.type}")
            
    except Exception as e:
        print(f"Erreur lors de l'extraction du CV: {str(e)}")
        raise e


async def extract_job_content(job_content, firecrawl_client) -> str:
    """
    Extrait le contenu de l'offre d'emploi selon le type d'input.
    """
    try:
        if isinstance(job_content, str):
            # Si c'est une URL
            if job_content.startswith(('http://', 'https://')):
                return await extract_from_url(job_content, firecrawl_client)
            # Si c'est du texte direct
            else:
                return job_content
        else:
            # Si c'est un fichier uploadé
            return await extract_file_content(job_content)
            
    except Exception as e:
        print(f"Erreur lors de l'extraction de l'offre: {str(e)}")
        raise e


async def extract_pdf_content(pdf_file) -> str:
    """
    Extrait le contenu d'un fichier PDF.
    """
    try:
        import PyPDF2
        from io import BytesIO
        
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.getvalue()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
        
    except ImportError:
        # Fallback si PyPDF2 n'est pas installé
        return "Contenu PDF non disponible - PyPDF2 requis"
    except Exception as e:
        print(f"Erreur lors de l'extraction PDF: {str(e)}")
        raise e


async def extract_word_content(word_file) -> str:
    """
    Extrait le contenu d'un fichier Word.
    """
    try:
        from docx import Document
        from io import BytesIO
        
        doc = Document(BytesIO(word_file.getvalue()))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
        
    except ImportError:
        # Fallback si python-docx n'est pas installé
        return "Contenu Word non disponible - python-docx requis"
    except Exception as e:
        print(f"Erreur lors de l'extraction Word: {str(e)}")
        raise e


async def extract_from_url(url: str, firecrawl_client) -> str:
    """
    Extrait le contenu d'une URL avec Firecrawl.
    """
    try:
        result = firecrawl_client.scrape_url(url)
        return result.get('content', '')
    except Exception as e:
        print(f"Erreur lors du scraping URL: {str(e)}")
        raise e


async def extract_file_content(file) -> str:
    """
    Extrait le contenu d'un fichier uploadé.
    """
    try:
        if file.type == "application/pdf":
            return await extract_pdf_content(file)
        elif file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                          "application/msword"]:
            return await extract_word_content(file)
        elif file.type == "text/plain":
            return file.getvalue().decode("utf-8")
        else:
            return "Format de fichier non supporté"
    except Exception as e:
        print(f"Erreur lors de l'extraction du fichier: {str(e)}")
        raise e


async def generate_personalized_cover_letter(
    resume_content: str, 
    job_description: str, 
    openai_client, 
    generation_params: Dict[str, Any]
) -> str:
    """
    Génère une lettre de motivation personnalisée avec les paramètres spécifiés.
    """
    try:
        # Construction du prompt personnalisé
        prompt = build_personalized_prompt(resume_content, job_description, generation_params)
        
        # Appel à l'API OpenAI
        response = await openai_client.chat.completions.create(
            model="gpt-4",  # ou "gpt-3.5-turbo" selon vos besoins
            messages=[
                {"role": "system", "content": "Vous êtes un expert en rédaction de lettres de motivation."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Erreur lors de la génération: {str(e)}")
        raise e


def build_personalized_prompt(
    resume_content: str, 
    job_description: str, 
    params: Dict[str, Any]
) -> str:
    """
    Construit un prompt personnalisé basé sur les paramètres fournis.
    """
    
    # Mapping des longueurs
    length_mapping = {
        "Courte (250-300 mots)": "entre 250 et 300 mots",
        "Moyenne (350-400 mots)": "entre 350 et 400 mots",
        "Longue (450-500 mots)": "entre 450 et 500 mots"
    }
    
    # Mapping des tons
    tone_mapping = {
        "Professionnel": "un ton professionnel et formel",
        "Enthousiaste": "un ton enthousiaste et motivé",
        "Confiant": "un ton confiant et assuré",
        "Humble": "un ton humble et respectueux",
        "Créatif": "un ton créatif et original"
    }
    
    # Construction du prompt
    prompt = f"""
    Rédigez une lettre de motivation personnalisée en {params['language']} avec les spécifications suivantes:

    **CV du candidat:**
    {resume_content}

    **Offre d'emploi:**
    {job_description}

    **Instructions de rédaction:**
    - Ton: {tone_mapping.get(params['tone'], 'professionnel')}
    - Longueur: {length_mapping.get(params['length'], 'entre 350 et 400 mots')}
    - Template: {params['template']}
    """
    
    # Ajout des informations personnalisées
    if params['company_name']:
        prompt += f"\n- Nom de l'entreprise: {params['company_name']}"
    if params['position_title']:
        prompt += f"\n- Titre du poste: {params['position_title']}"
    if params['hiring_manager']:
        prompt += f"\n- Nom du recruteur: {params['hiring_manager']}"
    
    # Ajout des éléments à mettre en avant
    if params['key_skills']:
        prompt += f"\n- Compétences clés à souligner: {params['key_skills']}"
    if params['achievements']:
        prompt += f"\n- Réalisations importantes: {params['achievements']}"
    
    # Ajout des options spéciales
    if params['include_salary']:
        prompt += "\n- Inclure une mention des attentes salariales"
    if params['include_availability']:
        prompt += "\n- Mentionner la disponibilité du candidat"
    if params['emphasize_skills']:
        prompt += "\n- Mettre l'accent sur les compétences techniques"
    
    prompt += """

    **Consignes importantes:**
    - Analysez attentivement le CV et l'offre d'emploi
    - Identifiez les points de correspondance
    - Personnalisez le contenu selon les spécifications
    - Utilisez un style adapté au secteur d'activité
    - Concluez par une invitation à l'entretien
    - Respectez la longueur demandée
    """
    
    return prompt