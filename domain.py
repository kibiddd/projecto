# Use a pipeline as a high-level helper
from transformers import pipeline
from datetime import datetime
import whois

# function that checks if registration info is invalid
def check_info(domain_info):
	if domain_info.startswith("No match") or domain_info.startswith("Streamline cancelled"):
		return True
	return False

def domain_analysis(pipe, url, domain_info):
	if check_info(info):
		print("Invalid info")
		return "Invalid info"
	# pipe = pipeline("text-generation", model="microsoft/Phi-4-mini-instruct", trust_remote_code=True)
	date = datetime.today().strftime('%Y-%m-%d')
	task = f"""Analyze this domain registration data and provide an overall scam risk score from 0-10 (10 = highest risk). Consider these factors:
	IMPORTANT: TODAY IS {date}.
1.  Registration Date: New domains (registered <6 months ago) are generally riskier. 
2.  Expiry Date: Domains expiring soon (within 1 year) may be riskier. 
3.  Contact Information: Redacted, incomplete, or suspicious WHOIS details increase risk.
4.  Other Factors: Any other suspicious registration information
	If no other information than URL is given, give a score of 0 and N/A as reasoning."""

	format_specification = """Output in strict JSON format:
	{"registration":"reasoning","expiry":"reasoning","contact":"reasoning","other":"reasoning","score":1-10}"""

	task = task + "\n" + format_specification

	# info = whois.whois_info(url)
	task = task + "\nURL=" + url + "\nInfo=" + str(domain_info)

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
	pipe = pipeline("text-generation", model="microsoft/Phi-4-mini-instruct", trust_remote_code=True)
	#url = 'http://yummy-rhinestone-button.glitch.me/hover.html'
	url = 'https://www.thekingsmeadow.net/FOSTER-CRAWFORD.htm'
	with open('legit-250311/31.txt', 'r') as f:
		info = f.read()
	domain_analysis(pipe=None, url=url, domain_info=info)

