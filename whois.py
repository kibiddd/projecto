import http.client
import re
import json

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

if __name__ == "__main__":
    print(get_domain("https://cyberfraudlawyers.com/contact-us/"))
    print(whois_data("cyberfraudlawyers.com"))