# Overview
The Intelligent Career Navigator is an AI-powered application designed to streamline and enhance the job application process. From analyzing your resume and planning targeted job searches to tailoring applications and providing interview preparation, this tool aims to be your comprehensive assistant in navigating the competitive job market.

It leverages advanced AI agents to automate tedious tasks, allowing you to focus on refining your skills and acing your interviews.
# Features
- Resume Analysis: Extracts key skills, industries, roles, and tone from your uploaded PDF resume.
- Intelligent Job Search Planning: Generates strategic job search queries based on your profile and career preferences.
- Real-time Job Search (Mocked): Simulates searching for real, active job postings from popular platforms (e.g., LinkedIn, Indeed, Google Jobs) using a cached system. (Note: Currently uses mocked results for demonstration; can be extended for live search.)
- Automated Application Tailoring: Generates a personalized resume and a concise cover letter for specific job descriptions, highlighting your most relevant experiences and skills.
- Editable Application Drafts: Provides an option to review and manually tweak the AI-generated tailored resume and cover letter before sending.
- Automated Email Application: Sends tailored applications directly via email using SendGrid.
- Application Tracking: Logs all your applied jobs in a local SQLite database for easy tracking and management.
- Interview Preparation Guidance: Offers AI-powered advice for coding, system design, and behavioral interview rounds tailored to specific job titles.
- User-Friendly Interface: Built with Streamlit for an intuitive and interactive user experience.
# Getting Started
Follow these instructions to set up and run the Intelligent Career Navigator on your local machine.

## Prerequisites
Before you begin, ensure you have the following installed: 
```
Python 3.8+
pip (Python package installer, usually comes with Python)
```
## Installation
Clone the Repository:
```
git clone https://github.com/nkrishnanpdx/career-navigator.git
cd career-navigator
```
Create a Virtual Environment (Recommended):
```
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```
Install Dependencies:
```
pip install -r requirements.txt
```
##
API Key Configuration
The application requires API keys for AI model interaction and email sending. Set these as environment variables:

###  OpenAI API Key: For gpt-4o-mini and other OpenAI models.
- Windows (Command Prompt): set OPENAI_API_KEY="your_openai_api_key"
- macOS/Linux (Bash/Zsh): export OPENAI_API_KEY="your_openai_api_key"

### SendGrid API Key: For sending application emails.
- Windows (Command Prompt): set SENDGRID_API_KEY="your_sendgrid_api_key"
- macOS/Linux (Bash/Zsh): export SENDGRID_API_KEY="your_sendgrid_api_key"
Important: Also, update the FROM_EMAIL and TO_EMAIL placeholders in agents/email_agent.py to your desired email addresses.

## Prepare Sample Resume
Place a PDF file named sample_resume.pdf in the root directory of the career-navigator project. This will be the resume you upload and use for analysis.

# Usage
Run the Streamlit Application:
```
streamlit run app.py
```
Your browser should automatically open to the application (usually at http://localhost:8501).

- Upload Your Resume: Use the sidebar to upload your sample_resume.pdf.
- Run Career Navigator: Click the "🔍 Run Career Navigator" button.
  - The app will analyze your resume and propose job search queries.
  -  It will then perform a mocked job search and display the "Found Job Listings".
- Generate & Edit Application Draft:
  - Select a job from the "Found Job Listings" dropdown.
  - Click "Generate Draft for Editing". The app will generate a tailored resume and cover letter.
  - You can then review and edit these drafts in the provided text areas.
- Send Application:
  -  After editing, click the "🚀 Send Application" button. The tailored application will be emailed, and the application will be logged.
- Prepare for Interviews:
  -  In the "Prep for Interviews" section, enter a job title.
  - Click "Generate Interview Prep" to receive AI-powered guidance for coding, system design, and behavioral rounds.

