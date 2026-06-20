import requests
import json
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

KEYWORDS = [
    "ai",
    "llm",
    "machine learning",
    "deep learning",
    "nlp",
    "rag",
    "langchain",
    "genai",
    "generative ai",
    "computer vision",
    "mlops",
]

# دریافت جاب‌ها
jobs = requests.get(
    "https://remoteok.com/api",
    headers={"User-Agent": "Mozilla/5.0"}
).json()

# فایل جاب‌های دیده‌شده
try:
    with open("seen_jobs.json", "r") as f:
        seen = json.load(f)
except:
    seen = []

new_seen = seen.copy()

for job in jobs:

    if not isinstance(job, dict):
        continue

    job_id = job.get("id")

    if not job_id:
        continue

    if job_id in seen:
        continue

    title = str(job.get("position", "")).lower()

    if not any(k in title for k in KEYWORDS):
        continue

    company = job.get("company", "Unknown")
    url = job.get("url", "")

    message = f"""
🤖 AI Job Alert

🏢 Company: {company}
💼 Position: {job.get('position','')}
🔗 {url}
"""

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

    new_seen.append(job_id)

with open("seen_jobs.json", "w") as f:
    json.dump(new_seen, f)
