import http.client
from whois import get_domain

def screenshot(url):
    conn = http.client.HTTPSConnection("sitepic1.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "9d1ccd75d1msha3f67fb0406279cp150b1ajsnf56415087996",
        'x-rapidapi-host': "sitepic1.p.rapidapi.com"
    }
    conn.request("GET", "/screenshot?url=" + url + "&height=720&width=1280&delay=0", headers=headers)

    res = conn.getresponse()
    data = res.read()

    domain = get_domain(url)
    filename = "website-screenshot/" + domain + ".png"
    with open(filename, "wb") as file:
        file.write(data)
    print("Screenshot saved as screenshot.png")
    return domain



if __name__ == "__main__":
    screenshot("www.umontreal.ca")
