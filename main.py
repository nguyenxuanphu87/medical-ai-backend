from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI(title="Medical Diagnosis API")

# =========================
# CORS – cho phép frontend gọi
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Đọc file diseases.json
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "diseases.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    diseases = json.load(f)

# =========================
# Model nhận dữ liệu
# =========================
class SymptomInput(BaseModel):
    symptom: str

# =========================
# API chẩn đoán
# =========================
@app.post("/diagnose")
def diagnose(data: SymptomInput):
    user_symptom = data.symptom.lower()

    for disease in diseases:
        match_count = 0

        for keyword in disease["keywords"]:
            if keyword.lower() in user_symptom:
                match_count += 1

        # Nếu khớp >= 2 triệu chứng → nghi ngờ bệnh
        if match_count >= 2:
            return {
                "disease": disease["name"],
                "explanation": disease["explanation"],
                "advice": disease["advice"]
            }

    return {
        "disease": "Chưa xác định",
        "explanation": "Chưa đủ triệu chứng để đưa ra chẩn đoán.",
        "advice": "Nên đến cơ sở y tế để được tư vấn."
    }
