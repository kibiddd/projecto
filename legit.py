import pandas as pd

dataset = pd.read_csv('Fraudulent_online_shops_dataset.csv')

# extract only Label=legitimate
dataset = dataset[dataset['Label'] == 'legitimate']

# extract Online shop URL to list
online_shop_urls = dataset['Online shop URL'].tolist()

# write out to file
with open('legitimate_online_shop_urls.txt', 'w') as f:
    for url in online_shop_urls:
        f.write(url + '\n')
