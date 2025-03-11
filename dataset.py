import requests
import random
from whois import check_link_status, whois_info

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

def get_active():
    all_phish = load_dataset("phishing-links-NEW-last-hour.txt")
    active = []
    for idx, a in enumerate(all_phish, start=1):
        print(f"Checking URL {idx}/{len(all_phish)}: {a}")
        if check_link_status(a):
            active.append(a)
    return active

def write_out():
    active = get_active()
    print(len(active))
    with open("active.txt", "w", encoding="utf-8") as file:
        for idx, a in enumerate(active, start=1):
            file.write(a + "\n")
            print(f"Active URL {idx}/{len(active)}: {a}")

def new_only(dataset1, dataset2):
    only_new = []
    for d in dataset1:
        if d not in dataset2:
            only_new.append(d)
    return only_new

def get_whois(path1, path2):
    path1 = "phishing-links-250309.txt"
    path2 = "phishing-links-250308.txt"
    dataset = new_only(load_dataset(path1), load_dataset(path2))
    for idx, url in enumerate(dataset):
        print(f"Screenshotting URL {idx}/{len(dataset)}: {url}")
        raw = whois_info(url)
        # save raw to txt file
        filename = "phish-250309/" + str(idx) + ".txt"

        # Open the file in text mode ("w") since raw is a string
        with open(filename, "w", encoding="utf-8") as file:
            file.write(raw)

if __name__ == "__main__":
    random_dataset("legitimate_urls.txt", "random_legit.txt", 2000)

