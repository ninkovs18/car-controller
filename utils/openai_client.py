from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from fastapi import UploadFile
from io import BytesIO
import base64

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_question_with_image(question: str, image: UploadFile):
    image_bytes = BytesIO(image.file.read())

    system_prompt_image = """
Task:
You are given an image of a car taken from eye-level perspective.
Your job is to determine where the car’s nose (the front part of the car, where the headlights and license plate are located) is pointing relative to the image frame.

Rules:

- If the car’s nose is pointing directly toward the left edge of the frame, return "left".
- If the car’s nose is pointing directly toward the right edge of the frame, return "right".
- If the car’s nose is pointing directly toward the top edge of the frame, return "up".
- If the car’s nose is pointing directly toward the bottom edge of the frame, return "down".
- If the car’s nose is pointing diagonally toward the top-left corner, return "up_left".
- If the car’s nose is pointing diagonally toward the top-right corner, return "up_right".
- If the car’s nose is pointing diagonally toward the bottom-left corner, return "down_left".
- If the car’s nose is pointing diagonally toward the bottom-right corner, return "down_right".


Important notes:
- The nose of the car is the FRONT end (headlights, grille, bumper). Never confuse it with the rear.
- Output only one of the 8 possible values. Nothing else is valid.
- If the nose of the car is looking at the camera, you have to return "down".

Output format (strict):

{ "nose_points": "left|right|up|down|up_left|up_right|down_left|down_right" }

Return only this JSON object. Do not include any explanation or text outside of the JSON.

"""


    response_image = client.chat.completions.create(
        model="gpt-5-2025-08-07",
        messages=[
             {"role": "system", "content": system_prompt_image},
             {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(image_bytes.getvalue()).decode()}"}}
            ]
        }],
        response_format={"type": "json_object"}
    )

    image_answer = response_image.choices[0].message.content

    response_image_json = json.loads(image_answer)

    nose_points = response_image_json["nose_points"]

    truth = ""

    if nose_points == "up":
        truth = "The car is pictured from the rear."
    elif nose_points == "up_left":
        truth = "The car is pictured from the rear left side."
    elif nose_points == "up_right":
        truth = "The car is pictured from the rear right side."
    elif nose_points == "down":
        truth = "The car is pictured from the front."
    elif nose_points == "down_left":
        truth = "The car is pictured from the front left side."
    elif nose_points == "down_right":
        truth = "The car is pictured from the front right side."
    elif nose_points == "left":
        truth = "The car is pictured from the left side."
    elif nose_points == "right":
        truth = "The car is pictured from the right side. "
        

    system_prompt_question = f""" 
You are an assistant that verifies the accuracy of a user's statement against a known truth.

User's statement: "{question}"
Known truth: "{truth}"

Check if the user's statement is correct based on the known truth. 

Respond only in JSON format as follows:

{{
  "answer": "Correct." 
}}

- If the user's statement is correct, the value should be "Correct."
- If the user's statement is incorrect, the value should be "Incorrect. {truth}"

Do not add anything else outside the JSON.

"""
    
    response_question = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        temperature=0,
        messages=[
             {
                "role": "user",
                "content": [
                    {"type": "text", "text": system_prompt_question}, 
            ]
        }],
        response_format={"type": "json_object"}
    )

    question_answer = response_question.choices[0].message.content

    response_question_json = json.loads(question_answer)

    answer = response_question_json["answer"]

    return answer



