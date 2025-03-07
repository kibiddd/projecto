from huggingface_hub import InferenceClient
import main

client = InferenceClient(
	provider="together",
	api_key="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"
)

def domain_analysis():
	task = """Based on the URL and the domain registration information, how likely is the website fraudulent?
Specifically, look at (1) Is the registration recent and short? 
(2) Is the contact information redacted or partial?
(3) Could the domain name be used to create a false sense of legitimacy?
Based on the answer to the above questions, give your final verdict on a scale of 1 to 10, with 10 being most likely."""
	url = "https://cyberfraudlawyers.com/"
	info = main.whois_info(url)
	task = task + "\nURL=" + url + "\nInfo=" + str(info)

	messages = [
		{
		"role": "user",
		"content": task
		}
	]

	completion = client.chat.completions.create(
		model="meta-llama/Llama-3.2-3B-Instruct",
		messages=messages,
		max_tokens=500,
	)
	result = completion.choices[0].message.content
	print(result)
	return result

#print(completion.choices[0].message)