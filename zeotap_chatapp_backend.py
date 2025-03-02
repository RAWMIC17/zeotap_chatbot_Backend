import time
import json
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Documentation sources
DOC_SOURCES = {
    "segment": "https://segment.com/docs/",
    "mparticle": "https://docs.mparticle.com/",
    "lytics": "https://docs.lytics.com/",
    "zeotap": "https://docs.zeotap.com/home/en-us/"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

def fetch_page_content(url):
    """Fetch page content using Requests first, then Selenium if blocked."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 403:
            print(f"⚠️ 403 Forbidden - Retrying with Selenium: {url}")
            return fetch_page_with_selenium(url)

        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def fetch_page_with_selenium(url):
    """Use Selenium if Requests gets blocked."""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"user-agent={HEADERS['User-Agent']}")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)
        time.sleep(5)  # Let JavaScript load
        
        # Scroll to load content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        page_source = driver.page_source
        driver.quit()
        return page_source
    except Exception as e:
        print(f"Error fetching with Selenium: {e}")
        return None

def extract_summary(page_content):
    """Extract a meaningful 80-100 word summary from the page."""
    try:
        soup = BeautifulSoup(page_content, "html.parser")

        # Find main content sections (avoiding menus/navs)
        main_content = soup.find("article") or soup.find("main") or soup.find("div", class_="content")
        if not main_content:
            main_content = soup.find("body")

        # Extract text from <p> or relevant sections
        paragraphs = main_content.find_all("p", recursive=True)
        if not paragraphs:
            paragraphs = main_content.find_all(["div", "span", "h2"])

        text = " ".join([p.text.strip() for p in paragraphs if p.text.strip()])
        words = text.split()

        if len(words) > 100:
            return " ".join(words[:100]) + "..."
        return text if len(words) >= 80 else "No relevant information found."

    except Exception as e:
        print(f"Error extracting summary: {e}")
        return "No relevant information found."


@app.route('/scrape', methods=['POST'])
def scrape():
    """API endpoint to scrape data based on query."""
    try:
        data = request.get_json()
        query = data.get("query", "").strip().lower()

        if not query:
            return jsonify({"error": "Query parameter is missing"}), 400

        matched_source = next((key for key in DOC_SOURCES if key in query), None)

        if not matched_source:
            return jsonify({"message": "No matching documentation found for your query."}), 404

        url = DOC_SOURCES[matched_source]
        print(f"🔍 Scraping: {matched_source} - {url}")

        page_content = fetch_page_content(url)
        if not page_content:
            return jsonify({"error": "Failed to fetch page content"}), 500

        summary = extract_summary(page_content)

        return jsonify({
            "query": query,
            "source": matched_source.capitalize(),
            "summary": summary if summary else "No relevant information found.",
            "url": url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
