from transformers import pipeline
from domain import domain_analysis
from cont import content_analysis
from url import url_analysis

def combine():

	task = """Based on the analysis of URL, domain registration, and a screenshot of the website, determine if it is a scam website. 
Summarize and list the most important keywords for each analysis, followed by a summary of the website and its potential risks, a final verdict on a scale of 1 to 10, with 10 being most likely.
Output should be a strict json format without any other comment. I.e. {"URL analysis": [keywords], "Domain analysis": [keywords], "Content analysis": [keywords], "Summary": "summary", "verdict": 1-10}"""
	link = "https://cyberfraudlawyers.com/"


	task = task + "\nURL=" + link + "\nURL_Analysis=" + url_analysis() + "\nDomain_Analysis=" + domain_analysis() + "\nScreenshot_Analysis=" + content_analysis()
	messages = [
		{
		"role": "user",
		"content": task
		}
	]
	pipe = pipeline("text-generation", model="microsoft/Phi-4-mini-instruct", trust_remote_code=True)

	result = pipe(messages, max_new_tokens=500)
	generated_text = result[0]['generated_text']
	content = generated_text[1]['content']
	print(content)
	return content

combine()