import requests
import os

# Telegram credentials from GitHub Secrets
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# AI-related keywords
keywords = [
    "ai",
    "artificial intelligence",
    "machine learning",
    "ml",
    "deep learning",
    "llm",
    "nlp",
    "computer vision",
    "cv",
    "rag",
    "langchain",
    "langgraph",
    "agent",
    "ai engineer",
    "ml engineer",
    "data scientist",
    "data science",
    "generative ai",
    "genai",
    "python"
]

print("Downloading jobs...")

response = requests.get(
    "https://remoteok.com/api",
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

print("Status Code:", response.status_code)

jobs = response.json()

print("Jobs received:", len(jobs))

found = False

for job in jobs:

    if not isinstance(job, dict):
        continue

    title = str(job.get("position", "")).lower()

    print("Checking:", title)

    if not any(word in title for word in keywords):
        continue

    found = True

    company = job.get("company", "Unknown")
    url = job.get("url", "")

    message = (
        f"🤖 AI Job Found\n\n"
        f"🏢 Company: {company}\n"
        f"💼 Position: {job.get('position','')}\n"
        f"🔗 {url}"
    )

    telegram = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=30
    )

    print("Telegram response:", telegram.text)

    break

if not found:
    print("No AI jobs found.")
