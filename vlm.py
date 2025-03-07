from huggingface_hub import InferenceClient

client = InferenceClient(
	provider="together",
	api_key="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"
)
# rag: whatsapp is a red flag
def screenshot_analysis():
	task = """Based on the URL and the screenshot of the website, how likely is the website fraudulent? 
Specifically, look at (1) Phishing: Is the website requesting personal information or payment? 
(2) Too-good-to-be-true offer: Is it offering free product or service? 
(3) Format: Does the website have poor design or low-quality image? Is there any typo?
(4) Transparency: Does the website provide clear and trustworthy contact information?
(5) Impersonation: Is this website pretending to create a false sense of legitimacy? 
Based on the answer to the above questions, give your final verdict on a scale of 1 to 10, with 10 being most likely."""
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

	completion = client.chat.completions.create(
    	model="meta-llama/Llama-3.2-11B-Vision-Instruct",
		messages=messages,
		max_tokens=500,
	)
	result = completion.choices[0].message.content
	print(result)
	return result

#print(completion.choices[0].message)