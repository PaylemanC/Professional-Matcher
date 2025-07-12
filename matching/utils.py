import re # Pattern: [^a-z0-9\s] -> Letters, numbers and spaces
import unicodedata
import spacy

nlp = spacy.load("es_core_news_sm")  

def clean_job_offer(job_offer):
    job_offer = unicodedata.normalize('NFKD', job_offer).encode('ascii', 'ignore').decode('utf-8')

    job_offer = job_offer.lower()

    job_offer = re.sub(r'[^a-z0-9\s]', '', job_offer)

    job_offer_doc = nlp(job_offer)
    job_offer = ' '.join([word.text for word in job_offer_doc 
                          if not word.is_stop])  

    return job_offer

print(clean_job_offer("Software Engineer - Python & Django - Oferta de Trabajo increíble...!"))
