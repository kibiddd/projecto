# Use a pipeline as a high-level helper
from transformers import pipeline

def url_analysis():
    task = """Analyze the URL and determine how likely is the website fraudulent.
Specifically, look at (1) Is the domain a misspelling or character substitution of a popular brand? Does it use subdomains to mislead?
(2) Note random strings/numbers, excessive hyphens or unusual symbols, HTTP instead of HTTPS, or unusually long URLs.
(3) Is the extension uncommon or high-risk (.xyz, .top, .club, .online, etc.) rather than standard (.com, .org, .net, etc.)?
(4) Other suspicious factors (or N/A if none).
Rate the URL's risk on a scale of 1 to 10, with 10 being most likely.
Output in strict JSON format without any other comment: {"answer1": explanation1, "answer2": explanation2, "answer3": explanation3, "answer4": explanation4 or N/A, "verdict": 1-10}

URL= https://umontreal.ca
{"answer1": "The domain 'umontreal.ca' is not a misspelling or character substitution of a popular brand. It appears to be the legitimate domain for the University of Montreal (Université de Montréal). It does not use subdomains to mislead.", "answer2": "The URL does not contain random strings, umontreal stands for University of Montreal. There's no excessive or unusual symbols. It uses HTTPS. The URL is not unusually long.", "answer3": "The extension '.ca' is the standard country code top-level domain for Canada. It is considered a safe and standard extension, especially for Canadian educational institutions.", "answer4": "N/A", "verdict": 1}

URL=https://cyberfraudlawyers.com/"""

    messages = [
    {"role": "user", "content": task},
    ]
    pipe = pipeline("text-generation", model="meta-llama/Llama-3.2-3B-Instruct")
    result = pipe(messages, max_new_tokens=200)
    #generated_text = result[0]['generated_text']
    #content = generated_text[1]['content']
    #print(result)
    return result


print(url_analysis())
