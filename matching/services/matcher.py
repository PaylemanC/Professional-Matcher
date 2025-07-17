from matching.utils import clean_text, lemmatize_text
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
from sklearn.metrics.pairwise import cosine_similarity
from technologies.utils import extract_techs_from_desc
from profiles.utils import build_user_profile_text, find_keyword_in_profile

class MatcherService:
    def __init__(self, user, job_description):
        self.user = user
        self.profile = user.profile
        self.job_offer = clean_text(job_description, r'[^a-z0-9\s]')

        self.lemmatized_job_offer = lemmatize_text(job_description, r'[^a-z0-9\s]')

        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # all-mpnet-base-v2
        self.kw_model = KeyBERT(model=self.model)

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
        
        threshold = 0.75    
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
        '''
        Extracts and matches non-technical keywords from job offer against user profile (user.profile.bio and career_items descriptions/titles).
        - Returns matched and missing keywords with their sources.
        - Focus on: soft skills, methodologies, certifications, etc. 
        '''
        job_text = ' '.join(self.lemmatized_job_offer)
        job_keywords_with_scores = self.kw_model.extract_keywords(
            job_text, 
            keyphrase_ngram_range=(1, 2),  
            stop_words=None,  
            top_n=10, 
            use_maxsum=True,  
            nr_candidates=20  
        )        
        job_keywords_list = [keyword[0] for keyword in job_keywords_with_scores]
        
        user_profile_text = build_user_profile_text(self.profile)
        if not user_profile_text:
            return {
                'matched_keywords': [],
                'missing_keywords': job_keywords_list,
                'match_score': 0.0,
                'details': []
            }
        
        job_embeddings = self.model.encode(job_keywords_list)
        
        user_keywords = self.kw_model.extract_keywords(
            user_profile_text,
            keyphrase_ngram_range=(1, 2),
            stop_words=None,  
            top_n=12,  
            use_maxsum=True,
            nr_candidates=20  
        )        

        user_keywords_terms = [keyword[0] for keyword in user_keywords]
        if not user_keywords_terms:
            return {
                'matched_keywords': [],
                'missing_keywords': job_keywords_list,
                'match_score': 0.0,
                'details': []
            }
        
        user_embeddings = self.model.encode(user_keywords_terms)
        
        similarity_matrix = cosine_similarity(job_embeddings, user_embeddings)

        threshold = 0.70           
        matched_keywords = []
        missing_keywords = []
        match_details = []        
        for i, job_keyword in enumerate(job_keywords_list):
            best_match_idx = similarity_matrix[i].argmax()
            best_similarity = similarity_matrix[i][best_match_idx]
            
            if best_similarity >= threshold:
                matched_user_keyword = user_keywords_terms[best_match_idx]
                matched_keywords.append(job_keyword)

                sources = find_keyword_in_profile(matched_user_keyword, self.profile)
                primary_source = sources[0] if sources else 'unknown'
                
                match_details.append({
                    'job_keyword': job_keyword,
                    'user_keyword': matched_user_keyword,
                    'similarity_score': float(best_similarity),
                    'source': primary_source,
                    'all_sources': sources  
                })
            else:
                missing_keywords.append(job_keyword)
        
        match_score = (len(matched_keywords) / len(job_keywords_list) * 100) if job_keywords_list else 0.0
        
        self.keyword_match_results = {
            'matched_keywords': matched_keywords,
            'missing_keywords': missing_keywords,
            'match_score': match_score,
            'details': match_details
        }
        
        return self.keyword_match_results

    def related_career_items(self):
        ''' 
        Ranks user's career items by relevance to the job offer.
        - Uses semantic similarity to score complete career experiences against job requirements.
        - Returns ranked career items with relevance scores and matched concepts.
        - Focus on: contextual experience matching, complete work history
        '''
        experiences = self.profile.career_items.filter(item_type='experience')
        education = self.profile.career_items.filter(item_type='education')

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