from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ai_clients import analyze_car_angle, read_mileage, read_vin
from utils.read_file import read_bytes
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import logging


logging.basicConfig(level=logging.INFO)

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_UPLOAD_BYTES = 8 * 1024 * 1024

def err(status: int, code: str, message: str):
    return JSONResponse(
        status_code=status,
        content={"error": code, "message": message}
    )

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(
    question: str = Form(...),
    image: UploadFile = File(...)
):
    if not image:
        return err(400, "MISSING_FILE", "Image is required.")
    if image.content_type and not image.content_type.startswith("image/"):
        return err(400, "INVALID_CONTENT_TYPE", "Only image uploads are allowed.")
    if not question or not question.strip():
        return err(400, "MISSING_QUESTION", "Question is required.")

    contents = await image.read()
    if len(contents) > MAX_UPLOAD_BYTES:
        return err(413, "FILE_TOO_LARGE", "File exceeds upload limit.")
    await image.seek(0)

    try:
        answer = await analyze_car_angle(question, image)
        return answer
    
    except HTTPException as e:
        raise
    except Exception as e:
        logging.exception("Analyze failed")
        return err(502, "AI_ERROR", f"Analyze failed: {e}")

@app.post("/read_mileage")
async def read_mileage_endpoint(image: UploadFile = File(...)):
    if not image:
        return err(400, "MISSING_FILE", "Image is required.")
    if image.content_type and not image.content_type.startswith("image/"):
        return err(400, "INVALID_CONTENT_TYPE", "Only image uploads are allowed.")

    try:
        image_bytes = await read_bytes(image)
        value = await read_mileage(image_bytes)
        return {"value": value}
    
    except HTTPException as e:
        raise
    except Exception as e:
        logging.exception("Read mileage failed")
        return err(502, "OCR_ERROR", f"Read mileage failed: {e}")

@app.post("/read_vin")
async def read_vin_endpoint(image: UploadFile = File(...)):
    if not image:
        return err(400, "MISSING_FILE", "Image is required.")
    if image.content_type and not image.content_type.startswith("image/"):
        return err(400, "INVALID_CONTENT_TYPE", "Only image uploads are allowed.")

    try:
        image_bytes = await read_bytes(image)
        value = await read_vin(image_bytes)
        return {"value": value}
    
    except HTTPException as e:
        raise
    except Exception as e:
        logging.exception("Read VIN failed")
        return err(502, "OCR_ERROR", f"Read VIN failed: {e}")