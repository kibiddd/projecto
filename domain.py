# Use a pipeline as a high-level helper
from transformers import pipeline
import whois

def domain_analysis(url):
	pipe = pipeline("text-generation", model="microsoft/Phi-4-mini-instruct", trust_remote_code=True)
	task = """Based on the domain registration information, analyze potential fraud indicators:
(1) Is the registration recent (less than 6 months) or expiring soon (less than a year)? Today is 2025-03-07.
(2) Is the contact information redacted, partial, or suspicious?
(3) Is the registrar known for hosting malicious sites or lacking verification?
(4) Other suspicious registration factors. Answer N/A if none.

Based on these factors, provide your verdict on a scale of 1 to 10, with 10 being most likely fraudulent.
Output in strict JSON format: {"answer1": explanation1, "answer2": explanation2, "answer3": explanation3, "answer4": explanation4 or "N/A", "verdict": 1-10}"""

	info = whois.whois_info(url)
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

if __name__ == "__main__":
	domain_analysis(url="https://cyberfraudlawyers.com/")

