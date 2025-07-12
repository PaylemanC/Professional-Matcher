import re # Pattern: [^a-z0-9\s] -> Letters, numbers and spaces
import unicodedata

def clean_job_offer(job_offer):
    job_offer = unicodedata.normalize('NFKD', job_offer).encode('ascii', 'ignore').decode('utf-8')

    job_offer = job_offer.lower()

    job_offer = re.sub(r'[^a-z0-9\s]', '', job_offer)

    return job_offer

example = clean_job_offer("Software Engineer - Python & Django - Oferta de Trabajo!")  
print(example)