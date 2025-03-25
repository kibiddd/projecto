import os
import requests
import json
from bs4 import BeautifulSoup
import concurrent.futures
import logging
import threading
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Thread-safe writing to active URLs file
write_lock = threading.Lock()


def process_domain(domain, idx, output_dir, active_file):
    """
    Process a domain by checking both HTTPS and HTTP protocols,
    then scrape and save content if available.
    """
    cleaned_domain = domain.strip()
    if not cleaned_domain:
        return False

    # Try HTTPS first
    url = f"https://{cleaned_domain}"
    response = check_url(url)

    # Fallback to HTTP if HTTPS fails
    if not response:
        url = f"http://{cleaned_domain}"
        response = check_url(url)

    if response and response.ok:
        success, content = scrape_and_save(response, idx, output_dir)
        if success and not is_error_page(content):
            with write_lock:
                # Update JSON file with index mapping
                update_active_urls(active_file, idx, url)
            return True
    return False


def is_error_page(content):
    """Check if content contains common error messages"""
    error_phrases = [
        '404', 'not found', 'page not found',
        'error', 'this page could not be found'
    ]
    return any(phrase in content.lower() for phrase in error_phrases)


def update_active_urls(filename, idx, url):
    """Thread-safe JSON updates"""
    # Read existing data
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    # Update data
    data[str(idx)] = url

    # Write back to file
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def check_url(url, timeout=10):
    """
    Check if a URL is accessible with proper error handling
    Returns response object if available, None otherwise
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
        if len(text) < 20:  # Increased minimum content length
            return None
        return response
    except Exception as e:
        logging.debug(f"Connection failed for {url}: {str(e)}")
        return None


def scrape_and_save(response, idx, output_dir):
    """
    Process and save website content from a successful response
    Returns (success, content) tuple
    """
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        # Clean content
        cleaned_lines = [line.strip() for line in text.splitlines() if line.strip()]
        cleaned_text = '\n'.join(cleaned_lines)

        # Save to file
        filename = os.path.join(output_dir, f"{idx}_scraped.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        return True, cleaned_text
    except Exception as e:
        logging.error(f"Error processing content: {e}")
        return False, ''


def main(input_file, num_workers=10):
    """
    Main processing function with concurrent execution
    """
    output_dir = "scam-active"
    active_file = "scam-active.json"  # Changed to JSON

    # Initialize output
    os.makedirs(output_dir, exist_ok=True)
    with open(active_file, 'w') as f:  # Initialize empty JSON
        json.dump({}, f)

    # Read domains
    with open(input_file, 'r') as f:
        domains = f.readlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        with tqdm(total=len(domains), desc="Processing domains") as pbar:
            future_to_idx = {
                executor.submit(process_domain, domain, idx, output_dir, active_file): idx
                for idx, domain in enumerate(domains)
            }

            successful = 0
            for future in concurrent.futures.as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    if future.result():
                        successful += 1
                except Exception as e:
                    logging.error(f"Error processing domain #{idx}: {e}")
                finally:
                    pbar.update(1)
                    pbar.set_postfix_str(f"Current index: {idx}")

    logging.info(f"Completed processing. Successfully scraped {successful}/{len(domains)} sites.")


if __name__ == "__main__":
    main(input_file="merged_scam_domains.txt")