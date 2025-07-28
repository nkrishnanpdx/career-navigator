import sqlite3
import hashlib
import json
import os
import re
from simple_agents import Agent, Runner

DB_PATH = "data/job_cache.sqlite"

def initialize_cache():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_cache (
            query TEXT PRIMARY KEY,
            results TEXT
        )
    """)
    conn.commit()
    conn.close()

def cache_results(query: str, results: list):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO job_cache (query, results) VALUES (?, ?)", (query, json.dumps(results)))
    conn.commit()
    conn.close()

def get_cached_results(query: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT results FROM job_cache WHERE query = ?", (query,))
    row = cursor.fetchone()
    conn.close()
    return json.loads(row[0]) if row else None

class RealJobSearchAgent:
    def __init__(self):
        initialize_cache()

        # Instructions for the agent to interpret search results and format output
        self.instructions = """
        You are a job search assistant. You have been provided with web search results for a job query.
        Your task is to extract relevant job postings from these results, focusing on LinkedIn, Indeed, Google Jobs, or similar reputable sources.
        For each job, identify its title, company, location, and a direct URL to the posting.

        Finally, return a list of jobs as a JSON array. Each object in the array MUST have the fields: "title", "company", "location", and "url".
        If no relevant jobs are found in the provided search results, return an empty JSON array: [].

        Example of expected JSON output:
        [
            {"title": "Senior Software Engineer", "company": "Acme Corp", "location": "Remote", "url": "https://linkedin.com/jobs/123"},
            {"title": "Data Analyst", "company": "DataCo", "location": "New York, NY", "url": "https://indeed.com/jobs/456"}
        ]
        """
        self.agent = Agent(
            name="RealJobSearch",
            instructions=self.instructions,
            model="gpt-4o-mini", 
        )

    async def search(self, query: str) -> list:
        # Check local cache first
        cached = get_cached_results(query)
        if cached:
            print(f"DEBUG: Returning cached results for query: '{query}'")
            return cached

        # --- MOCKED WEB SEARCH RESULTS ---
        print(f"DEBUG: Using MOCKED web search results for query: '{query}'...")
        mock_web_search_results = [
            {"title": f"Senior Software Engineer - {query}", "link": "https://www.linkedin.com/jobs/mock-se-job", "snippet": "Leading software company seeking experienced engineer."},
            {"title": f"Data Scientist - {query}", "link": "https://www.indeed.com/jobs/mock-ds-job", "snippet": "Join our data team and build innovative solutions."},
            {"title": f"Cybersecurity Analyst - {query}", "link": "https://jobs.google.com/mock-cyber-job", "snippet": "Protect our systems from threats."}
        ]
        
        # Format mock search results into a string for the LLM
        formatted_results = []
        for i, res in enumerate(mock_web_search_results):
            formatted_results.append(f"Result {i+1}:\nTitle: {res.get('title', 'N/A')}\nLink: {res.get('link', 'N/A')}\nSnippet: {res.get('snippet', 'N/A')}\n")
        
        search_results_string = "\n".join(formatted_results)
        print(f"DEBUG: Formatted MOCKED search results for LLM:\n{search_results_string[:500]}...")

        # Step 2: Ask the agent to parse these results into JSON
        prompt_for_agent = f"""
        Here are the web search results for the query "{query}":

        {search_results_string}

        Please extract job listings from these results and provide them as a JSON array with "title", "company", "location", and "url". If a company or location isn't explicitly mentioned, try to infer it or use "N/A".
        """
        
        print(f"DEBUG: Sending final prompt to agent for JSON generation: {prompt_for_agent[:500]}...")
        agent_raw_response = await Runner.run(self.agent, prompt_for_agent)
        print(f"DEBUG: Agent's raw response (for JSON): {agent_raw_response}")

        job_list = []
        try:
            # Remove markdown code fences if present
            cleaned_response = re.sub(r"^```(?:json)?\n", "", agent_raw_response, flags=re.MULTILINE)
            cleaned_response = re.sub(r"\n```$", "", cleaned_response, flags=re.MULTILINE).strip()

            parsed_output = json.loads(cleaned_response)
            if isinstance(parsed_output, list):
                job_list = parsed_output
            else:
                print(f"WARNING: Agent output is JSON but not a list: {parsed_output}")
        except json.JSONDecodeError as e:
            print(f"ERROR: Failed to parse agent's final JSON output: {e}. Output: {agent_raw_response}")
            job_list = []
        except Exception as e:
            print(f"ERROR: An unexpected error occurred processing agent output: {e}. Output: {agent_raw_response}")
            job_list = []

        # Basic validation and filtering
        jobs = []
        for item in job_list:
            # Ensure all required keys are present and it's a dictionary
            if isinstance(item, dict) and all(k in item for k in ["title", "url", "company", "location"]):
                jobs.append(item)
            else:
                print(f"WARNING: Invalid job item format received from agent: {item}. Missing required keys or not a dict.")

        # Cache the result
        if jobs: # Only cache if valid jobs were found
            cache_results(query, jobs)
            print(f"DEBUG: Cached {len(jobs)} jobs for query: '{query}'")
        else:
            print(f"DEBUG: No valid jobs to cache for query: '{query}'")

        return jobs
