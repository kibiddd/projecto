# Use a pipeline as a high-level helper
from transformers import pipeline
from google import genai
from google.genai import types


def url_analysis(url):
    client = genai.Client(
        api_key="AIzaSyAr92W1v_HCTp3swoRaLlntgTBKyIBMtaM"
    )
    prompt = f"""You're a scam detection expert. Analyze URLs for phishing risk using the following steps, give a score 1-10 with 10 being most likely a scam.
    Output strict JSON.
    1. Immediate red flag if URL uses http
    2. Evaluate TLD risk (E.g., .xyz/.top = high, .com/.org/.(country) = low)
    3. Identify suspicious patterns (random strings, numbers, or excessive subdomains)
    4. Check for brand impersonation through character substitutions or clone project
    5. Assess other anomalies

    URL: http://amaz0n-payments.xyz/account-verify  
    {{"verdict": 10,
      "Explanation" : ["URL uses http",
       ".xyz is a high-risk TLD",
      "'account-verify' path common in credential phishing",
      "Uses 'amaz0n' with zero substitution to mimic 'amazon'"]
    }}

    URL: https://cyberfraudlawyers.com/
    {{"verdict": 7,
      "Explanation" : ["URL uses https",
       ".com is a low-risk TLD",
      "separating 'cyberfraudlawyers' we get cyber fraud lawyers, which may be used to build a false sense of legitimacy",
      "Website may be pretending to be cyber fraud lawyers to bait users"]    
    }}

    URL: {url}"""

    model = "gemini-2.0-flash-lite"
    contents = [prompt]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=200,
        response_mime_type="text/plain",
    )

    try:
        content_result = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        print(content_result.text)
        return content_result.text  # Access the full response and return it
    except Exception as e:
        print(f"Error during content generation: {e}")
        return None


if __name__ == "__main__":
    url_analysis(url="https://www.bestplaces.net/backfence/viewcomment.aspx?id=54A364A3-E13D-4D65-8D24-DCC811C4BB60&city=Encinitas_CA&p=50622678")