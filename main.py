import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

response = requests.get(
    "https://remoteok.com/api",
    headers={"User-Agent": "Mozilla/5.0"}
)

jobs = response.json()

keywords = [
    "ai",
    "llm",
    "machine learning",
    "nlp",
    "deep learning"
]

for job in jobs:

    if not isinstance(job, dict):
        continue

    title = str(job.get("position", "")).lower()

    if any(word in title for word in keywords):

        company = job.get("company", "")
        url = job.get("url", "")

        text = (
            f"Company: {company}\n"
            f"Position: {title}\n"
            f"{url}"
        )

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": text
            }
        )

        break
