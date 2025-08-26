from fastapi import FastAPI, File, Form, UploadFile
from openai_client import analyze_car_angle

app = FastAPI()

@app.post("/analyze")
async def analyze(
    question: str = Form(...),
    image: UploadFile = File(...)
):
    answer = analyze_car_angle(question, image)
    return answer
