from fastapi import FastAPI, File, Form, UploadFile
from openai_client import analyze_car_angle, read_number

app = FastAPI()

@app.post("/analyze")
async def analyze(
    question: str = Form(...),
    image: UploadFile = File(...)
):
    answer = analyze_car_angle(question, image)
    return answer

@app.post("/read")
async def read(image: UploadFile = File(...)):
    number = await read_number(image)
    return number