import requests
from bs4 import BeautifulSoup
from dataset import load_dataset
from domain import check_all

def domain_to_url(domain):
    # check if domain is already a url
    if domain.startswith("http"):
        return domain
    else:
        return "https://" + domain

def scrape_text(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text content only
        scraped = soup.get_text(strip=True)  # Get all text, separating with newlines

        # if scraped text is empty and screenshot is white -> website not found.

        return scraped
    except requests.exceptions.RequestException as e:
        return f"URL is unreachable."

def write_out(path, scraped):
    with open(path, "w", encoding="utf-8") as file:
        print("Writing out")
        file.write(scraped)


# Example usage:
if __name__ == "__main__":
    link_path = 'scam-y.txt'
    to_path = 'scam-y/'
    dataset = load_dataset(link_path)
    inactives = check_all(link_path, to_path)
    unreachable = []
    for idx, link in enumerate(dataset):
        print(f'{idx+1}/{len(dataset)}')
        if idx in inactives:
            continue
        url = domain_to_url(link)
        text = scrape_text(url)
        if text.startswith('URL is unreachable'):
            unreachable.append(idx)
            continue
        write_out_path = to_path + str(idx) + '_text.txt'
        write_out(write_out_path, text)
    print(len(unreachable))
