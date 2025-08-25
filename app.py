from fastapi import FastAPI, File, Form, UploadFile
from utils.openai_client import ask_question_with_image

app = FastAPI()

@app.post("/analyze")
async def analyze(
    question: str = Form(...),
    image: UploadFile = File(...)
):
    answer = ask_question_with_image(question, image)
    return answer
