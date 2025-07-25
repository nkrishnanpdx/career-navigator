# agents/deep_search_agent.py

import sqlite3
import hashlib
import json
import os
from deepsearch.tools import WebSearchTool
from openai import OpenAI
from openai.agents import AgentExecutor, OpenAIAgent

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
        self.agent = OpenAIAgent(
            model="gpt-4o",
            tools=[WebSearchTool()],
            instructions="""
            You are a job search assistant. Given a job title and location, use the WebSearchTool to find real, active job postings from LinkedIn, Indeed, or Google Jobs.
            Return a list of jobs as JSON with fields: title, company, location, and url.
            """
        )
        self.executor = AgentExecutor(agent=self.agent)
        initialize_cache()

    async def search(self, query: str) -> list:
        # Check local cache first
        cached = get_cached_results(query)
        if cached:
            return cached

        # Perform web search via DeepSearch agent
        result = await self.executor.run_async(f"Find jobs for: {query}")
        job_list = result.outputs if hasattr(result, "outputs") else []

        # Basic validation
        jobs = []
        for item in job_list:
            if isinstance(item, dict) and "title" in item and "url" in item:
                jobs.append(item)

        # Cache the result
        cache_results(query, jobs)
        return jobs
