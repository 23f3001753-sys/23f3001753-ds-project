import os
import requests
from bs4 import BeautifulSoup

def fetch_html_with_js(url: str) -> str:
    """
    Minimal fetcher. No JavaScript execution.
    Handles local files and URLs.
    """
    # Local file path?
    if os.path.exists(url):
        ext = url.lower().split(".")[-1]

        if ext in ["png", "jpg", "jpeg"]:
            return f"[IMAGE:{url}]"

        if ext in ["pdf"]:
            return f"[PDF:{url}]"

        if ext in ["html", "htm"]:
            with open(url, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

        return f"[FILE:{url}]"

    # Remote URL?
    try:
        r = requests.get(url, timeout=10)
        content_type = r.headers.get("Content-Type", "")

        if "image" in content_type:
            return "[REMOTE_IMAGE]"

        if "pdf" in content_type:
            return "[REMOTE_PDF]"

        if "html" in content_type:
            return r.text

        return "[UNSUPPORTED_REMOTE_FILE]"

    except:
        return "[FETCH_ERROR]"


def extract_text(html: str) -> str:
    """
    Basic text extractor from HTML or placeholder strings.
    """
    if html.startswith("[IMAGE") or html.startswith("[PDF"):
        return html  # No text to extract
    try:
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator="\n", strip=True)
    except Exception:
        return html


def submit_answer(submit_url: str, payload: dict) -> dict:
    """
    POST quiz answers.
    """
    try:
        r = requests.post(submit_url, json=payload, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}
