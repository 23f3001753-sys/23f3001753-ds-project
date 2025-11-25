from fastapi import FastAPI, Request, HTTPException
from api.routes import router

app = FastAPI(
    title="LLM Analysis Quiz API",
    description="23f3001753 IITM Project",
    version="1.0.0",
)

app.include_router(router)

@app.get("/")
def home():
    return {"status": "running", "message": "LLM Quiz API by 23f3001753"}
