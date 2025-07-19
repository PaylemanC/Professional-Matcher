import spacy
from matching.utils import clean_text

nlp = spacy.load("es_core_news_sm")  

def clean_profile_career_item(career_item):
    if not career_item:
        return {"title": "", "description": ""}
    
    title = clean_text(career_item.title, with_stop_words=True)
    
    description = ""
    if career_item.description:
        description = clean_text(career_item.description, with_stop_words=True)
    
    return {
        "title": title,
        "description": description
    }

def lemmatize_profile_career_item(career_item):
    cleaned = clean_profile_career_item(career_item)

    lemmatized_title = []
    lemmatized_description = []

    if cleaned["title"]:
        title_doc = nlp(cleaned["title"])
        lemmatized_title = [token.lemma_ for token in title_doc if token.lemma_.strip()]

    if cleaned["description"]:
        description_doc = nlp(cleaned["description"])
        lemmatized_description = [token.lemma_ for token in description_doc if token.lemma_.strip()]

    return {
        "title": lemmatized_title,
        "description": lemmatized_description
    }

def build_user_profile_text(profile):
    profile_parts = []
    
    if profile.bio:
        cleaned_bio = clean_text(profile.bio, with_stop_words=True)
        if cleaned_bio:  
            profile_parts.append(cleaned_bio)
    
    career_items = profile.career_items.all()
    for item in career_items:
        cleaned_item = clean_profile_career_item(item)
        
        if cleaned_item['title']:
            profile_parts.append(cleaned_item['title'])
        
        if cleaned_item['description']:
            profile_parts.append(cleaned_item['description'])
    
    return ' '.join(profile_parts)
