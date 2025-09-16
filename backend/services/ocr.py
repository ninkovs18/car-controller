from io import BytesIO
import json
from PIL import Image
from google.genai import types
from google.genai import Client
from prompts.prompt_builder import build_ocr_prompt_mileage, build_ocr_prompt_vin, build_180_or_0_prompt
from services.guards import ensure_odometer, ensure_vin_present
from openai import OpenAI
from fastapi import HTTPException

def _open_image_or_raise(buf: BytesIO) -> Image.Image:
    try:
        buf.seek(0)
        return Image.open(buf)
    except Exception as e:
        raise RuntimeError(f"Failed to open image: {e}")

def _parse_json_or_raise(text: str) -> dict:
    try:
        return json.loads(text)
    except Exception as e:
        raise RuntimeError(f"Model returned non-JSON response: {e}")

async def get_mileage(client: OpenAI, client_google: Client, image: BytesIO, new_image: BytesIO, rotation: int) -> str:
    try:
        ensure_odometer(client, image)
        opened_image = _open_image_or_raise(new_image)

        if int(rotation) in (0, 180):
            
            opened_old_image = _open_image_or_raise(image)
            system_180_prompt = build_180_or_0_prompt()

            cfg = types.GenerateContentConfig(response_mime_type="application/json")
            resp = client_google.models.generate_content(
                model="gemini-2.5-flash",
                contents=[opened_image, opened_old_image, system_180_prompt],
                config=cfg,
            )
            data = _parse_json_or_raise(resp.text)
           
            val = data.get("value")

            return val  

    
        system_prompt_ocr = build_ocr_prompt_mileage()
        cfg = types.GenerateContentConfig(response_mime_type="application/json")
        resp = client_google.models.generate_content(
            model="gemini-2.5-flash",
            contents=[opened_image, system_prompt_ocr],
            config=cfg,
        )
        data = _parse_json_or_raise(resp.text)

        mileage = data.get("mileage")
        if not mileage:
            raise RuntimeError("OCR did not return 'mileage'")
        return mileage
    
    except HTTPException as e:
        raise

    except RuntimeError:

        raise
    except Exception as e:
        
        raise RuntimeError(f"get_mileage failed: {e}")

async def get_vin(client: OpenAI, client_google: Client, new_image: BytesIO) -> str:
    try:
        ensure_vin_present(client, new_image)
        opened_image = _open_image_or_raise(new_image)
        system_prompt_ocr = build_ocr_prompt_vin()

        cfg = types.GenerateContentConfig(response_mime_type="application/json")
        resp = client_google.models.generate_content(
            model="gemini-2.5-flash",
            contents=[opened_image, system_prompt_ocr],
            config=cfg,
        )
        data = _parse_json_or_raise(resp.text)

        vin = data.get("vin")
        if not vin:
            raise RuntimeError("OCR did not return 'vin'")
        return vin

    except HTTPException as e:
        raise
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(f"get_vin failed: {e}")