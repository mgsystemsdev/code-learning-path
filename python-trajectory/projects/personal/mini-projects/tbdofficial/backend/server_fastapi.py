# Author:      Miguel Gonzalez Almonte  # Created:     2025-05-24  # File:        server_fastapi.py  # Description: FastAPI server  
# server_fastapi.py
# FastAPI version with Swagger UI

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import json

app = FastAPI()

class LogEntry(BaseModel):
    event: str
    context: Dict[str, str]

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.post("/log")
def log_event(entry: LogEntry):
    with open("logs/launch.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry.dict()) + "\n")
    return {"status": "logged"}

@app.get("/widgets")
def list_widgets():
    return {
        "qt": ["QPushButton", "QSlider", "QCheckBox"],
        "tk": ["Button", "Scale", "Checkbutton"]
    }

# To run:
# uvicorn server_fastapi:app --reload
