from .models import Technology

def extract_techs_from_desc(lemmatized_desc):
    all_technologies = Technology.objects.all()
    
    found_technologies = []
    
    for tech in all_technologies:
        tech_name = tech.name.lower()
        if tech_name in lemmatized_desc:
            found_technologies.append(tech_name)
    
    return found_technologies