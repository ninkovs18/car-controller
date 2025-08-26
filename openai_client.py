from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi import UploadFile
from utils.truth_map import NOSE_POINTS_MAP
from services.car_direction import get_car_direction
from services.direction_checker import get_final_answer
from services.car_ocr import get_number_from_image

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_car_angle(question: str, image: UploadFile):
    
    nose_points = get_car_direction(client, image)

    truth = NOSE_POINTS_MAP.get(nose_points, "")

    answer = get_final_answer(client, question, truth)

    return answer

def read_number(image: UploadFile):
    extracted_number = get_number_from_image(client, image)
    return extracted_number



