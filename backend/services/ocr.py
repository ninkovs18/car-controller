from io import BytesIO
import json
from PIL import Image
from google.genai import types
from google.genai import Client
from prompts.prompt_builder import build_ocr_prompt_mileage, build_ocr_prompt_vin, build_180_or_0_prompt

async def get_mileage(client_google: Client, image: BytesIO, new_image: BytesIO, rotation: int) -> str:
    opened_image = Image.open(new_image)
    opened_old_image = Image.open(image)
    if(int(rotation) == 0 or int(rotation) == 180):
        system_180_prompt = build_180_or_0_prompt()

        config = types.GenerateContentConfig(
        response_mime_type="application/json"
        )

        response = client_google.models.generate_content(model="gemini-2.5-flash",
                                          contents=[opened_image, opened_old_image, system_180_prompt],
                                          config=config
                                          )
        response_json_new = json.loads(response.text)
        rotation_new = response_json_new.get("value", "-")
        return rotation_new
    

    system_prompt_ocr = build_ocr_prompt_mileage()

    config = types.GenerateContentConfig(
        response_mime_type="application/json"
        )

    response = client_google.models.generate_content(model="gemini-2.5-flash",
                                          contents=[opened_image, system_prompt_ocr],
                                          config=config
                                          )
    response_json_new = json.loads(response.text)
    rotation_new = response_json_new.get("mileage", "-")
    return rotation_new

async def get_vin(client_google: Client, new_image: BytesIO) -> str:
    opened_image = Image.open(new_image)
    system_prompt_ocr = build_ocr_prompt_vin()

    config = types.GenerateContentConfig(
        response_mime_type="application/json"
        )

    response = client_google.models.generate_content(model="gemini-2.5-flash",
                                          contents=[opened_image, system_prompt_ocr],
                                          config=config
                                          )
    response_json_new = json.loads(response.text)
    rotation_new = response_json_new.get("vin", "-")
    return rotation_new