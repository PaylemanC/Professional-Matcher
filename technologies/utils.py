from .models import Technology

def extract_techs_from_desc(lemmatized_desc):
    all_technologies = Technology.objects.all()

    text_string = ' '.join(lemmatized_desc)
    
    found_technologies = []
    
    for tech in all_technologies:
        tech_name = tech.name.lower()
        if tech_name in text_string:
            found_technologies.append(tech_name)
    
    return found_technologies