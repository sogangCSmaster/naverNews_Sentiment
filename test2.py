import pandas as pd
import os
import sys



csv_file = 'news_7a5_20180101.csv'
df = pd.read_csv(csv_file, encoding='utf-8')

selected = ['urls', 'body']

url_raws = df[selected[0]].tolist()
body_raws = df[selected[1]].tolist()


for url in df['urls']:
    print(url)
