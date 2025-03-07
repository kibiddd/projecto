from transformers import pipeline
from huggingface_hub import login
from dotenv import load_dotenv
import os

load_dotenv()

# Replace 'your_huggingface_token' with your actual Hugging Face token
token = os.getenv("TOKEN")

login(token=token)

# rag: whatsapp is a red flag
def screenshot_analysis():
	pipe = pipeline("image-text-to-text", model="meta-llama/Llama-3.2-11B-Vision-Instruct")
	task = """Based on the URL and the screenshot of the website, how likely is the website fraudulent? 
Specifically, look at (1) Phishing: Is the website requesting personal information or payment? 
(2) Too-good-to-be-true offer: Is it offering free product or service? 
(3) Format: Does the website have poor design or low-quality image? Is there any typo?
(4) Transparency: Does the website provide clear and trustworthy contact information?
(5) Impersonation: Is this website pretending to create a false sense of legitimacy? 
(6) Other suspicious factors. Answer N/A if none.
Based on the answer to the above questions, give your final verdict on a scale of 1 to 10, with 10 being most likely.
Output should be a strict json format without any other comment. I.e. {"answer1": explanation1, "answer2": explanation2,..., "answer6": explanation6 or N/A, "verdict": 1-10}"""
	url = "https://cyberfraudlawyers.com/"
	task = task + "\nURL=" + url

	messages = [
	{
		"role": "user",
		"content": [
			{
				"type": "text",
				"text": task
			},
			{
				"type": "image_url",
				"image_url": {
					"url": "https://snapshot-site.com/screenshots/cyberfraudlawyers.com/9173cc59-7331-4524-9c7c-91a3038d6aec/1741328050.png"
				}
			}
		]
	}
	]

	result = pipe(text=messages, max_new_tokens=500)
	generated_text = result[0]['generated_text']
	print(generated_text)
	return generated_text

screenshot_analysis()