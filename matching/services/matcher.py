from matching.utils import clean_job_offer, lemmatize_job_offer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from technologies.utils import extract_techs_from_desc

class MatcherService:
    def __init__(self, user, job_description):
        self.user = user
        self.profile = user.profile
        self.job_offer = clean_job_offer(job_description)

        self.model = SentenceTransformer('all-mpnet-base-v2')
        self.lemmatized_job_offer = lemmatize_job_offer(job_description)

    def match_technologies(self):
        ''' 
        Matches user.profile.technologies with technologies from job offer

        Returns self.technology_match_results: {
            'matched_technologies': List of user technologies that match with job offer
            'missing_technologies': List of job offer technologies that user doesn't have
            'match_score': Percentage score of user technologies that matched
            'details': List of dictionaries with details of each match
        }

        '''
        user_technologies = [tech.name for tech in self.profile.technologies.all()]
        
        if not user_technologies:
            return {
                'matched_technologies': [],
                'missing_technologies': [],
                'match_score': 0.0,
                'details': []
            }
        
        job_technologies = extract_techs_from_desc(self.lemmatized_job_offer)
        
        if not job_technologies:
            return {
                'matched_technologies': [],
                'missing_technologies': user_technologies,
                'match_score': 0.0,
                'details': []
            }
        
        user_embeddings = self.model.encode(user_technologies)
        job_embeddings = self.model.encode(job_technologies)
        
        similarity_matrix = cosine_similarity(user_embeddings, job_embeddings)
        
        threshold = 0.8        
        match_details = []        
        matched_technologies = []
        matched_job_technologies = []         
        for i, user_tech in enumerate(user_technologies):
            best_match_idx = similarity_matrix[i].argmax()
            best_similarity = similarity_matrix[i][best_match_idx]
            
            if best_similarity >= threshold:
                matched_tech = job_technologies[best_match_idx]
                matched_technologies.append(user_tech)
                matched_job_technologies.append(matched_tech)
                match_details.append({
                    'user_technology': user_tech,
                    'job_technology': matched_tech,
                    'similarity_score': float(best_similarity)
                })
        
        missing_technologies = [tech for tech in job_technologies 
                               if tech not in matched_job_technologies]
 
        match_score = (len(matched_technologies) / len(user_technologies) * 100) if user_technologies else 0.0
        
        self.technology_match_results = {
            'matched_technologies': matched_technologies,
            'missing_technologies': missing_technologies,
            'match_score': match_score,
            'details': match_details
        }
        
        return self.technology_match_results    

    def highlight_keywords(self):
        ''' Extracts keywords from the job offer based on user profile. Classifies them as 'matched' and 'missing' '''
        pass    

    def related_career_items(self):
        ''' Search related career items based on the job offer '''
        pass

    def suggest_missing_elements(self):
        ''' Suggests action verbs, metrics, or phrases that appear in the job offer but are not present in the profile '''
        pass

    def score_match(self):
        ''' Returns a score based on the match between user profile and job offer '''
        pass

    def match(self):
        ''' Main method to execute the matching process '''
        self.match_technologies()
        self.highlight_keywords()
        self.related_career_items()
        self.suggest_missing_elements()
        return self.score_match()