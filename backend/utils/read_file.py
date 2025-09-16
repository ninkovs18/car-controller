from fastapi import UploadFile
from io import BytesIO

async def read_bytes(upload: UploadFile) -> BytesIO:
    bytes = await upload.read()
    return  BytesIO(bytes)
