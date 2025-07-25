import fitz  # PyMuPDF

def extract_text_from_pdf(path: str) -> str:
    """Extract raw text from a PDF file"""
    doc = fitz.open(path)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text


# tools/search_utils.py
import aiohttp
from bs4 import BeautifulSoup

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def search_duckduckgo(query):
    """Perform a simple DuckDuckGo search and return top result snippets"""
    base_url = "https://html.duckduckgo.com/html/"
    async with aiohttp.ClientSession() as session:
        data = {'q': query}
        async with session.post(base_url, data=data) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            results = []
            for a in soup.find_all("a", class_="result__a"):
                title = a.get_text()
                link = a.get("href")
                results.append({"title": title, "link": link})
                if len(results) >= 5:
                    break
            return results
