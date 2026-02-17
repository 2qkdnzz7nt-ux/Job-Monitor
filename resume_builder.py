from datetime import datetime

class ResumeBuilder:
    def __init__(self, user_profile):
        self.profile = user_profile

    def generate_resume(self):
        """
        Generates a Markdown resume based on the user profile.
        """
        current_year = datetime.now().year
        grad_year = current_year + 3 # Freshman + 3 years
        
        # Template
        content = f"""# {self.profile.get('name', '[Your Name]')}
**Email:** [email@university.edu] | **Phone:** [555-555-5555] | **LinkedIn:** [linkedin.com/in/yourname]
**Location:** [City, State] | **Visa Status:** F-1 Student (CPT/OPT Eligible)

---

## 🎓 EDUCATION

**[University Name]** | [City, State]
*Bachelor of Science in {self.profile.get('major')}* | Expected May {grad_year}
*   **Relevant Coursework:** Calculus II, Introduction to Python (Planned), Engineering Fundamentals.
*   **Activities:** [Club Name], [Society of Asian Scientists and Engineers / ASABE Member].

---

## 💻 SKILLS

*   **Programming:** Python (Basic), Mobile App Development.
*   **Mathematics:** Calculus I & II, Statistics (Planned).
*   **Tools:** [VS Code], [Git/GitHub - *Recommended to learn*], [Microsoft Office].
*   **Languages:** English (Proficient), [Native Language].

---

## 🚀 PROJECTS

**Mobile Application Project** | *High School Capstone* | [Date]
*   Designed and developed a mobile application using [Tool/Language, e.g., MIT App Inventor / Swift].
*   Implemented features such as [Feature 1] and [Feature 2] to solve [Problem].
*   Conducted user testing with [Number] peers to iterate on UI/UX design.

**Coursework Python Projects** | *[High School / University]* | [Date]
*   Created scripts to automate [Task] using Python.
*   Analyzed data sets related to [Topic] using basic data processing techniques.

---

## 🏆 EXPERIENCE (Optional)

**[Position Title]** | *[Organization/Company]* | [Dates]
*   [Action Verb] [Task] resulting in [Result].
*   Collaborated with a team of [Number] to achieve [Goal].

---
"""
        return content

if __name__ == "__main__":
    print("Resume Builder Module Loaded.")
