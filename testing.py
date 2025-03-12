import requests
from dataset import load_dataset

dataset = load_dataset("random_legit.txt")
dataset = dataset[:500]
status = []
for idx, url in enumerate(dataset):
    print(f"Analyzing URL {idx+1}/{len(dataset)}: {url}")
    try:
        response = requests.get(url, timeout=5)
        status.append(response.status_code)
    except requests.exceptions.RequestException as e:
        print(f"Could not reach the page: {e}")
        status.append(None)
with open("status.txt", "w", encoding="utf-8") as file:
    for s in status:
        file.write(str(s) + "\n")
