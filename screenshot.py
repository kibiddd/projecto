import http.client
import json
from whois import get_domain
from dataset import load_dataset, new_only

def screenshot(url):

    conn = http.client.HTTPSConnection("scraper-tech.p.rapidapi.com")

    payload = f'{{"url":"{url}","screen_size":"1920x1080","delay":"10","full_height":1}}'

    headers = {
        'x-rapidapi-key': "9d1ccd75d1msha3f67fb0406279cp150b1ajsnf56415087996",
        'x-rapidapi-host': "scraper-tech.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    try:
        conn.request("POST", "/screenshot.php?url=https%3A%2F%2Fexample.com", payload, headers)

        res = conn.getresponse()
        data = res.read().decode("utf-8")
        data = json.loads(data)

        # Validate the response key
        if "response" in data:
            response = data["response"]
            return response.get("url")  # Return the URL from the response
        else:
            print(f"Error: 'response' key not found in API response. Full response: {data}")
            return None  # Return None if key is not found

    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        print(f"Error decoding JSON response: {e}")
        return None

    except http.client.HTTPException as e:
        # Handle HTTP errors
        print(f"HTTP error occurred: {e}")
        return None

    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    #print(screenshot("https://pt.overleaf.com/login"))
    #path1 = "phishing-links-250309.txt"
    #path2 = "phishing-links-250308.txt"
    #dataset = new_only(load_dataset(path1), load_dataset(path2))
    dataset = load_dataset("random_legit.txt")
    with open("ss-legit.txt", "a") as f:  # Open the file in append mode
        for idx, url in enumerate(dataset[161:500]):
            print(f"Screenshotting {idx + 1}/500: {url}")
            screenshot_url = screenshot(url)
            if screenshot_url:
                f.write(screenshot_url + "\n")
                print(f"Saved screenshot URL: {screenshot_url}")
            else:
                f.write(f"Failed to capture screenshot for URL: {url}\n")

    #for idx, url in enumerate(dataset[:100]):
    #    print(f"Screenshotting URL {idx}/{len(dataset)}: {url}")
    #    screenshot(url, str(idx), "random-legit/")
