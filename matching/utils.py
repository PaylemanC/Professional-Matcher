import re # Pattern:  r'[^a-z0-9\s]' -> Letters, numbers and spaces
import unicodedata
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from matching.constants import COMMON_ACTION_VERBS, COMMON_SOFT_SKILLS, SOFT_SKILL_PATTERNS, RELEVANT_PHRASE_PATTERNS

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

def match_action_verbs(job_text, user_profile_text, model):
    if not job_text or not user_profile_text:
        return [], []
    
    job_verbs = find_action_verbs(job_text)
    user_verbs = find_action_verbs(user_profile_text)
    
    if not job_verbs:
        return [], []
    
    matched_verbs = []
    missing_verbs = []
    
    for job_verb in job_verbs:
        if job_verb in COMMON_ACTION_VERBS and job_verb in user_verbs:
            matched_verbs.append({
                'job_term': job_verb,
                'user_term': job_verb,
                'similarity_score': 1.0
            })
        elif job_verb in COMMON_ACTION_VERBS:
            best_match = None
            best_score = 0.0
            
            for user_verb in user_verbs:
                if user_verb in COMMON_ACTION_VERBS:
                    if len(set(job_verb) & set(user_verb)) >= 3:  
                        score = len(set(job_verb) & set(user_verb)) / max(len(job_verb), len(user_verb))
                        if score > best_score and score > 0.5:
                            best_score = score
                            best_match = user_verb
            
            if best_match:
                matched_verbs.append({
                    'job_term': job_verb,
                    'user_term': best_match,
                    'similarity_score': best_score
                })
            else:
                missing_verbs.append(job_verb)
        else:
            continue
    
    return matched_verbs, missing_verbs

def match_soft_skills(job_text, user_profile_text, model):
    if not job_text or not user_profile_text:
        return [], []
    job_clean = clean_text(job_text, with_stop_words=True)
    user_clean = clean_text(user_profile_text, with_stop_words=True)
    
    job_skills_found = []
    user_skills_found = []
    
    for skill in COMMON_SOFT_SKILLS:
        if skill.lower() in job_clean.lower():
            job_skills_found.append(skill)
        if skill.lower() in user_clean.lower():
            user_skills_found.append(skill)
    
    for pattern in SOFT_SKILL_PATTERNS:
        job_matches = re.findall(pattern, job_clean, re.IGNORECASE)
        user_matches = re.findall(pattern, user_clean, re.IGNORECASE)
        
        for match in job_matches:
            if isinstance(match, tuple):
                match = ' '.join(filter(None, match))
            if match and match not in job_skills_found:
                job_skills_found.append(match.strip())
        
        for match in user_matches:
            if isinstance(match, tuple):
                match = ' '.join(filter(None, match))
            if match and match not in user_skills_found:
                user_skills_found.append(match.strip())
    
    if not job_skills_found:
        return [], []
    
    matched_skills = []
    missing_skills = []    
    for job_skill in job_skills_found:
        if job_skill in user_skills_found:
            matched_skills.append({
                'job_term': job_skill,
                'user_term': job_skill,
                'similarity_score': 1.0
            })
        else:
            missing_skills.append(job_skill)
    
    return matched_skills, missing_skills

def match_relevant_phrases(job_text, user_profile_text, model):
    if not job_text or not user_profile_text:
        return [], []
    
    job_clean = clean_text(job_text, with_stop_words=True)
    user_clean = clean_text(user_profile_text, with_stop_words=True)
    
    job_phrases_found = []
    user_phrases_found = []
    
    for pattern in RELEVANT_PHRASE_PATTERNS:
        job_matches = re.findall(pattern, job_clean, re.IGNORECASE)
        user_matches = re.findall(pattern, user_clean, re.IGNORECASE)
        
        for match in job_matches:
            if isinstance(match, tuple):
                match = ' '.join(filter(None, match))
            if match and match not in job_phrases_found:
                job_phrases_found.append(match.strip())
        
        for match in user_matches:
            if isinstance(match, tuple):
                match = ' '.join(filter(None, match))
            if match and match not in user_phrases_found:
                user_phrases_found.append(match.strip())
    
    if not job_phrases_found:
        return [], []
    
    matched_phrases = []
    missing_phrases = []    
    for job_phrase in job_phrases_found:
        if job_phrase.lower() in user_clean.lower():
            matched_phrases.append({
                'job_term': job_phrase,
                'user_term': job_phrase,
                'similarity_score': 1.0
            })
        else:
            missing_phrases.append(job_phrase)
    
    return matched_phrases, missing_phrases
