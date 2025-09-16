from fastapi import FastAPI, File, Form, UploadFile
from ai_clients import analyze_car_angle, read_mileage, read_vin
from utils.read_file import read_bytes

app = FastAPI()

@app.post("/analyze")
async def analyze(
    question: str = Form(...),
    image: UploadFile = File(...)
):
    answer = analyze_car_angle(question, image)
    return answer

@app.post("/read_mileage")
async def read_mileage_endpoint(image: UploadFile = File(...)):
    image_bytes = await read_bytes(image)
    mileage = await read_mileage(image_bytes)
    return mileage

@app.post("/read_vin")
async def read_vin_endpoint(image: UploadFile = File(...)):
    image_bytes = await read_bytes(image)
    vin = await read_vin(image_bytes)
    return vin