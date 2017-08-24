import requests
import re
import urllib.parse
from bs4 import BeautifulSoup

keyword = '吉林省科技厅'
baidu_url = 'http://www.baidu.com/s?wd='+urllib.parse.quote(keyword)

# soup = BeautifulSoup(res.text)
def recompile_parse_one_page(html):
    pattern = re.compile('<h3 class="t"><a.*?href = "(.*?)".*?target="_blank"', re.S)
    items = re.findall(pattern, html)
    return items
    #print(items)

#url = 'http://www.baidu.com/link?url=AEY_aTkV3bUN_g46Nd7CF58pJcIsuusvA0bKqMjML0nsoUg3VUOEOiFAvR3vuFKbJ4ofvMKTvU_-GKHdnJQdwuCtTFW10s-tn6LgDYsoJga'
def get_realurl(url):
    try:
        temp = requests.get(url.rstrip(),timeout = 10)
        tempurl = temp.url
        print('get  '+ url + ',  real url is : '+ tempurl)
        return tempurl
    except requests.exceptions.Timeout:
          print ("Timeout occurred")

def get_content(html):
    soupitemss = []
    soup = BeautifulSoup(html,'html.parser')
    for item in soup.select('.t a'):
        soupitems = {}
        soupitems['title'] = item.text
        soupitems['href'] = item['href']
        soupitemss.append(soupitems)
    return soupitemss

def get_keyword_page(current_url):
    inside_title = []
    inside_href = []
    '''递归调用网站链接名所有带“通知”二字的链接'''
    response = requests.get(current_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'html.parser')
    if soup.select('a') != None :
        for item in soup.select('a'):
            if '通知' in item.text :
                if item['href']!= current_url and current_url[:-1]+item['href'].strip('.')!=current_url:
                    if item['href'][0:4] == 'http' and item['href']!= current_url:
                        inside_title.append(item.text.strip())
                        inside_href.append(item['href'])
                        print(item.text.strip(),item['href'])
                        get_keyword_page(item['href'])
                    else:
                        inside_title.append(item.text.strip())
                        inside_href.append(current_url[:-1]+item['href'].strip('.'))
                        print(item.text.strip(),current_url[:-1]+item['href'].strip('.'))
                        get_keyword_page(current_url[:-1]+item['href'].strip('.'))
    for turple in zip(inside_title,inside_href):
        print (turple)
    print('返回zip(titile,href)迭代器')
    return zip(inside_title,inside_href)

resbaidu = requests.get(baidu_url)
#resulturl = recompile_parse_one_page(resbaidu.text)

result = get_content(resbaidu.text)

i = 0
resultBaidu = []
for urllink in result:
    realurl = get_realurl(urllink['href'])
    #variable = requests.get(realurl)
    i = i + 1
    #remove baike.baidu.com
    if realurl[:24] == 'https://baike.baidu.com/' or realurl[:22] == 'http://map.baidu.com/':
        continue
    else:
        resultBaidu.append([urllink['title'], realurl])
        print(i)
print(resultBaidu)
final = []
for item in resultBaidu:
    final.append(get_keyword_page(item[1]))
result_tocsv = []
for item in final:
    for res in item:
        result_tocsv.append(list(res))
print(result_tocsv)

import pandas as pd
df = pd.DataFrame(result_tocsv)
df.to_csv('result.csv')
print('保存到当前目录result.csv文件中')
    # print(variable.text)
