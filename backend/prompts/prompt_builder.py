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
  "result": "Correct|Incorrect" 
}}

- If the user's statement is correct, the result should be "Correct."
- If the user's statement is incorrect, the result should be "Incorrect."

Do not add anything else outside the JSON.

""")


def build_rotation_prompt() -> str:
    return textwrap.dedent("""
    Task:
    You are an assistant specialized in analyzing image orientation. Your sole task is to determine the exact rotation of the text within the provided image.

    Rules:
    -   Analyze the text to determine its orientation relative to an upright, human-readable position.
    -   Match the orientation to one of the following four values:
        -   **0**: The text is upright and flows from left to right. This is the correct, default orientation.
        -   **180**: The text is completely upside down.
        -   **90**: The text is rotated 90 degrees clockwise (to the right).
        -   **-90**: The text is rotated 90 degrees counter-clockwise (to the left).

    Output format (strict):
    Return a single JSON object with a key "rotation" and a value representing the rotation in degrees. The only valid values are 0, 90, 180, or -90.

    Example outputs:
    -   Upright text: { "rotation": 0 }
    -   Upside-down text: { "rotation": 180 }
    -   Left-rotated text: { "rotation": -90 }
    -   Right-rotated text: { "rotation": 90 }
    
    Return only this JSON object. Do not include any explanation or text outside of the JSON.
    """)

def build_180_or_0_prompt() -> str:
    return textwrap.dedent("""
You are an expert at analyzing images of car dashboards. Your task is to examine the provided images, identify the correct orientation, and read the mileage.

Instructions:
1.  Analyze two or more images of a car's digital display.
2.  Determine which image is displayed with a normal, upright orientation. One image may be rotated 180 degrees.
3.  Read the mileage (kilometers) from the image with the correct orientation.
4.  Return the output in a JSON object with one attribute:
    -   `value`: The mileage reading as a numerical value, without commas, decimals, or any other characters.

Example:
User provides two images. One is upright, the other is inverted.

Your response should be a JSON object like this:
```json
{
  "value": 278659
}

""")

def build_ocr_prompt_vin() -> str:
    return textwrap.dedent("""
  You are an AI specialized in reading VIN numbers (Vehicle Identification Number) from car images.

Instructions:
1. Carefully analyze the provided image and extract the VIN number.
2. The VIN number is a 17-character alphanumeric string (uppercase letters and digits, no spaces).
3. Return ONLY a valid JSON object.
4. Do not add any extra text or explanations.
5. If the VIN is not perfectly clear, still return your best guess.

Output format:
{
  "vin": "<the extracted VIN number>"
}

Example:
If the image shows: `1HGCM82633A123456`
Output: { "vin": "1HGCM82633A123456" }
    """)

def build_ocr_prompt_mileage() -> str:
    return textwrap.dedent("""
You are an AI specialized in reading car mileage (odometer reading) from images.

Instructions:
1. Carefully analyze the provided image and extract the mileage value.
2. The mileage value is a number, sometimes with commas, dots, or the unit "km" or "miles".
3. Return ONLY the number as a string, without any commas, dots, or letters.
4. Return ONLY a valid JSON object.
5. Do not add any extra text or explanations.
6. If the value is not perfectly clear, still return your best guess.

Output format:
{
  "mileage": "<the extracted mileage number as a string>"
}

Example:
If the image shows: `234,567 km`
Output: { "mileage": "234567" }
    """)


def build_car_detection_prompt() -> str:
    return textwrap.dedent("""
You are a fast image triage. Answer only JSON.

Task: Decide if the image shows the EXTERIOR of exactly ONE PASSENGER VEHICLE
(e.g., car, SUV, van, minivan, small crossover), suitable for angle/orientation analysis,
even if only a substantial portion of that single vehicle is visible.

TRUE if:
- The image contains exactly one passenger vehicle exterior, and
- It may be partially cropped or occluded, as long as it is unambiguously the exterior of a single passenger vehicle.
  Accept close views such as: front bumper + headlight/grille, fender + wheel/door panel, rear lamps + bumper.

FALSE if the image shows:
- More than one vehicle (even if all are passenger vehicles),
- Interiors (dashboard, instrument cluster/odometer, seats),
- License-plate close-ups with no surrounding body context,
- Motorcycles, bicycles,
- Buses, trucks, trailers, heavy machinery,
- Toys, models, drawings, renderings,
- Or the view is so close/blurred that you cannot tell it’s the exterior of a passenger vehicle.

Output (strict):
{ "is_passenger_vehicle": true|false }

    """)

def build_vin_detection_prompt() -> str:
    return textwrap.dedent("""
You are a fast image triage. Answer only JSON.

Task: Decide if the image contains a VIN label/plate or a VIN string (17 chars, uppercase letters & digits, no I/O/Q).

Signals for true: metal/plastic VIN plate, windshield corner VIN tag, door jamb sticker with long alphanumeric code.
False: odometer, random stickers, license plate, mileage numbers.

Return ONLY:
{ "has_vin": true|false }
    """)

def build_mileage_detection_prompt() -> str:
    return textwrap.dedent("""
You are a fast image triage. Answer only JSON.

Task: Decide if the image shows an odometer / instrument cluster (digital 7-segment or analog dials) suitable for mileage OCR.

True if: gauge cluster, odometer display, dashboard with mileage readout.
False if: car exterior, VIN plate, license plate, random text.

Return ONLY:
{ "is_odometer": true|false }

    """)