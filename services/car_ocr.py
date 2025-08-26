from openai import OpenAI
import json
from fastapi import UploadFile
from io import BytesIO
import base64
from prompts.image_angle import build_ocr_prompt

def get_number_from_image(client: OpenAI, image: UploadFile) -> str:

    image_bytes = BytesIO(image.file.read())
    
    system_prompt_ocr = build_ocr_prompt()
    
    response_image = client.chat.completions.create(
        model="gpt-5-2025-08-07",
        messages=[
            {"role": "system", "content": system_prompt_ocr},
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
    
    return response_json.get("rotation", "-")