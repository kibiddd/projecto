import http.client
import json
import base64
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def screenshot(url):
    """
    Takes a screenshot of the given URL using the scraper-tech.p.rapidapi.com API.
    Returns the screenshot image data as bytes if successful, None otherwise.
    """
    conn = http.client.HTTPSConnection("scraper-tech.p.rapidapi.com")

    #payload = f'{{"url":"{url}","screen_size":"1920x1080","delay":"10","full_height":1}}'

    headers = {
        'x-rapidapi-key': "9d1ccd75d1msha3f67fb0406279cp150b1ajsnf56415087996",
        'x-rapidapi-host': "sitepic1.p.rapidapi.com"
    }

    try:
        conn.request("GET", f"/screenshot?url={url}&height=720&width=1280&delay=10", headers=headers)
        res = conn.getresponse()
        image_data = res.read()  # Read the response as raw bytes

        # No need to decode as UTF-8, return the bytes directly
        if image_data:
            return image_data
        else:
            logging.error("Error: No image data received in API response.")
            return None

    except http.client.HTTPException as e:
        logging.error(f"HTTP error occurred: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None


def save_screenshot(image_data, filepath):
    """
    Saves the screenshot image data to a file.
    """
    try:
        with open(filepath, 'wb') as f:
            f.write(image_data)
        logging.info(f"Screenshot saved to {filepath}")
        return True
    except Exception as e:
        logging.error(f"Error saving screenshot to {filepath}: {e}")
        return False


if __name__ == "__main__":
    url = "https://aeposcoin.com"
    image_data = screenshot(url)

    if image_data:
        filepath = "aeposcoin_screenshot.png"  # Specify the desired filepath
        save_screenshot(image_data, filepath)
    else:
        logging.warning(f"Failed to capture screenshot for {url}")
