import http.client
import json
import concurrent.futures
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def screenshot(url):
    """
    Takes a screenshot of the given URL using the scraper-tech.p.rapidapi.com API.
    Returns the screenshot URL if successful, None otherwise.
    """
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
            logging.error(f"Error: 'response' key not found in API response. Full response: {data}")
            return None  # Return None if key is not found

    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        logging.error(f"Error decoding JSON response: {e}")
        return None

    except http.client.HTTPException as e:
        # Handle HTTP errors
        logging.error(f"HTTP error occurred: {e}")
        return None

    except Exception as e:
        # Handle any other unexpected errors
        logging.error(f"An unexpected error occurred: {e}")
        return None


def process_url(idx, url, data):
    """
    Takes a screenshot of a URL and adds the screenshot URL to the data dictionary.
    """
    try:
        screenshot_url = screenshot(url)
        if screenshot_url:
            data[str(idx)]["ss_url"] = screenshot_url
            logging.info(f"Screenshot URL added for index {idx}: {screenshot_url}")
        else:
            logging.warning(f"Failed to capture screenshot for index {idx}: {url}")
    except Exception as e:
        logging.error(f"Error processing index {idx}: {e}")


def main(input_file, output_file, num_workers=10):
    """
    Main function to process URLs in parallel and add screenshot URLs to the JSON file.
    """
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading JSON file: {e}")
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(process_url, idx, entry["url"], data): idx for idx, entry in data.items()}
        for future in concurrent.futures.as_completed(futures):
            future.result()  # Check for exceptions in the worker threads

    try:
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        logging.info(f"Screenshot URLs added to {output_file}")
    except IOError as e:
        logging.error(f"Error writing to JSON file: {e}")


if __name__ == "__main__":
    input_file = "scam-active.json"  # Replace with your input JSON file
    output_file = "scam_active.json"  # Replace with your desired output JSON file
    num_workers = 5  # Adjust the number of workers as needed
    main(input_file, output_file, num_workers)
