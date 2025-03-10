from dataset import load_dataset
from domain import domain_analysis
from transformers import pipeline

def load_txt(path):
    with open(path, 'r') as f:
        return f.read()

def anal_domain(pipe, path, url):
    text = load_txt(path)
    domain_result = domain_analysis(pipe, url, text)
    # remove .txt from path
    path = path[:-4]
    with open(path + '_dom.txt', 'w') as f:
        f.write(domain_result)
    print(domain_result)
    return domain_result

def all_anal_domain(path):
    pipe = pipeline("text-generation", model="microsoft/Phi-4-mini-instruct", trust_remote_code=True)
    urls = load_dataset(path)
    prefix = 'phish-250309/'
    for idx, u in enumerate(urls):
        print(f'Analysing {idx}/{len(urls)-1}, url={u}')
        txt_path = prefix + str(idx) + '.txt'
        return anal_domain(pipe, txt_path, u)



if __name__ == '__main__':
    all_anal_domain('phishing-links-250309.txt')