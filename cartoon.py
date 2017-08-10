import requests
from bs4 import BeautifulSoup as bs
import pandas as pd




# news_total = []
# soup = bs(res.text,'html.parser')
# for news in soup.select('.li_img_de'):
#     result = {}
#     result['h3'] = news.select('h3')[0].text
#     result['time'] = news.select('.head_con_p_o')[0]('span')[0].text
#     result['author'] = news.select('.head_con_p_o')[0]('span')[1].text
#     result['href'] = news.select('a')[0]['href']
#     news_total.extend(result)



def getNewsDetail(newsurl):
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    soup = bs(res.text, 'html.parser')
    news_total = []
    for news in soup.select('.li_img_de'):
        result = {}
        result['time'] = news.select('.head_con_p_o')[0]('span')[0].text
        result['h3'] = news.select('h3')[0].text
        result['author'] = news.select('.head_con_p_o')[0]('span')[1].text
        result['href'] = news.select('a')[0]['href']
        #print (result)
        news_total.append(result)
    return news_total

newsURL ='https://news.dmzj.com/manzhanqingbao/p{}.html'
news_sum = []
for i in range(1,5):
    news_url = newsURL.format(i)
    newsary = getNewsDetail(news_url)
    news_sum.extend(newsary)
columns = ['time','h3','author','href']
df = pd.DataFrame(news_sum,columns=columns)
df.to_excel("C:\\Users\\Administrator\\Desktop\\test.xlsx",encoding="utf_8_sig",index=False,columns=columns)
print(df)


