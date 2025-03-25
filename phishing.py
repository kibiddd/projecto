import requests
from dataset import load_dataset
from bs4 import BeautifulSoup
import time
import concurrent.futures
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_available(url, timeout=10):
    """
    Checks if a website is available and not a parked domain.
    Returns True if available with meaningful content, False otherwise.
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
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().lower()

        if not text:
            return False

        return True

    except (requests.ConnectionError, requests.Timeout,
            requests.TooManyRedirects, requests.HTTPError,
            requests.exceptions.SSLError) as e:
        logging.error(f"Error checking {url}: {e}")
        return False

def process_url(url, idx, available_urls, output_file='phishing_active.txt'):
    """
    Checks if a URL is available and writes it to a file if it is.
    """
    logging.info(f'Checking url {idx}: {url}')
    if is_available(url):
        with open(output_file, 'a') as f:
            f.write(url + '\n')
        available_urls.append(url)
        logging.info(f"Found available URL: {url}, no {len(available_urls)}")
        return True
    return False

def main(num_workers=10, output_file='phishing_active.txt', max_urls=10000):
    """
    Loads a dataset of URLs, checks their availability using multiple workers,
    and saves the available URLs to a file.
    """
    phishing_dataset = load_dataset('phishing-links-ACTIVE.txt')
    available_urls = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Use a list to keep track of the future tasks
        futures = {executor.submit(process_url, url, idx, available_urls, output_file): idx for idx, url in enumerate(phishing_dataset)}

        for future in concurrent.futures.as_completed(futures):
            idx = futures[future]
            try:
                future.result()  # Get the result (or exception) from the future
            except Exception as e:
                logging.error(f"Error processing URL at index {idx}: {e}")

            if len(available_urls) >= max_urls:
                logging.info(f"Reached the maximum number of URLs: {max_urls}")
                break

            time.sleep(0.1) # Be polite - add delay

    print(f"Found {len(available_urls)} available URLs")

if __name__ == "__main__":
    main()
