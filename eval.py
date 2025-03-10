from dataset import load_dataset
from domain import domain_analysis
from cont import content_analysis
from url import url_analysis
from transformers import pipeline

def load_txt(path):
    with open(path, 'r') as f:
        return f.read()

def all_anal_url(path):
    pipe = pipeline("text-generation", model="microsoft/Phi-4-mini-instruct", trust_remote_code=True)
    prefix = 'phish-250309/url_anal/'
    dataset = load_dataset(path)
    for idx, u in enumerate(dataset):
        print(f'Analysing {idx}/{len(dataset) - 1}, url={u}')
        result_url = url_analysis(u, pipe)
        new_path = prefix + str(idx) + '_url.txt'
        with open(new_path, 'w') as f:
            f.write(result_url)

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
        anal_domain(pipe, txt_path, u)

def anal_cont(url, image_path):
    content_result = content_analysis(url, image_path)
    new_path = image_path[:-4] + '_cont.txt'
    with open(new_path, 'w') as f:
        f.write(content_result)
    print(content_result)
    return content_result

def all_anal_cont(path):
    urls = load_dataset(path)
    prefix = 'phish-250309/'
    for idx, u in enumerate(urls[500:]):
        print(f'Analysing {idx+500}/{len(urls) - 1}, url={u}')
        img_path = prefix + str(idx+500) + '.png'
        anal_cont(u, img_path)


if __name__ == '__main__':
    all_anal_url('phishing-links-250309.txt')