import urllib.request
from bs4 import BeautifulSoup
import time
import dryscrape


def crawl(url):
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
        if i == 5:
            break
        elif i == 1:
            counts.append(likeCount.string)
        elif i == 2:
            counts.append(likeCount.string)
        elif i == 3:
            counts.append(likeCount.string)
        elif i == 4:
            counts.append(likeCount.string)
        i += 1

    like = counts[0]
    warm = counts[1]
    sad = counts[2]
    angry = counts[3]

    if like >= warm and like >= sad and like >= angry:
        return "like"
    elif warm >= like and warm >= sad and warm >= angry:
        return "warm"
    elif sad >= like and sad >= warm and sad >= angry:
        return "sad"
    elif angry >= like and angry >= warm and angry >= sad:
        return "angry"


if __name__ == '__main__':
    url = "http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=100&oid=028&aid=0002401439"

    result = crawl(url)
    print(result)

