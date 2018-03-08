import urllib.request
from bs4 import BeautifulSoup
import time
import os
import dryscrape
import sys
import pandas as pd

def crawl(url):
    elems = url.split('http://')
    if len(elems) == 2:
        root = elems[1].split('/')[0]
    else:
        elems = url.split('https://')
        if len(elems) == 2:
            root = elems[1].split('/')[0]
        else:
            root = url.split('/')[0]
        '''
        if root == "boomup.chosun.com":
            continue
        '''
    session = dryscrape.Session()
    session.visit(url)
    response = session.body()
    soup = BeautifulSoup(response, 'lxml')
    for script in soup(['script', 'style']):
        script.extract()

    rawArticle = soup.find('div', {'id':'articleBodyContents'})
    article = rawArticle.get_text()
    article = article.replace('\t', '')
    article = article.replace('\n', '')

    likeCounts = soup.find_all('span', {'class' : 'u_likeit_list_count _count'})

    i = 1
    counts = []
    for likeCount in likeCounts:
        if i == 6:
            break
        elif i == 1:
            counts.append(likeCount.string)
        elif i == 2:
            counts.append(likeCount.string)
        elif i == 3:
            counts.append(likeCount.string)
        elif i == 4:
            counts.append(likeCount.string)
        elif i == 5:
            counts.append(likeCount.string)
        i += 1
    if root == "http://sports.news.naver.com/":
        warm = counts[0]
        sad = counts[1]
        angry = counts[2]
        like = counts[3]
        neutral = counts[4]
    else:
        like = counts[0]
        warm = counts[1]
        sad = counts[2]
        angry = counts[3]
        neutral = counts[4]

    if like >= warm and like >= sad and like >= angry and like >= neutral:
        return "like"
    elif warm >= like and warm >= sad and warm >= angry and warm >= neutral:
        return "warm"
    elif sad >= like and sad >= warm and sad >= angry and sad >= neutral:
        return "sad"
    elif angry >= like and angry >= warm and angry >= sad and angry >= neutral:
        return "angry"
    elif neutral >= like and neutral >= warm and neutral >= sad and neutral >= angry:
        return "neutral"


if __name__ == '__main__':

    file_list = []
    foldername = './data'

    for path, dirs, files in os.walk(foldername):
        if files:
            for filename in files:
                fullname = os.path.join(path, filename)
                file_list.append(fullname)

    for file in file_list:
        section = file.split('/')[1]
        classname = file.split('/')[2]
        subclass = file.split('/')[3].split('.')[0]

        df = pd.read_csv(file, encoding='utf-8')
        selected = ['urls', 'body']
        url_list = df[selected[0]].tolist()
        body_raw = df[selected[1]].tolist()

        if not os.path.isdir('Like_dataset/like'):
            os.mkdir('Like_dataset')
            os.mkdir('Like_dataset/like')
        if not os.path.isdir('Like_dataset/warm'):
            os.mkdir('Like_dataset/warm')
        if not os.path.isdir('Like_dataset/sad'):
            os.mkdir('Like_dataset/sad')
        if not os.path.isdir('Like_dataset/angry'):
            os.mkdir('Like_dataset/angry')
        if not os.path.isdir('Like_dataset/neutral'):
            os.mkdir('Like_dataset/neutral')
        j = 0
        for i in range(len(url_list)):
            result = crawl(url_list[i])
            if result == "like":
                fp = open('Like_dataset/like/'+str(j)+'.txt', 'w', encoding='utf-8')
                fp.write(str(body_raw[i]))
                fp.close()
            elif result == "warm":
                fp = open('Like_dataset/warm/'+str(j)+'.txt', 'w', encoding='utf-8')
                fp.write(str(body_raw[i]))
                fp.close()
            elif result == "sad":
                fp = open('Like_dataset/sad/'+str(j)+'.txt', 'w', encoding='utf-8')
                fp.write(str(body_raw[i]))
                fp.close()
            elif result == "angry":
                fp = open('Like_dataset/angry/'+str(j)+'.txt', 'w', encoding='utf-8')
                fp.write(str(body_raw[i]))
                fp.close()
            elif result == "neutral":
                fp = open('Like_dataset/neutral/'+str(j)+'.txt', 'w', encoding='utf-8')
                fp.write(str(body_raw[i]))
                fp.close()
            j += 1
