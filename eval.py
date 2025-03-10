from dataset import load_dataset
from domain import domain_analysis

def load_txt(path):
    with open(path, 'r') as f:
        return f.read()

def anal_domain(path, url):
    text = load_txt(path)
    domain_result = domain_analysis(url, text)
    # remove .txt from path
    path = path[:-4]
    with open(path + '_dom.txt', 'w') as f:
        f.write(domain_result)
    print(domain_result)
    return domain_result


if __name__ == '__main__':
    url = load_dataset('phishing-links-250309.txt')
    info = anal_domain('phish-250309/0.txt', url[0])
    print(info)