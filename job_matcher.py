import datetime

class JobMatcher:
    def __init__(self, user_profile):
        """
        Initialize with user profile (skills, major, visa_status)
        """
        self.user_profile = user_profile
        
    def analyze_text(self, text):
        """
        Analyze raw job description text.
        """
        # Create a dummy job object
        dummy_job = {
            "title": "Custom Job Analysis",
            "description": text
        }
        return self.analyze_job(dummy_job)

    def analyze_job(self, job):
        """
        Analyze a job to identify required skills and potential match.
        Returns a dict with score, matched_skills, and missing_skills.
        """
        score = 0
        description = job.get('description', '').lower()
        title = job.get('title', '').lower()
        
        # 1. Visa Check (Binary Filter)
        negatives = ["us citizen", "u.s. citizen", "citizenship required", "clearance"]
        for neg in negatives:
            if neg in description:
                return {"score": 0, "status": "Ineligible (Visa)", "matched_skills": [], "missing_skills": []}
        
        # 2. Skill Analysis
        # We check against ALL known tech skills, not just what the user has.
        # This helps identifying what to learn.
        
        # Define skill categories for analysis
        tech_skills = {
            "Languages": ["python", "java", "c++", "javascript", "sql", "html/css", "go", "rust", "swift", "kotlin"],
            "Frameworks": ["react", "node", "django", "flask", "spring", "aws", "docker", "kubernetes", "flutter", "react native"],
            "Concepts": ["machine learning", "data structures", "algorithms", "rest api", "system design", "agile", "mobile app", "calculus"]
        }
        
        found_skills = []
        user_skills = [k.lower() for k in self.user_profile.get('keywords', [])]
        
        matched_user_skills = []
        missing_market_skills = []
        
        for category, skills in tech_skills.items():
            for skill in skills:
                if skill in description or skill in title:
                    found_skills.append(skill)
                    if skill in user_skills:
                        matched_user_skills.append(skill)
                        score += 10
                    else:
                        missing_market_skills.append(skill)
                        score += 2 # Still give points for relevance to target field
        
        # 3. Role Relevance (Tech Focus)
        target_roles = ["software", "developer", "engineer", "data", "product", "analyst"]
        is_tech_role = False
        for role in target_roles:
            if role in title:
                score += 20
                is_tech_role = True
        
        if not is_tech_role:
            score -= 10
            
        # 4. Experience Level (Freshman friendly)
        entry_level = ["intern", "internship", "co-op", "student", "entry level"]
        for level in entry_level:
            if level in title or level in description:
                score += 15
        
        return {
            "score": min(score, 100),
            "status": "Match" if score > 40 else "Low Match",
            "matched_skills": matched_user_skills,
            "missing_skills": missing_market_skills,
            "all_required_skills": found_skills
        }

    def process_jobs(self, jobs_list):
        """
        Takes a list of job dictionaries and adds analysis data.
        """
        processed_jobs = []
        skill_frequency = {}
        
        for job in jobs_list:
            analysis = self.analyze_job(job)
            job.update(analysis)
            processed_jobs.append(job)
            
            # Count skill frequency for recommendation
            for skill in analysis['missing_skills']:
                skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
                
        # Sort by score descending
        sorted_jobs = sorted(processed_jobs, key=lambda x: x['score'], reverse=True)
        
        return sorted_jobs, skill_frequency

if __name__ == "__main__":
    # Test Logic
    print("Job Matcher Module Loaded.")
