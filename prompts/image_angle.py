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

def build_ocr_prompt() -> str:
    return textwrap.dedent("""
    Task:
    You are a highly accurate OCR assistant. Your job is to extract either a **Vehicle Identification Number (VIN)** or a **mileage reading** from the provided image. Your core task is to **ensure absolute accuracy and correct character sequence** in the final output.

    Rules for Extraction:
    1.  **Image Orientation:** First, identify the correct orientation of the image. If the image is rotated, mentally rotate it to the correct, upright position for proper transcription.
    2.  **Prioritize VIN Extraction:**
        -   Check if the image contains a VIN. A VIN is a unique, **17-character alphanumeric string** (excluding the letters I, O, and Q) typically found on a vehicle's identification plate.
        -   If a VIN is found, extract the complete 17-character string.
    3.  **If no VIN, extract Mileage Reading:**
        -   If no VIN is found, look for a mileage reading. This will be a numerical value, usually followed by "km" or "miles", or displayed clearly on a dashboard.
        -   **Crucial for Mileage:** Extract ONLY the digits of the mileage. Do NOT include any commas, periods, spaces, or text (like "km" or "miles"). The extracted mileage should be a continuous string of numbers.

    General Principle:
    You must be extremely careful to transcribe every character and number **in the correct order**. Before returning a result, **carefully review the sequence** of characters to ensure it matches the image precisely, without any additions, omissions, or transpositions. Take all the time you need to be certain.

    Output format (strict):
    You must return a JSON object with two keys: "type" and "value".

    -   If a **VIN** is found, set "type" to "vin" and "value" to the 17-character VIN string.
    -   If **mileage** is found, set "type" to "mileage" and "value" to the continuous string of numerical digits.

    Example VIN output:
    { "type": "vin", "value": "WAUZZZF49HA036784" }

    Example mileage output:
    { "type": "mileage", "value": "125500" }
    
    Return only this JSON object. Do not include any explanation or text outside of the JSON.
    """)