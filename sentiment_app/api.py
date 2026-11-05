"""HTTP API for the sentiment scorer."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from sentiment_app.analyzer import analyze_comment

app = FastAPI(title="Qogam sentiment", version="0.1.0")


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/analyze")
def analyze(body: AnalyzeRequest) -> dict:
    try:
        return analyze_comment(body.text).as_dict()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
