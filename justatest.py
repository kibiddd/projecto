import base64
import os
from google import genai
from google.genai import types
from PIL import Image


def generate():
    client = genai.Client(
        api_key="AIzaSyAr92W1v_HCTp3swoRaLlntgTBKyIBMtaM"
    )
    image = Image.open("website-screenshot/cyberfraudlawyer.png")
    task = """Based on the URL and the screenshot of the website, how likely is the website fraudulent? 
Specifically, look at (1) Phishing: Is the website requesting personal information or payment? 
(2) Too-good-to-be-true offer: Is it offering free product or service? 
(3) Format: Does the website have poor design or low-quality image? Is there any typo?
(4) Transparency: Does the website provide clear and trustworthy contact information?
(5) Impersonation: Is this website pretending to create a false sense of legitimacy? 
(6) Other suspicious factors. Answer N/A if none.
Based on the answer to the above questions, give your final verdict on a scale of 1 to 10, with 10 being most likely.
Output should be a strict json format without any other comment. I.e. {\"answer1\": explanation1,..., \"answer6\": explanation6 or N/A, \"verdict\": 1-10}
url = \"https://cyberfraudlawyers.com/\""""
    model = "gemini-2.0-flash-lite"
    contents = [image,task]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=500,
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()