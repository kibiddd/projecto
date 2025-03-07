# Use a pipeline as a high-level helper
from transformers import pipeline
import main

def domain_analysis():
	pipe = pipeline("text-generation", model="microsoft/Phi-3.5-mini-instruct", trust_remote_code=True)
	task = """Based on the URL and the domain registration information, how likely is the website fraudulent?
Specifically, look at (1) Is the registration recent and/or expiring in less than a year? It is 2025-03-07 today.
(2) Is the contact information redacted or partial?
(3) Could the domain name be used to create a false sense of legitimacy?
(4) Other suspicious factors. Answer N/A if none.
Based on the answer to the above questions, give your final verdict on a scale of 1 to 10, with 10 being most likely.
Output should be a strict json format without any other comment. I.e. {"answer1": answer1, "answer2": answer2, "answer3": answer3, "answer4": answer4, "verdict": verdict(1-10)}"""
	url = "https://cyberfraudlawyers.com/"
	info = main.whois_info(url)
	task = task + "\nURL=" + url + "\nInfo=" + str(info)

	messages = [
		{
		"role": "user",
		"content": task
		}
	]

	result = pipe(messages, max_new_tokens=500)
	generated_text = result[0]['generated_text']
	content = generated_text[1]['content']
	print(content)
	return content

print(domain_analysis())