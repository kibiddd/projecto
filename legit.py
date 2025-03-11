import pandas as pd

dataset = pd.read_csv('URL dataset.csv')

# extract only Label=legitimate
dataset = dataset[dataset['type'] == 'legitimate']

# extract Online shop URL to list
online_shop_urls = dataset['url'].tolist()

# write out to file
with open('legitimate_urls.txt', 'w') as f:
    for url in online_shop_urls:
        f.write(url + '\n')
