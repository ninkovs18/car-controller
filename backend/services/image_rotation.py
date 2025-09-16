from openai import OpenAI
from io import BytesIO
from prompts.prompt_builder import build_rotation_prompt
import base64
import json

async def get_rotation(client: OpenAI, image: BytesIO) -> int:

    
    system_prompt_rotation = build_rotation_prompt()
    
    response_image = client.chat.completions.create(
        model="gpt-5-2025-08-07",
        messages=[
            {"role": "system", "content": system_prompt_rotation},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(image.getvalue()).decode()}"}}
                ]
            }
        ],
        response_format={"type": "json_object"}
    )
    
    image_answer = response_image.choices[0].message.content
    response_json = json.loads(image_answer)
    
    rotation = response_json.get("rotation", "-")

    return int(rotation)