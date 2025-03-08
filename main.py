# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import gradio as gr
import requests
from bs4 import BeautifulSoup
import re

#URL = "https://who.is/whois/google.com"
#page = requests.get(URL)
#content = page.text


#soup = BeautifulSoup(content, 'html.parser')

# extract text from soup
#text = soup.get_text()

key_info = [
    "Registrar Info",
    "Important Dates",
    "Name Servers",
    "Registrar Data",
    "Site Status"]


def find_key_info(text, key):
    start = text.find(key)
    end = text.find(key_info[key_info.index(key) + 1])
    return text[start:end]

def parse_info(info):
    info_lines = [line.strip() for line in info.splitlines() if line.strip()]
    info_lines = info_lines[1:]
    info_dict = {}
    for i in range(0, len(info_lines), 2):
        info_dict[info_lines[i]] = info_lines[i + 1]
    return info_dict

def parse_registrar_data(data):

    data = re.sub(r':', r': ', data)
    # add new line when there's a capital letter following a lower case
    data = re.sub(r'([a-z])([A-Z])', r'\1\n\2', data)
    return data

def get_info(text, key):
    info = find_key_info(text, key)
    return parse_info(info)


def parse_url(url):
    # strip all prefix of url
    url = re.sub(r'^https?://(www\.)?', '', url)
    url = re.sub(r'^www\.', '', url)
    return "https://who.is/whois/" + url.split('/')[0]



def check_website(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)

        print(response.status_code)
        return response.status_code == 200
    except requests.RequestException:
        print("Error")
        return False

def whois_info(url):
    if not check_website(url):
        return "Page not found. Please check the URL."
    url = parse_url(url)
    print(url)
    page = requests.get(url)
    # return error message if page not found
    content = page.text

    soup = BeautifulSoup(content, 'html.parser')

    # extract text from soup
    text = soup.get_text()

    # if text include "WHOIS data currently unavailable." return "Domain seems down!"
    if "WHOIS data currently unavailable." in text:
        return "The domain seems down!"

    # get registrar_info, important_dates, and registrar data into a JSON-like structure
    registrar_info = get_info(text, "Registrar Info")
    important_dates = get_info(text, "Important Dates")
    registrar_data = parse_registrar_data(find_key_info(text, "Registrar Data"))

    whois_data = {
        "Registrar Info": registrar_info,
        "Important Dates": important_dates,
        "Registrar Data": registrar_data
    }
    return whois_data

# find "Registrar Info" in text
#start = text.find("Registrar Data")
# end at "Important Dates"
#end = text.find("Site Status")
# extract text from start to end excluding the start
#registrar_info = text[start:end]

# add a space after each:
#registrar_info = re.sub(r':', r': ', registrar_info)
# add new line when there's a capital letter following a lower case
#registrar_info = re.sub(r'([a-z])([A-Z])', r'\1\n\2', registrar_info)

#registrar_info_lines = [line.strip() for line in registrar_info.splitlines() if line.strip()]
#registrar_info_lines = registrar_info_lines[1:]

# put in dictionary, odd element is key and even is value
#registrar_info_dict = {}
#for i in range(0, len(registrar_info_lines), 2):
#    registrar_info_dict[registrar_info_lines[i]] = registrar_info_lines[i + 1]
print(whois_info("google.ca"))
demo = gr.Interface(
    fn=whois_info,
    inputs=gr.Textbox(label="Enter URL", placeholder="https://example.com"),
    outputs=gr.Textbox(label="Output")
)

# use domain.py


if __name__ == "__main__":
    demo.launch()