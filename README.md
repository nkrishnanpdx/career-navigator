A multi-agent job search and application assistant built using OpenAI's Agent SDK and agentic design principles.

This system automates job searching, resume tailoring, email submissions, and tracking, all powered by collaborating AI agents.

Agents

- Profile Analyzer: Extracts skills and preferences from your resume (PDF).

- Job Planner Agent: Plans targeted job search queries.

- Job Search Agent: (Mock up) Retrieves job descriptions based on search queries.

- Application Tailor Agent: Generates tailored resumes and cover letters.

- Email Agent: Sends job applications via email (SendGrid).

- Application Tracker Agent: Logs submissions in a local SQLite database.


Please edit agents/email_agent.py
- add TO_EMAIL and FROM_EMAIL 

Enter the actual api keys in .env
- You can just export with set in cmd too.

Dont forget to save you resume in /pwd/career-navigator/sample_resume.pdf





