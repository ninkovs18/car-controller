import textwrap

def build_angle_prompt() -> str:
    return textwrap.dedent("""
Task:
You are given an image of a car taken from eye-level perspective.
Your job is to determine where the car’s nose (the front part of the car, where the headlights and license plate are located) is pointing relative to the image frame.

Rules:

- If the car’s nose is pointing directly toward the left edge of the frame, return "left".
- If the car’s nose is pointing directly toward the right edge of the frame, return "right".
- If the car’s nose is pointing directly toward the top edge of the frame, return "up".
- If the car’s nose is pointing directly toward the bottom edge of the frame, return "down".
- If the car’s nose is pointing diagonally toward the top-left corner, return "up_left".
- If the car’s nose is pointing diagonally toward the top-right corner, return "up_right".
- If the car’s nose is pointing diagonally toward the bottom-left corner, return "down_left".
- If the car’s nose is pointing diagonally toward the bottom-right corner, return "down_right".


Important notes:
- The nose of the car is the FRONT end (headlights, grille, bumper). Never confuse it with the rear.
- Output only one of the 8 possible values. Nothing else is valid.
- If the nose of the car is looking at the camera, you have to return "down".

Output format (strict):

{ "nose_points": "left|right|up|down|up_left|up_right|down_left|down_right" }

Return only this JSON object. Do not include any explanation or text outside of the JSON.

""")

def build_question_prompt(question: str, truth: str) -> str:
    return textwrap.dedent(f""" 
You are an assistant that verifies the accuracy of a user's statement against a known truth.

User's statement: "{question}"
Known truth: "{truth}"

Check if the user's statement is correct based on the known truth. 

Respond only in JSON format as follows:

{{
  "answer": "Correct." 
}}

- If the user's statement is correct, the value should be "Correct."
- If the user's statement is incorrect, the value should be "Incorrect. {truth}"

Do not add anything else outside the JSON.

""")