import sys
import json
import os
from job_matcher import JobMatcher
from resume_builder import ResumeBuilder
try:
    from github_job_fetcher import fetch_github_jobs
except ImportError as e:
    print(f"CRITICAL ERROR: Could not import github_job_fetcher: {e}")
    input("Press Enter to exit...")
    sys.exit(1)
except SyntaxError as e:
    print(f"CRITICAL ERROR: Syntax error in github_job_fetcher: {e}")
    input("Press Enter to exit...")
    sys.exit(1)

# Sample User Profile (Current State: Freshman Ag/Bio Student)
USER_PROFILE = {
    "name": "Alex Student", # Placeholder
    "major": "Agricultural and Biological Engineering",
    "year": "Freshman",
    "visa": "F1",
    "keywords": [
        "Python", "Math", "Calculus", "Mobile App"
    ]
}

SAVED_JOBS_FILE = "saved_jobs.json"

def load_tech_jobs():
    """
    Simulates a database of TECH internships to analyze.
    """
    jobs = [
        {
            "id": 10,
            "title": "Microsoft Explore Intern (Rotational: PM & SWE)",
            "company": "Microsoft",
            "description": "12-week summer internship for 1st and 2nd-year students. Rotational program combining Software Engineering and Product Management. Required: Intro to CS, Calculus, and one programming language (Python/Java/C++).",
            "location": "Redmond, WA / Atlanta, GA"
        },
        {
            "id": 9,
            "title": "Meta University - Engineering (Internship)",
            "company": "Meta",
            "description": "8-10 week internship for first/second-year students. Focus on iOS, Android, or Web dev. Requirements: Current freshman or sophomore. Knowledge of at least one programming language (Python, Java, C++, etc.).",
            "location": "Menlo Park, CA / Remote"
        },
        {
            "id": 8,
            "title": "STEP Intern (Student Training in Engineering Program)",
            "company": "Google",
            "description": "12-week internship for first/second-year students. Required: Experience in one or more: Java, C++, Python. Completed at least one college-level CS course. Passion for technology.",
            "location": "Mountain View, CA / Remote"
        },
        {
            "id": 1,
            "title": "Software Engineering Intern - Summer 2026",
            "company": "TechGiant",
            "description": "Build scalable web applications. Required: Java or C++, Data Structures, Algorithms. AWS is a plus. Visa sponsorship available.",
            "location": "Seattle, WA"
        },
        {
            "id": 2,
            "title": "Mobile Engineering Intern",
            "company": "Appify",
            "description": "Develop iOS and Android apps. Experience with Mobile App development (Swift/Kotlin/React Native) required. Good understanding of UI/UX.",
            "location": "San Diego, CA"
        },
        {
            "id": 3,
            "title": "Data Science Intern",
            "company": "DataCorp",
            "description": "Analyze user behavior. Required: Python, SQL, Machine Learning basics, Pandas. Strong Math/Calculus background preferred. CPT/OPT friendly.",
            "location": "San Francisco, CA"
        },
        {
            "id": 4,
            "title": "Product Management Intern",
            "company": "StartupX",
            "description": "Work with engineering teams. Needs understanding of Agile, User Stories, and basic SQL.",
            "location": "Remote"
        },
        {
            "id": 5,
            "title": "Frontend Developer Intern",
            "company": "WebFlow Inc",
            "description": "Create beautiful UIs. Required: React, JavaScript, HTML/CSS. Design portfolio appreciated.",
            "location": "New York, NY"
        },
        {
            "id": 6,
            "title": "Systems Engineer Intern",
            "company": "AutoDrive",
            "description": "Embedded systems for autonomous vehicles. C++, Linux, RTOS. Citizenship required due to regulations.",
            "location": "Austin, TX"
        },
        {
            "id": 7,
            "title": "Cloud Infrastructure Intern",
            "company": "CloudNine",
            "description": "DevOps and Cloud focus. Python, Go, Docker, Kubernetes. Open to international students.",
            "location": "Boston, MA"
        }
    ]
    return jobs

def save_job(job):
    """
    Saves a job to a JSON file.
    """
    saved_jobs = []
    if os.path.exists(SAVED_JOBS_FILE):
        try:
            with open(SAVED_JOBS_FILE, 'r') as f:
                saved_jobs = json.load(f)
        except:
            pass
            
    # Check for duplicates
    for s in saved_jobs:
        if s.get('title') == job.get('title') and s.get('company') == job.get('company'):
            print("Job already saved.")
            return

    saved_jobs.append(job)
    with open(SAVED_JOBS_FILE, 'w') as f:
        json.dump(saved_jobs, f, indent=2)
    print("Job saved successfully!")

def view_saved_jobs():
    if not os.path.exists(SAVED_JOBS_FILE):
        print("No saved jobs yet.")
        return

    with open(SAVED_JOBS_FILE, 'r') as f:
        jobs = json.load(f)
        
    print(f"\n📂 Saved Jobs ({len(jobs)}):")
    for i, job in enumerate(jobs):
        print(f"{i+1}. {job.get('title')} @ {job.get('company', 'Unknown')}")
        print(f"   Score: {job.get('score', 'N/A')}")
        print("-" * 20)

def analyze_custom_text(matcher):
    print("\n📝 Paste the job description below (Press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    text = "\n".join(lines)
    
    if not text.strip():
        return

    analysis = matcher.analyze_text(text)
    
    print("\n🔍 Analysis Result:")
    print(f"Score: {analysis['score']}/100")
    print(f"Status: {analysis['status']}")
    print(f"Matched Skills: {', '.join(analysis['matched_skills'])}")
    print(f"Missing Skills: {', '.join(analysis['missing_skills'])}")
    
    save = input("\nSave this analysis? (y/n): ")
    if save.lower() == 'y':
        job_to_save = {
            "title": "Custom Job Analysis", 
            "company": "User Input", 
            "description": text[:100] + "..."
        }
        job_to_save.update(analysis)
        save_job(job_to_save)

def generate_resume_file():
    builder = ResumeBuilder(USER_PROFILE)
    content = builder.generate_resume()
    
    filename = "My_Resume_Draft.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"\n✅ Resume draft generated: {filename}")
    print("You can open this file in any text editor or Markdown viewer.")

def main():
    matcher = JobMatcher(USER_PROFILE)
    
    while True:
        print("\n🚀 US Job Search & Career Explorer")
        print("1. View & Analyze Mock Jobs")
        print("2. Analyze Custom Job Description (Paste Text)")
        print("3. Generate Resume Template")
        print("4. View Saved Jobs")
        print("5. Fetch Live Jobs from GitHub (Summer 2026) [NEW]")
        print("6. Exit")
        
        choice = input("\nSelect an option (1-6): ")
        
        if choice == '1':
            jobs = load_tech_jobs()
            results, _ = matcher.process_jobs(jobs)
            for i, row in enumerate(results):
                if row['score'] == 0: continue
                print(f"{i+1}. [{row['score']}%] {row['title']} @ {row['company']}")
                print(f"   Missing: {', '.join(row['missing_skills'])}")
            
            idx = input("\nEnter number to save a job (or Enter to skip): ")
            if idx.isdigit() and 0 < int(idx) <= len(results):
                save_job(results[int(idx)-1])
                
        elif choice == '2':
            analyze_custom_text(matcher)
            
        elif choice == '3':
            generate_resume_file()
            
        elif choice == '4':
            view_saved_jobs()
            
        elif choice == '5':
            try:
                gh_jobs = fetch_github_jobs()
                if gh_jobs:
                    print(f"\n[+] Successfully loaded {len(gh_jobs)} jobs from GitHub!")
                    # Process with our matcher
                    results, _ = matcher.process_jobs(gh_jobs)
                    
                    print(f"\n--- Top 20 Matches from Live Data (Total: {len(results)}) ---")
                    # Show top 20
                    display_limit = min(20, len(results))
                    for i in range(display_limit):
                        row = results[i]
                        # Safe print for Windows terminals
                        title = row['title'].encode('ascii', 'ignore').decode('ascii')
                        company = row['company'].encode('ascii', 'ignore').decode('ascii')
                        print(f"{i+1}. [{row['score']}%] {title} @ {company}")
                        print(f"   Location: {row['location'].encode('ascii', 'ignore').decode('ascii')}")
                        print(f"   Link: {row['url']}")
                        print("-" * 30)
                        
                    idx = input("\nEnter number to save a job (or Enter to skip): ")
                    if idx.isdigit() and 0 < int(idx) <= display_limit:
                        save_job(results[int(idx)-1])
                else:
                    print("No jobs found or connection failed.")
            except Exception as e:
                print(f"Error occurred: {e}")
                input("Press Enter to continue...")

        elif choice == '6':
            print("Good luck with your search!")
            sys.exit()
            
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
