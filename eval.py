from dataset import load_dataset
from domain import domain_analysis
from cont import content_analysis
from url import url_analysis
from transformers import pipeline
from combine import combine

def load_txt(path):
    with open(path, 'r') as f:
        return f.read()

def all_anal_url(dataset_path, save_path, start=0, end=-1):
    pipe = pipeline("text-generation", model="microsoft/Phi-4-mini-instruct", trust_remote_code=True)
    dataset = load_dataset(dataset_path)
    dataset = dataset[start:end]
    for idx, u in enumerate(dataset):
        print(f'Analysing {idx+1}/{len(dataset)}, url={u}')
        result_url = url_analysis(u, pipe)
        new_path = save_path + str(idx) + '_url.txt'
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

def anal_cont(url, image_path, folder_path):
    content_result = content_analysis(url, image_path)
    if content_result is None:  # Check if content_result is invalid
        print(f"Warning: content_analysis returned None for url={url} and image_path={image_path}")
        return None  # Skip further processing
    new_path = folder_path + '_cont.txt'
    with open(new_path, 'w') as f:
        f.write(content_result)
    print(content_result)
    return content_result


def all_anal_cont(dataset_path, img_path, folder_path):
    urls = load_dataset(dataset_path)
    urls = urls[280:500]
    images = load_dataset(img_path)
    images = images[280:500]
    for idx, u in enumerate(urls):
        image = images[idx]
        idx += 280
        print(f'Analysing {idx}/{len(urls) - 1}, url={u}')
        img_path = folder_path + str(idx)
        anal_cont(u, image, img_path)

# function to load n_cont.txt
def load(path):
    with open(path, 'r') as f:
        return f.read()

# function to load all
def eval_combine(dataset_path, folder_path):
    dataset = load_dataset(dataset_path)
    pipe = pipeline("text-generation", model="microsoft/Phi-4-mini-instruct", trust_remote_code=True)

    for idx, u in enumerate(dataset[92:]):
        idx += 92
        print(f'Analysing {idx}/{len(dataset) - 1}, url={u}')
        url_path = folder_path + str(idx) + '_url.txt'
        url_result = load(url_path)
        domain_path = folder_path + str(idx) + '_dom.txt'
        domain_result = load(domain_path)
        content_path = folder_path + str(idx) + '_cont.txt'
        content_result = load(content_path)
        # print(f'url={u}, url_result={url_result}, domain_result={domain_result}, content_result={content_result}')
        combine_anal = combine(u, url_result, domain_result, content_result, pipe)
        combine_path = folder_path + str(idx) + '_combine.txt'
        with open(combine_path, 'w') as f:
            f.write(combine_anal)


if __name__ == '__main__':
    all_anal_url('random_legit.txt', 'legit-250311/', 0, 500)
    # all_anal_cont('random_legit.txt', 'ss-legit.txt', 'legit-250311/')
    #eval_combine('phishing-links-250309.txt', 'phish-250309/')