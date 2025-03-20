# Use a pipeline as a high-level helper
from transformers import pipeline

def url_analysis(url,pipe):
    prompt = f"""Analyze URLs for phishing risk using the following steps, give a score 1-10 with 10 being most likely a scam.
     Output strict JSON.
    1. If URL uses http, score >= 7
    2. Check for brand impersonation through character substitutions
    3. Evaluate TLD risk (E.g., .xyz/.top = high, .com/.org/.(country) = low)
    4. Identify suspicious patterns (random strings, excessive subdomains)
    5. Assess other anomalies

    URL: http://amaz0n-payments.xyz/account-verify  
    {{
      "Explanation" : ["URL uses http", 
      "Uses 'amaz0n' with zero substitution to mimic 'amazon'",
       ".xyz is a high-risk TLD",
      "'account-verify' path common in credential phishing"]
      "verdict": 10
    }}
    
    URL: http://144644103365.com
    {{
      "Explanation" : ["URL uses http", 
      "no impersonation in URL",
       ".com is a low-risk TLD",
       "domain contains random strings 144644103365"],
       "verdict": 8
    }}
    
    URL: https://cyberfraudlawyers.com/
    {{
      "Explanation" : ["no impersonation in URL",
       ".com is a low-risk TLD",
      "separating 'cyberfraudlawyers' we get cyber fraud lawyers, which may be used to build a false sense of legitimacy"],
      "verdict": 7
    }}

    URL: {url}"""

    messages = [
    {"role": "user", "content": prompt},
    ]
    #pipe = pipeline("text-generation", model="meta-llama/Llama-3.2-3B-Instruct")
    result = pipe(messages, max_new_tokens=200)
    generated_text = result[0]['generated_text']
    content = generated_text[1]['content']

    print(content)
    return content

if __name__ == "__main__":
    pipe = pipeline("text-generation", model="microsoft/Phi-4-mini-instruct", trust_remote_code=True)
    url_analysis(url="https://www.bestplaces.net/backfence/viewcomment.aspx?id=54A364A3-E13D-4D65-8D24-DCC811C4BB60&city=Encinitas_CA&p=50622678", pipe=pipe)