from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

app = FastAPI(title="Medical Diagnosis API")

# Cho phép frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 ĐỌC JSON 1 LẦN DUY NHẤT (RẤT QUAN TRỌNG)
with open("data/diseases.json", encoding="utf-8") as f:
    DISEASES = json.load(f)

class SymptomInput(BaseModel):
    symptom: str

@app.post("/diagnose")
def diagnose(data: SymptomInput):
    user_text = data.symptom.lower()

    best_match = None
    best_score = 0

    for disease in DISEASES:
        score = 0
        for kw in disease["keywords"]:
            if kw in user_text:
                score += 1

        if score > best_score:
            best_score = score
            best_match = disease

    if best_match and best_score > 0:
        return {
            "disease": best_match["name"],
            "explanation": best_match["explanation"],
            "advice": best_match["advice"]
        }

    return {
        "disease": "Chưa xác định",
        "explanation": "Triệu chứng chưa đủ rõ ràng.",
        "advice": "Nên đến cơ sở y tế để được tư vấn."
    }
