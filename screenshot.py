import http.client
from whois import get_domain
from dataset import load_dataset, new_only

def screenshot(url, n, path):
    conn = http.client.HTTPSConnection("sitepic1.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "9d1ccd75d1msha3f67fb0406279cp150b1ajsnf56415087996",
        'x-rapidapi-host': "sitepic1.p.rapidapi.com"
    }
    conn.request("GET", "/screenshot?url=" + url + "&height=720&width=1280&delay=5", headers=headers)

    res = conn.getresponse()
    data = res.read()

    domain = get_domain(url)
    filename = path + n + ".png"
    with open(filename, "wb") as file:
        file.write(data)
    print("Screenshot saved as "+filename)
    return domain



if __name__ == "__main__":
    #path1 = "phishing-links-250309.txt"
    #path2 = "phishing-links-250308.txt"
    #dataset = new_only(load_dataset(path1), load_dataset(path2))
    dataset = load_dataset("legitimate_online_shop_urls.txt")
    for idx, url in enumerate(dataset):
        print(f"Screenshotting URL {idx}/{len(dataset)}: {url}")
        screenshot(url, str(idx), "legit/")
