## 🔹 **Backend (Flask) **

# Zeotap Chatbot - Backend (Flask)

This is the **Flask-based backend** for the Zeotap Chatbot, responsible for handling user queries, scraping data, and generating web scraped responses.

## 🚀 Features
- API endpoint for processing user queries
- Web scraping for fetching relevant data
- Summarization and response generation

## 🛠️ Tech Stack
- **Python** (Backend Logic)
- **Flask** (Web Framework)
- **BeautifulSoup / Requests** (Scraping)
- **OpenAI / NLP Models** (For response generation)

## 🏗️ Setup & Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/RAWMIC17/zeotap_chatbot_Backend.git
cd zeotap-chatbot-backend
```
2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```
4️⃣ Run the Server
```sh
python app.py
```
The API will be available at:
```sh
http://127.0.0.1:5000/scrape
```
