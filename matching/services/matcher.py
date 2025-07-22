from matching.utils import lemmatize_text, match_action_verbs, match_soft_skills, match_relevant_phrases
from sklearn.metrics.pairwise import cosine_similarity
from technologies.utils import extract_techs_from_desc
from technologies.models import Technology
from profiles.utils import build_user_profile_text, lemmatize_profile_career_item
from .model_singleton import model_singleton, EmbeddingCache

class MatcherService:
    def __init__(self, user, job_description):
        self.user = user
        self.profile = user.profile
        self.job_description = job_description
        self.lemmatized_job_offer = lemmatize_text(job_description)
        
        # Singleton
        self.model = model_singleton.get_sentence_transformer('all-MiniLM-L6-v2')
        self.kw_model = model_singleton.get_keybert_model('all-MiniLM-L6-v2')

        # Cache technologies
        self._all_technologies = None 
    def get_all_technologies(self):
        if self._all_technologies is None:
            self._all_technologies = set(Technology.objects.values_list('name', flat=True))
        return self._all_technologies

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
            self.technology_match_results = {
                'matched_technologies': [],
                'missing_technologies': [],
                'match_score': 0.0,
                'details': []
            }
            return self.technology_match_results
        
        job_technologies = extract_techs_from_desc(self.lemmatized_job_offer)
        
        if not job_technologies:
            self.technology_match_results = {
                'matched_technologies': [],
                'missing_technologies': user_technologies,
                'match_score': 0.0,
                'details': []
            }
            return self.technology_match_results
        
        # Cache embeddings
        user_embeddings = EmbeddingCache.get_or_compute_batch(user_technologies, self.model)
        job_embeddings = EmbeddingCache.get_or_compute_batch(job_technologies, self.model)
        if len(user_embeddings) == 0 or len(job_embeddings) == 0:
            self.technology_match_results = {
                'matched_technologies': [],
                'missing_technologies': job_technologies,
                'match_score': 0.0,
                'details': []
            }
            return self.technology_match_results
        
        similarity_matrix = cosine_similarity(user_embeddings, job_embeddings)
        
        threshold = 0.65  # Reducido para permitir más matches válidos
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

    def match_keywords(self):
        '''
        Match keywords from the job description with the user profile. Returns matched and missing keywords:
        - Verbs. 
        - Soft skills.
        - Phrases.
        '''
        try:
            user_text = build_user_profile_text(self.profile)
        except Exception as e:
            user_text = ""
            if hasattr(self.profile, 'bio') and self.profile.bio:
                user_text = self.profile.bio
        
        try:
            matched_action_verbs, missing_action_verbs = match_action_verbs(self.job_description, user_text, self.model)
        except Exception as e:
            matched_action_verbs, missing_action_verbs = [], []
        
        try:
            matched_soft_skills, missing_soft_skills = match_soft_skills(self.job_description, user_text, self.model)
        except Exception as e:
            matched_soft_skills, missing_soft_skills = [], []
            
        try:
            matched_phrases, missing_phrases = match_relevant_phrases(self.job_description, user_text, self.model)
        except Exception as e:
            matched_phrases, missing_phrases = [], []
        
        matched_action_verbs_terms = [item['job_term'] if isinstance(item, dict) else item for item in matched_action_verbs]
        missing_action_verbs_terms = [item if isinstance(item, str) else str(item) for item in missing_action_verbs]
        matched_soft_skills_terms = [item['job_term'] if isinstance(item, dict) else item for item in matched_soft_skills]
        missing_soft_skills_terms = [item if isinstance(item, str) else str(item) for item in missing_soft_skills]
        matched_phrases_terms = [item['job_term'] if isinstance(item, dict) else item for item in matched_phrases]
        missing_phrases_terms = [item if isinstance(item, str) else str(item) for item in missing_phrases]
        
        self.keyword_match_results = {
            'matched_keywords': {
                'action_verbs': {
                    'items': matched_action_verbs_terms,
                    'count': len(matched_action_verbs_terms),
                    'description': 'Verbos de acción que tienes en tu perfil y coinciden con la oferta'
                },
                'soft_skills': {
                    'items': matched_soft_skills_terms,
                    'count': len(matched_soft_skills_terms),
                    'description': 'Habilidades blandas que tienes y son requeridas'
                },
                'phrases': {
                    'items': matched_phrases_terms,
                    'count': len(matched_phrases_terms), 
                    'description': 'Frases relevantes que aparecen en tu perfil y en la oferta'
                }
            },
            'missing_keywords': {
                'action_verbs': {
                    'items': missing_action_verbs_terms,
                    'count': len(missing_action_verbs_terms),
                    'description': 'Verbos de acción que aparecen en la oferta pero no en tu perfil'
                },
                'soft_skills': {
                    'items': missing_soft_skills_terms,
                    'count': len(missing_soft_skills_terms),
                    'description': 'Habilidades blandas requeridas que no tienes destacadas'
                },
                'phrases': {
                    'items': missing_phrases_terms,
                    'count': len(missing_phrases_terms),
                    'description': 'Frases relevantes de la oferta que podrías incorporar'
                }
            }
        }
        
        total_matched = sum(cat['count'] for cat in self.keyword_match_results['matched_keywords'].values())
        total_missing = sum(cat['count'] for cat in self.keyword_match_results['missing_keywords'].values())
        total_analyzed = total_matched + total_missing
        
        match_score = (total_matched / total_analyzed * 100) if total_analyzed > 0 else 0.0
        self.keyword_match_results['match_score'] = match_score
        
        self.keyword_match_results['details'] = {
            'matched_items': [item for cat in self.keyword_match_results['matched_keywords'].values() for item in cat['items']],
            'missing_items': [item for cat in self.keyword_match_results['missing_keywords'].values() for item in cat['items']],
            'total_matched': total_matched,
            'total_missing': total_missing,
            'total_analyzed': total_analyzed
        }
        
        return self.keyword_match_results

    def related_career_items(self):
        ''' 
        Ranks user's work experiences by relevance to the job offer.
        - Uses semantic similarity to score complete work experiences against job requirements.
        - Returns ranked experiences with relevance scores and matched concepts.
        - Focus on: work experience only.
        '''        
        experiences = self.profile.career_items.select_related().filter(item_type='experience')
        
        if not experiences:
            self.career_items_results = {
                'ranked_career_items': [],
                'relevance_scores': [],
                'details': []
            }
            return self.career_items_results
        
        career_item_texts = []
        career_item_details = []        
        
        for item in experiences:
            try:
                lemmatized_item = lemmatize_profile_career_item(item)
                
                title_tokens = lemmatized_item.get('title', []) or []
                desc_tokens = lemmatized_item.get('description', []) or []
                
                all_tokens = title_tokens + desc_tokens
                item_text = ' '.join(all_tokens).strip()
                
                if item_text: 
                    career_item_texts.append(item_text)
                    career_item_details.append({
                        'career_item': item,
                        'text': item_text,
                        'type': item.item_type,
                        'title_tokens': title_tokens,
                        'desc_tokens': desc_tokens
                    })
            except Exception as e:
                continue
        
        if not career_item_texts:
            self.career_items_results = {
                'ranked_career_items': [],
                'relevance_scores': [],
                'details': []
            }
            return self.career_items_results

        try:
            job_embedding = EmbeddingCache.get_or_compute(self.lemmatized_job_offer, self.model)
            career_embeddings = EmbeddingCache.get_or_compute_batch(career_item_texts, self.model)
            
            if len(career_embeddings) == 0:
                self.career_items_results = {
                    'ranked_career_items': [],
                    'relevance_scores': [],
                    'details': []
                }
                return self.career_items_results
            
            similarities = cosine_similarity([job_embedding], career_embeddings)[0]
            
            ranked_results = []
            for i, (similarity_score, detail) in enumerate(zip(similarities, career_item_details)):
                ranked_results.append({
                    'career_item': detail['career_item'],
                    'relevance_score': float(similarity_score),
                    'type': detail['type'],
                    'title': detail['career_item'].title,
                    'description': detail['career_item'].description or '',
                    'institution': detail['career_item'].institution or 'Independiente',
                    'start_date': detail['career_item'].start_date,
                    'end_date': detail['career_item'].end_date,
                    'processed_text': detail['text'],
                    'title_tokens': detail['title_tokens'],
                    'desc_tokens': detail['desc_tokens']
                })
            
            ranked_results.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            ranked_career_items = [result['career_item'] for result in ranked_results]
            relevance_scores = [result['relevance_score'] for result in ranked_results]
            
            self.career_items_results = {
                'ranked_career_items': ranked_career_items,
                'relevance_scores': relevance_scores,
                'details': ranked_results
            }
            
        except Exception as e:
            self.career_items_results = {
                'ranked_career_items': [detail['career_item'] for detail in career_item_details],
                'relevance_scores': [0.5] * len(career_item_details),  # Default medium score
                'details': [{
                    'career_item': detail['career_item'],
                    'relevance_score': 0.5,
                    'type': detail['type'],
                    'title': detail['career_item'].title,
                    'description': detail['career_item'].description or '',
                    'institution': detail['career_item'].institution or 'Independiente',
                    'start_date': detail['career_item'].start_date,
                    'end_date': detail['career_item'].end_date,
                    'processed_text': detail['text'],
                    'title_tokens': detail['title_tokens'],
                    'desc_tokens': detail['desc_tokens']
                } for detail in career_item_details]
            }
        
        return self.career_items_results

    def score_match(self):
        ''' Returns a score based on the match between user profile and job offer '''
        TECH = 0.40     
        KEYWORDS = 0.35  
        CAREER = 0.25   
        
        tech_results = getattr(self, 'technology_match_results', {})
        tech_matched = len(tech_results.get('matched_technologies', []))
        tech_missing = len(tech_results.get('missing_technologies', []))
        tech_user_total = len([tech.name for tech in self.profile.technologies.all()])
        
        if tech_user_total > 0 and (tech_matched + tech_missing) > 0:
            coverage_score = (tech_matched / (tech_matched + tech_missing)) * 100 
            user_score = (tech_matched / tech_user_total) * 100  
            tech_score = (coverage_score * 0.7 + user_score * 0.3)  
        else:
            tech_score = 0.0
        
        keywords_score = getattr(self, 'keyword_match_results', {}).get('match_score', 0.0)
        
        career_results = getattr(self, 'career_items_results', {})
        career_scores = career_results.get('relevance_scores', [])
        if career_scores:
            top_career_scores = sorted(career_scores, reverse=True)[:3]
            boosted_scores = [min(100, (score * 100) + 15) for score in top_career_scores]
            career_score = sum(boosted_scores) / len(boosted_scores)
        else:
            career_score = 20.0
        
        final_score = (
            tech_score * TECH +
            keywords_score * KEYWORDS +
            career_score * CAREER 
        )
        final_score = max(0.0, min(100.0, final_score))

        return round(final_score)

    def match(self):
        ''' Main method to execute the matching process '''
        self.match_technologies()
        self.match_keywords()
        self.related_career_items()  
        return self.score_match()
