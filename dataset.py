import requests
import random

def load_phishing_links(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404, 500)

        # Return the content of the file as a string
        content = response.text

        return content
    except requests.RequestException as e:
        print(f"Error fetching the file: {e}")
        return None

def load_all(url):
    content = load_phishing_links(url)
    if content:
        # split by linebreak
        lines = content.splitlines()
        print(type(lines))
        return lines
    else:
        print("Error loading dataset. Please check the URL and try again.")
        return None

def get_dataset():
    url = "https://phish.co.za/latest/phishing-links-ACTIVE.txt"
    url_list = load_all(url)
    if url_list:
        # output to txt file
        with open("phish.txt", "w", encoding="utf-8") as file:
            for u in url_list:
                file.write(u + "\n")

def load_dataset(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            # Attempt to read the file as UTF-8
            lines = file.read().splitlines()
            return lines
    except UnicodeDecodeError:
        # If UTF-8 fails, fall back to "latin-1" encoding
        with open(path, "r", encoding="latin-1") as file:
            lines = file.read().splitlines()
            return lines

def random_list(dataset, num):
    return random.sample(dataset, num)

def random_dataset(dataset_path, new_dataset_path, num):
    ran = random_list(load_dataset(dataset_path), num)
    # write out to txt
    with open(new_dataset_path, "w", encoding="utf-8") as file:
        for r in ran:
            file.write(r + "\n")


def new_only(dataset1, dataset2):
    only_new = []
    for d in dataset1:
        if d not in dataset2:
            only_new.append(d)
    return only_new


if __name__ == "__main__":
    random_dataset("legitimate_urls.txt", "random_legit.txt", 2000)

