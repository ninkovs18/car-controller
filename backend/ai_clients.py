from openai import OpenAI
import google.genai as genai
import os
from dotenv import load_dotenv
from fastapi import UploadFile
from io import BytesIO
from utils.truth_map import NOSE_POINTS_MAP
from services.car_direction import get_car_direction
from services.direction_checker import get_final_answer
from services.image_rotation import get_rotation
from services.ocr import get_mileage, get_vin
from utils.image_rotate import rotate_img_mileage, rotate_img_vin

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client_google = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_car_angle(question: str, image: UploadFile):
    
    nose_points = get_car_direction(client, image)

    truth = NOSE_POINTS_MAP.get(nose_points, "")

    answer = get_final_answer(client, question, truth)

    return answer

async def read_vin(image: BytesIO):
    rotation = await get_rotation(client, image)
    new_image = rotate_img_vin(image, rotation)
    vin = await get_vin(client_google, new_image)
    return vin

async def read_mileage(image: BytesIO):
    rotation = await get_rotation(client, image)
    new_image = rotate_img_mileage(image, rotation)
    mileage = await get_mileage(client_google, image, new_image, rotation)
    return mileage


