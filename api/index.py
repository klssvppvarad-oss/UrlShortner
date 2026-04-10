from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class URLRequest(BaseModel):
    url: str

def shorten_url(long_url: str) -> str:
    try:
        res = requests.get(
            "https://tinyurl.com/api-create.php",
            params={"url": long_url},
            timeout=5
        )

        short_url = res.text.strip()

        if "tinyurl.com" in short_url:
            short_url = short_url.replace("preview.", "")

        return short_url

    except:
        return "error"

@app.post("/shorten")
def shorten(data: URLRequest):
    return {
        "original": data.url,
        "short": shorten_url(data.url)
    }

# 👇 REQUIRED for Vercel
handler = app