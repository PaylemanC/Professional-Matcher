import re # Pattern:  r'[^a-z0-9\s]' -> Letters, numbers and spaces
import unicodedata
import spacy
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("es_core_news_sm")

def get_cached_embedding(text, model):
    try:
        from .services.model_singleton import EmbeddingCache
        return EmbeddingCache.get_or_compute(text, model)
    except ImportError:
        return model.encode([text])[0]

def clean_text(text: str, with_stop_words=False) -> str:
    '''
    Returns a cleaned version of the input text.
    - Normalizes unicode characters to ASCII.
    - Converts to lowercase.
    - Removes non-alphanumeric characters (except spaces).
    - Optionally removes stop words if with_stop_words is True.
    '''
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text_doc = nlp(text)
    if with_stop_words == False:
        text = ' '.join([word.text for word in text_doc if not word.is_stop])
    
    return text

def lemmatize_text(text: str, with_stop_words=False) -> str:
    '''
    Returns a lemmatized version of the input text.
    - With clean_text.
    - Uses spaCy's lemmatization.
    '''
    text = clean_text(text, with_stop_words)

    text_doc = nlp(text)
    lemmatized_words = [word.lemma_ for word in text_doc if word.lemma_.strip()]

    return ' '.join(lemmatized_words)

def find_keyword(keyword: str, text_sources: dict) -> list:
    if not keyword or not text_sources:
        return []
    
    keyword_lower = keyword.lower()
    found_in = []
    
    for source_id, text in text_sources.items():
        if text and keyword_lower in text.lower():
            found_in.append(source_id)
    
    return found_in

def find_action_verbs(text: str):
    if not text:
        return []
    
    action_verbs = []
    doc = nlp(text)
    for token in doc:
        # verbos - no auxiliares ni copulativos
        if (token.pos_ == "VERB" and 
            token.lemma_ not in ["ser", "estar", "haber", "tener"] and
            len(token.lemma_) > 2 and
            not token.is_stop):
            action_verbs.append(token.lemma_)
    
    return list(dict.fromkeys(action_verbs))

def extract_action_verbs(job_text, user_profile_text):    
    job_verbs = find_action_verbs(job_text)
    user_verbs = find_action_verbs(user_profile_text) if user_profile_text else []
    
    missing_verbs = list(set(job_verbs) - set(user_verbs)) # SET DIFFERENCE
    
    return missing_verbs

def extract_relevant_phrases(job_text, user_profile_text, kw_model, model):    
    job_keyphrases = kw_model.extract_keywords(
        job_text,
        keyphrase_ngram_range=(2, 3),  
        stop_words=None,
        top_n=10,  
        use_maxsum=True,
        nr_candidates=20  
    )
    
    relevance_patterns = [
        r'metodologia|metodologias|framework|frameworks',
        r'certificacion|certificaciones|titulo|titulos',
        r'testing|pruebas|qa|quality',
        r'devops|ci/cd|continuous|deployment',
        r'agile|agil|scrum|kanban',
        r'cloud|nube|aws|azure|gcp',
        r'api|rest|graphql|microservicio',
        r'docker|kubernetes|container',
        r'master|postgrado|especializacion|diplomado'
    ]
    
    relevant_phrases = []
    for phrase, score in job_keyphrases:
        for pattern in relevance_patterns:
            if re.search(pattern, phrase, re.IGNORECASE):
                relevant_phrases.append((phrase, score))
                break
    
    missing_phrases = []
    
    if user_profile_text and relevant_phrases:
        phrases_text = [phrase[0] for phrase in relevant_phrases]
        try:
            from .services.model_singleton import EmbeddingCache
            phrase_embeddings = EmbeddingCache.get_or_compute_batch(phrases_text, model)
            user_embedding = EmbeddingCache.get_or_compute(user_profile_text, model)
            similarities = cosine_similarity(phrase_embeddings, [user_embedding])
        except ImportError:
            phrase_embeddings = model.encode(phrases_text)
            user_embedding = model.encode([user_profile_text])
            similarities = cosine_similarity(phrase_embeddings, user_embedding)

        for i, (phrase, original_score) in enumerate(relevant_phrases):
            similarity = similarities[i][0]
            
            if similarity < 0.4: 
                missing_phrases.append({
                    'phrase': phrase,
                    'relevance_score': float(original_score),
                    'similarity_score': float(similarity),
                    'suggestion': f"Considera incluir experiencia con: {phrase}"
                })
    elif not user_profile_text:
        for phrase, score in relevant_phrases:
            missing_phrases.append({
                'phrase': phrase,
                'relevance_score': float(score),
                'similarity_score': 0.0,
                'suggestion': f"Considera incluir experiencia con: {phrase}"
            })
    
    return missing_phrases

def extract_soft_skills(job_text, user_profile_text, model):
    skill_patterns = [
        r'comunicacion\s*(efectiva|clara|asertiva)?',
        r'presentacion\s*(oral|escrita|publica)?',
        r'habilidades\s*de\s*comunicacion',
        r'liderazgo\s*(de\s*equipos?)?',
        r'gestion\s*de\s*equipos?',
        r'coordinacion\s*de\s*equipos?',
        r'mentoring|coaching',
        r'pensamiento\s*(critico|analitico)',
        r'resolucion\s*de\s*problemas',
        r'analisis\s*(critico|detallado)',
        r'toma\s*de\s*decisiones',
        r'gestion\s*del?\s*tiempo',
        r'organizacion\s*(personal|laboral)?',
        r'planificacion\s*(estrategica|operativa)?',
        r'multitarea|multi-tarea',
        r'trabajo\s*en\s*equipo',
        r'colaboracion\s*(efectiva)?',
        r'empatia\s*(profesional)?',
        r'adaptabilidad|flexibilidad',
        r'gestion\s*de\s*proyectos?',
        r'orientacion\s*a\s*resultados',
        r'proactividad|iniciativa',
        r'autonomia\s*(profesional)?'
    ]
    
    job_skills = []
    for pattern in skill_patterns:
        matches = re.findall(pattern, job_text, re.IGNORECASE)
        job_skills.extend(matches)
    
    if not job_skills:
        return []
    if not user_profile_text:
        return [{
            'skill': skill,
            'context': 'soft_skill',
            'similarity_score': 0.0
        } for skill in job_skills]
    
    try:
        from .services.model_singleton import EmbeddingCache
        skills_embeddings = EmbeddingCache.get_or_compute_batch(job_skills, model)
        user_embedding = EmbeddingCache.get_or_compute(user_profile_text, model)
        similarities = cosine_similarity(skills_embeddings, [user_embedding])
    except ImportError:
        skills_embeddings = model.encode(job_skills)
        user_embedding = model.encode([user_profile_text])
        similarities = cosine_similarity(skills_embeddings, user_embedding)
    
    missing_skills = []
    for i, skill in enumerate(job_skills):
        similarity = similarities[i][0]
        if similarity < 0.3: 
            missing_skills.append({
                'skill': skill,
                'context': 'soft_skill',
                'similarity_score': float(similarity)
            })
    
    return missing_skills
