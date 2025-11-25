from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from src.utils import fetch_html_with_js, extract_text, submit_answer
import json
import re

router = APIRouter()

STUDENT_EMAIL = "23f3001753@ds.study.iitm.ac.in"
SECRET_STRING = "23f3001753_super_secret_987"    # Replace with your own


class QuizRequest(BaseModel):
    email: str
    secret: str
    url: str


@router.post("/quiz")
async def handle_quiz(req: QuizRequest):
    # 1. Validate email + secret
    if req.email != STUDENT_EMAIL:
        raise HTTPException(status_code=403, detail="Invalid student email")

    if req.secret != SECRET_STRING:
        raise HTTPException(status_code=403, detail="Invalid secret")

    # 2. Load quiz page
    html = fetch_html_with_js(req.url)

    # Example sample parsing logic (you will replace this based on real question)
    text = extract_text(html)

    # 3. Simple sample detection: "What is 5 + 6?"
    m = re.search(r"What is (\d+) \+ (\d+)", text)
    if m:
        a = int(m.group(1))
        b = int(m.group(2))
        answer = a + b

        # Find submit URL from the page (dummy selector)
        submit_url = ""  # replace when real quiz gives actual URL

        resp = submit_answer(submit_url, req.email, req.secret, req.url, answer)
        return {"submitted_answer": answer, "server_response": resp}

    return {
        "status": "loaded",
        "message": "Quiz page fetched successfully — Now implement parsing logic here",
    }
