from matching.utils import clean_job_offer, lemmatize_job_offer

class MatcherService:
    def __init__(self, user, job_description):
        self.user = user
        self.profile = user.profile
        self.job_offer = clean_job_offer(job_description)
        self.lemmatized_job_offer = lemmatize_job_offer(job_description)

    def match_technologies(self):
        ''' Matches user.profile.technologies with technologies from job offer'''
        pass    

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