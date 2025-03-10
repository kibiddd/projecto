# Use a pipeline as a high-level helper
from transformers import pipeline

def url_analysis(url,pipe):
    task = """Analyze the URL structure for fraud indicators:
(1) Deceptive Domain: Does it contain misspellings, character substitutions, or deceptive subdomains?
(2) TLD: Is the TLD uncommon or high-risk (.xyz, .top, .club, .online, etc.)?
(3) Patterns: Does the URL contain suspicious patterns (excessive length, random strings, unusual characters)?
(4) Other suspicious URL factors. Answer N/A if none.

Based on these factors, provide your verdict on a scale of 1 to 10, with 10 being most likely fraudulent.
Output in strict JSON format: {"Deceptive Domain": explanation1, "TLD": explanation2, "Patterns": explanation3, "Other": explanation4, "verdict": 1-10}
URL=""" + url

    messages = [
    {"role": "user", "content": task},
    ]
    #pipe = pipeline("text-generation", model="meta-llama/Llama-3.2-3B-Instruct")
    result = pipe(messages, max_new_tokens=200)
    generated_text = result[0]['generated_text']
    content = generated_text[1]['content']

    print(content)
    return content

if __name__ == "__main__":
    url_analysis(url="https://cyberfraudlawyers.com/")