from google import genai
from google.genai import types
from PIL import Image
import urllib.request as urllib2
import io
from screenshot import screenshot

def content_analysis(url, file_name):
    client = genai.Client(
        api_key="AIzaSyAr92W1v_HCTp3swoRaLlntgTBKyIBMtaM"
    )
    #domain = screenshot(url)
    #file_name = "website-screenshot/" + domain + ".png"
    # try opening image file
    try:
        fd = urllib2.urlopen(file_name)
        image_file = io.BytesIO(fd.read())
        image = Image.open(image_file)
    except Exception as e:
        print(f"Error opening image file: {e}")
        return "Error loading website screenshot."
    task = """Based on the URL and the screenshot of the website, how likely is the website fraudulent? 
Specifically, look at (1) Phishing: Is the website requesting personal information or payment? 
(2) Suspicious offer: Is it offering too-good-to-be-true or free product/service? 
(3) Format: Does the website have poor design or low-quality image? Is there any typo?
(4) Transparency: Does the website provide clear and trustworthy contact information?
(5) Impersonation: Is this website pretending to create a false sense of legitimacy? 
(6) Other suspicious factors. Answer N/A if none.
Based on the answer to the above questions, give your final verdict on a scale of 1 to 10, with 10 being most likely.
Output should be a strict json format without any other comment. I.e. {\"Phishing\": explanation1,..., \"Other\": explanation6 or N/A, \"verdict\": 1-10}
url = """ + url
    model = "gemini-2.0-flash-lite"
    contents = [image,task]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=500,
        response_mime_type="text/plain",
    )

    try:
        content_result = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        return content_result.text  # Access the full response and return it
    except Exception as e:
        print(f"Error during content generation: {e}")
        return None


if __name__ == "__main__":
    result = content_analysis(url="https://www.yelp.ca/biz/journal-de-montreal-montreal", file_name="https://scraper.tech/screenshots/4080700079.png")
    if result:
        print("Result:", result)
