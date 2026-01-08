from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Medical Diagnosis API")

# Cho phép frontend truy cập (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SymptomInput(BaseModel):
    symptom: str

@app.post("/diagnose")
def diagnose(data: SymptomInput):
    s = data.symptom.lower()

    if "sốt" in s and "đau hốc mắt" in s:
        return {
            "disease": "Nghi ngờ sốt xuất huyết",
            "explanation": "Sốt cao kèm đau hốc mắt là dấu hiệu thường gặp.",
            "advice": "Cần đến cơ sở y tế để xét nghiệm."
        }

    if "đau họng" in s or "rát họng" in s:
        return {
            "disease": "Viêm họng",
            "explanation": "Triệu chứng điển hình của viêm họng.",
            "advice": "Súc miệng nước muối, giữ ấm cổ."
        }

    if "ho" in s and "sốt" in s:
        return {
            "disease": "Cảm cúm",
            "explanation": "Ho và sốt thường gặp trong cảm cúm.",
            "advice": "Nghỉ ngơi, uống nhiều nước."
        }

    if "đau đầu" in s and "mệt" in s:
        return {
            "disease": "Căng thẳng / thiếu ngủ",
            "explanation": "Triệu chứng thường gặp khi stress.",
            "advice": "Ngủ đủ giấc, thư giãn."
        }

    if "đau bụng" in s or "buồn nôn" in s:
        return {
            "disease": "Rối loạn tiêu hóa",
            "explanation": "Triệu chứng tiêu hóa phổ biến.",
            "advice": "Ăn nhẹ, tránh đồ dầu mỡ."
        }

    return {
        "disease": "Chưa xác định",
        "explanation": "Chưa đủ dữ liệu chuẩn đoán.",
        "advice": "Nên đi khám bác sĩ."
    }
