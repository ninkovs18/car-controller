from openai import OpenAI
import json
from fastapi import UploadFile
from io import BytesIO
import base64
from prompts.image_angle import build_rotation_prompt, build_ocr_prompt
from utils.image_rotate import rotate_img
import logging
import google.genai as genai
from google.genai import types
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
client_google = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def get_number_from_image(client: OpenAI, image: UploadFile) -> str:

    image_contents = await image.read()
    image_bytes = BytesIO(image_contents)
    
    system_prompt_rotation = build_rotation_prompt()
    
    response_image = client.chat.completions.create(
        model="gpt-5-2025-08-07",
        messages=[
            {"role": "system", "content": system_prompt_rotation},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(image_bytes.getvalue()).decode()}"}}
                ]
            }
        ],
        response_format={"type": "json_object"}
    )
    
    image_answer = response_image.choices[0].message.content
    response_json = json.loads(image_answer)
    
    rotation = response_json.get("rotation", "-")

    logger.info(str(rotation))

    new_image = rotate_img(image_bytes, int(rotation))

    opened_image = Image.open(new_image)

    system_prompt_ocr = build_ocr_prompt()

    config = types.GenerateContentConfig(
        response_mime_type="application/json"
        )

    response = client_google.models.generate_content(model="gemini-2.5-flash",
                                          contents=[opened_image, system_prompt_ocr],
                                          config=config
                                          )
    response_json_new = json.loads(response.text)
    rotation_new = response_json_new.get("value", "-")
    return rotation_new
