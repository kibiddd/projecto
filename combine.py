from huggingface_hub import InferenceClient
import model
import vlm

client = InferenceClient(
	provider="together",
	api_key="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"
)

task = """Based on the URL, analysis of domain registration, and analysis of screenshot of the website, summarize and list the insights in brief, followed by a final verdict on a scale of 1 to 10, with 10 being most likely."""
url = "https://cyberfraudlawyers.com/"
domain_analysis = model.domain_analysis()
screenshot_analysis = vlm.screenshot_analysis()
task = task + "\nURL=" + url + "\nDomain_Analysis=" + domain_analysis + "\nScreenshot_Analysis=" + screenshot_analysis
messages = [
	{
		"role": "user",
		"content": task
	}
]

completion = client.chat.completions.create(
    model="google/gemma-2-9b-it",
	messages=messages,
	max_tokens=500,
)

print(completion.choices[0].message)