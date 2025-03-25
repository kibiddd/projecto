import os
import json
from bs4 import BeautifulSoup
import requests

def check_url(url, timeout=10):
    """
    Check if a URL is accessible with proper error handling.
    Returns response object if available, None otherwise.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=timeout,
            allow_redirects=True
        )
        # Skip empty/parked pages
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().strip()
        if not text:  # Return None only if the page is completely empty
            return None
        return response
    except Exception as e:
        print(f"Connection failed for {url}: {str(e)}")
        return None


def find_and_add_missing_urls(active_file, output_dir):
    """
    Identify missing URLs based on scraped data and active links JSON file.
    Validate and add missing URLs to the JSON file.
    """
    # Load active URLs from JSON file
    try:
        with open(active_file, 'r') as f:
            active_urls = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        active_urls = {}

    # Load scraped data filenames
    try:
        scraped_files = [f for f in os.listdir(output_dir) if f.endswith("_scraped.txt")]
        scraped_indices = [int(f.split("_")[0]) for f in scraped_files]
    except FileNotFoundError:
        print(f"Directory '{output_dir}' not found.")
        return

    # Find missing indices
    active_indices = set(map(int, active_urls.keys()))
    missing_indices = set(scraped_indices) - active_indices

    print(f"Missing indices: {missing_indices}")

    # Process missing URLs
    for idx in missing_indices:
        domain_file = os.path.join(output_dir, f"{idx}_scraped.txt")
        try:
            with open(domain_file, 'r') as f:
                domain_content = f.read().strip()
                domain_name = domain_content.splitlines()[0]  # Assume first line contains domain name

            # Check URL availability (HTTPS first, then HTTP)
            url_https = f"https://{domain_name}"
            url_http = f"http://{domain_name}"
            response = check_url(url_https) or check_url(url_http)

            if response:  # If accessible, add to active URLs JSON file
                active_urls[str(idx)] = response.url  # Use actual URL from response

                print(f"Added URL for index {idx}: {response.url}")
        except Exception as e:
            print(f"Error processing index {idx}: {e}")

    # Save updated active URLs to JSON file
    with open(active_file, 'w') as f:
        json.dump(active_urls, f, indent=2)

    print("Updated active URLs JSON file.")


# Example usage
active_file = "scam-active.json"
output_dir = "scam-active"
find_and_add_missing_urls(active_file, output_dir)
