from openai import OpenAI
from io import BytesIO
from prompts.prompt_builder import build_rotation_prompt
import base64
import json

def _parse_json_or_raise(text: str) -> dict:
    try:
        return json.loads(text)
    except Exception as e:
        raise RuntimeError(f"Rotation model returned non-JSON response: {e}")

def _validate_rotation(val) -> int:
    try:
        r = int(val)
    except Exception:
        raise RuntimeError(f"Rotation is not an integer: {val}")
    if r not in (-90, 0, 90, 180):
        raise RuntimeError(f"Rotation out of allowed set (-90, 0, 90, 180): {r}")
    return r

async def get_rotation(client: OpenAI, image: BytesIO) -> int:
    """
    Returns: rotation int in {-90, 0, 90, 180}
    """
    try:
        image.seek(0)
        system_prompt_rotation = build_rotation_prompt()

        resp = client.chat.completions.create(
            model="gpt-5-2025-08-07",
            messages=[
                {"role": "system", "content": system_prompt_rotation},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64.b64encode(image.getvalue()).decode()}"
                            },
                        }
                    ],
                },
            ],
            response_format={"type": "json_object"},
        )

        raw = resp.choices[0].message.content
        data = _parse_json_or_raise(raw)
        rotation = _validate_rotation(data.get("rotation"))
        return rotation

    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(f"get_rotation failed: {e}")