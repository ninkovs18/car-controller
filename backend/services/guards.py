# services/guards.py
import base64, json
from io import BytesIO
from fastapi import HTTPException
from openai import OpenAI
from prompts.prompt_builder import build_vin_detection_prompt, build_mileage_detection_prompt, build_car_detection_prompt

def _b64(image_bytes: BytesIO) -> str:
    return f"data:image/jpeg;base64,{base64.b64encode(image_bytes.getvalue()).decode()}"

def _ask_json(client: OpenAI, system_prompt: str, image_b64: str, model="gpt-4o-mini-2024-07-18"):
    resp = client.chat.completions.create(
        model=model,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [{"type":"image_url","image_url":{"url": image_b64}}]},
        ],
    )
    return json.loads(resp.choices[0].message.content)

def ensure_car_exterior(client: OpenAI, image_bytes: BytesIO):
    prompt = build_car_detection_prompt()
    data = _ask_json(client, prompt, _b64(image_bytes))
    if not data.get("is_passenger_vehicle", False):
        raise HTTPException(status_code=422, detail="The image does not contain a vehicle .")

def ensure_vin_present(client: OpenAI, image_bytes: BytesIO):
    prompt = build_vin_detection_prompt()
    data = _ask_json(client, prompt, _b64(image_bytes))
    if not data.get("has_vin", False):
        raise HTTPException(status_code=422, detail="The image does not contain a VIN number.")

def ensure_odometer(client: OpenAI, image_bytes: BytesIO):
    prompt = build_mileage_detection_prompt()
    data = _ask_json(client, prompt, _b64(image_bytes))
    if not data.get("is_odometer", False):
        raise HTTPException(status_code=422, detail="The image does not contain an odometer display.")
