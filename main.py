from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI(title="Medical Diagnosis API")

# CORS cho frontend GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== LOAD JSON 1 LẦN DUY NHẤT =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "diseases.json")

with open(DATA_PATH, encoding="utf-8") as f:
    DISEASES = json.load(f)

class SymptomInput(BaseModel):
    symptom: str

@app.post("/diagnose")
def diagnose(data: SymptomInput):
    s = data.symptom.lower()

    for disease in DISEASES:
        for keyword in disease["keywords"]:
            if keyword in s:
                return {
                    "disease": disease["name"],
                    "explanation": disease["explanation"],
                    "advice": disease["advice"]
                }

    return {
        "disease": "Chưa xác định",
        "explanation": "Triệu chứng chưa đủ rõ để chẩn đoán.",
        "advice": "Bạn nên đi khám bác sĩ."
    }
