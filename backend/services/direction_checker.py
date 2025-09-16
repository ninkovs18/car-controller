from openai import OpenAI
import json
from prompts.prompt_builder import  build_question_prompt

def get_final_answer(client: OpenAI, question: str, truth: str) -> str:
    system_prompt_question = build_question_prompt(question, truth)
    
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

    return response_question_json["answer"]