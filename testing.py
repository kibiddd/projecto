import requests
from dataset import load_dataset
from eval import load

dataset = load_dataset("random_legit.txt")
dataset = dataset[:500]
path = 'legit-250311/'
status = []
for idx, url in enumerate(dataset):
    domain_info_path = path + str(idx) + ".txt"
    domain_info = load(domain_info_path)
    # find streamline cancelled in domain_info
    if "cancelled" in domain_info:
        status.append(idx)
print(status)