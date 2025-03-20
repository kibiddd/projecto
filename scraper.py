import requests
from bs4 import BeautifulSoup


def scrape_text(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text content only
        text = soup.get_text(strip=True)  # Get all text, separating with newlines

        return text
    except requests.exceptions.RequestException as e:
        return f"URL is unreachable."


# Example usage:
if __name__ == "__main__":
    url = "https://www.rutalee.com/"  # Replace with the desired URL
    content = scrape_text(url)
    print(content)
