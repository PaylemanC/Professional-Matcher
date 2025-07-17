import re # Pattern:  r'[^a-z0-9\s]' -> Letters, numbers and spaces
import unicodedata
import spacy

nlp = spacy.load("es_core_news_sm")  

def clean_text(text: str, pattern=None):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = text.lower()
    if pattern:
        text = re.sub(pattern, '', text)
    text_doc = nlp(text)
    text = ' '.join([word.text for word in text_doc 
                    if not word.is_stop])
    
    return text

def lemmatize_text(text: str, pattern=None) -> list:
    text = clean_text(text, pattern)

    text_doc = nlp(text)
    lemmatized_words = [word.lemma_ for word in text_doc if word.lemma_.strip()]

    return lemmatized_words

def find_keyword(keyword: str, text_sources: dict) -> list:
    if not keyword or not text_sources:
        return []
    
    keyword_lower = keyword.lower()
    found_in = []
    
    for source_id, text in text_sources.items():
        if text and keyword_lower in text.lower():
            found_in.append(source_id)
    
    return found_in

print(clean_text("Software Engineer - Python & Django - Oferta de Trabajo increíble...!", r'[^a-z0-9\s]'))
print(lemmatize_text("Software Engineer - Python & Django - Oferta de Trabajo increíble...!", r'[^a-z0-9\s]'))
print(find_keyword("Python", {"profile": "Python Developer", "job_offer": "Looking for an expert"}))
