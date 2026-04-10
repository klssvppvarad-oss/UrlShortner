from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ ADD THIS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for testing)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

def shorten_url(long_url: str) -> str:
    try:
        res = requests.get(
            "https://tinyurl.com/api-create.php",
            params={"url": long_url},
            timeout=5
        )
        return res.text
    except:
        return "error"

@app.post("/shorten")
def shorten(data: URLRequest):
    return {
        "original": data.url,
        "short": shorten_url(data.url)
    }

# ✅ Required for Vercel
handler = app
