import requests
import re
import urllib.parse
from bs4 import BeautifulSoup

keyword = '待搜索内容'
baidu_url = 'http://www.baidu.com/s?wd='+urllib.parse.quote(keyword)

# soup = BeautifulSoup(res.text)
def recompile_parse_one_page(html):
    pattern = re.compile('<h3 class="t"><a.*?href = "(.*?)".*?target="_blank"', re.S)
    items = re.findall(pattern, html)
    return items
    #print(items)

#url = 'http://www.baidu.com/link?url=AEY_aTkV3bUN_g46Nd7CF58pJcIsuusvA0bKqMjML0nsoUg3VUOEOiFAvR3vuFKbJ4ofvMKTvU_-GKHdnJQdwuCtTFW10s-tn6LgDYsoJga'
def get_realurl(url):
    temp = requests.get(url.rstrip())
    tempurl = temp.url
    print('get  '+ url + ',  real url is : '+ tempurl)
    return tempurl

def get_content(html):
    soupitemss = []
    soup = BeautifulSoup(html,'html.parser')
    for item in soup.select('.t a'):
        soupitems = {}
        soupitems['title'] = item.text
        soupitems['href'] = item['href']
        soupitemss.append(soupitems)
    return soupitemss

resbaidu = requests.get(baidu_url)
#resulturl = recompile_parse_one_page(resbaidu.text)

result = get_content(resbaidu.text)

i = 0
for urllink in result:
    realurl = get_realurl(urllink['href'])
    #variable = requests.get(realurl)
    i = i + 1
    print(i , urllink['title'] , realurl)
   # print(variable.text)
