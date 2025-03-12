from dataset import load_dataset
from domain import domain_analysis
from cont import content_analysis
from url import url_analysis
from transformers import pipeline
from combine import combine
import json

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
    with open(path, 'r', encoding='utf-8') as f:  # Specifying utf-8 encoding
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

def get_verdict(dataset_path, folder_path, start=0, end=-1):
    scores = []
    dataset = load_dataset(dataset_path)
    dataset = dataset[start:end]
    for idx, u in enumerate(dataset):
        path = folder_path + str(idx) + '_combine.txt'
        print(f'Analysing {idx+1}/{len(dataset)}, url={u}')
        # try loading the txt file in path
        try:
            # Open and read the file
            with open(path, 'r') as file:
                # Read contents and strip unnecessary whitespace
                contents = file.read().strip()

                # If the file contains backticks or non-JSON parts, remove them
                if contents.startswith('```json') and contents.endswith('```'):
                    contents = contents[7:-3].strip()

                # Parse the contents as JSON
                data = json.loads(contents)
                # append verdict
                scores.append(data['verdict'])
        except FileNotFoundError:
            print(f"Error: File not found at {path}")
            scores.append(None)
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON. {e}")
            scores.append(None)
        except Exception as e:
            print(f"Error: {e}")
            scores.append(None)

    return scores

def count_verdict(scores):
    count = {}
    for v in scores:
        if v in count:
            count[v] += 1
        else:
            count[v] = 1
    return count

def get_false_positive(scores):
    false_positive = []
    nones = []
    for idx, s in enumerate(scores):
        if s:
            if int(s) >= 7:
                false_positive.append(idx)
        else:
            nones.append(idx)
    return false_positive, nones

def get_classification(scores):
    classifications = []
    for s in scores:
        if s >= 7:
            classifications.append('Scam')
        elif s >= 4:
            classifications.append('Suspicious')
        else:
            classifications.append('Legit')
    return classifications

if __name__ == '__main__':
    verdicts = get_verdict('phishing-links-250309.txt', 'phish-250309/', 0, 500)
    print(len(verdicts))
    print(count_verdict(verdicts))
    # fps, nones = get_false_positive(verdicts)
    # print(fps)
    # print(nones)
    # all_anal_url('random_legit.txt', 'legit-250311/', 0, 500)
    # all_anal_cont('random_legit.txt', 'ss-legit.txt', 'legit-250311/')
    #eval_combine('phishing-links-250309.txt', 'phish-250309/')