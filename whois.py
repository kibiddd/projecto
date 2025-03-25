import http.client
import re
import json
import requests
from dataset import load_dataset

def check_link_status(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    return response.status_code

def get_domain(url):
    # strip all prefix of url
    url = re.sub(r'^https?://(www\.)?', '', url)
    url = re.sub(r'^www\.', '', url)
    return url.split('/')[0]


def whois_data(domain):
    conn = http.client.HTTPSConnection("whois55.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "9d1ccd75d1msha3f67fb0406279cp150b1ajsnf56415087996",
        'x-rapidapi-host': "whois55.p.rapidapi.com"
    }

    conn.request("GET", "/api/v1/whois?domain=" + domain, headers=headers)

    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

def get_raw_text(data):
    if data.startswith("{"):
        raw = json.loads(data)["raw"]
        # split raw at <<<
        return raw.split("<<<")[0]
    else:
        return data

def whois_info(url):
    domain = get_domain(url)
    data = whois_data(domain)
    raw_text = get_raw_text(data)
    return raw_text

def get_whois(dataset_path, save_path):
    dataset = load_dataset(dataset_path)
    #dataset = dataset[163:]
    for idx, url in enumerate(dataset):
        print(f"Checking WHOIS {idx}/{len(dataset)}: {url}")
        raw = whois_info(url)
        # save raw to txt file
        filename = save_path + str(idx) + ".txt"

        # Open the file in text mode ("w") since raw is a string
        with open(filename, "w", encoding="utf-8") as file:
            file.write(raw)

if __name__ == "__main__":
    get_whois('scam-y.txt', 'scam-y/')