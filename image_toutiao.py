import json
import re
from urllib.parse import urlencode
from hashlib import md5
import os
import requests
import pymongo
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from config import *
from multiprocessing import Pool
from json.decoder import JSONDecodeError
#不会MONGODB
#成功声明MONGODB对象
client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]

#网易云课堂Python3爬虫三大案例
#1.分析Ajax抓取今日头条街拍美图

#今日头条网站输入关键字：街拍，选择图集

def get_page_index(offset, keyword):
    #在XHR中 offset Headers 最下方数据，与该offset的url相同
    #由于是Ajax格式不是html不能使用BeautifulSoup等
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3
    }
    #urlencode自动编码 相当于offset的url：
    # http://www.toutiao.com/search_content/?offset=0
    # &format=json&keyword=%E8%A1%97%E6%8B%8D
    # &autoload=true&count=20&cur_tab=3
    url = 'http://www.toutiao.com/search_content/?' + urlencode(data)
    #若status_code == 200 代表请求成功
    try:
        response = requests.get(url)
        #返回结果就是检查中 Response 选项里的内容
        #json格式
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("请求索引页出错")
        return None

def parse_page_index(html):
    try:
        #json.loads转换
        data = json.loads(html)
        #保证json数据含有data属性
        #data.keys返回所有json的键
        if data and 'data' in data.keys():
            for item in data.get('data'):
                #yield构造一个生成器
                yield item.get('article_url')
    #可能为空报错
    except JSONDecodeError:
        pass

def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            #一开始此处忘加text了导致返回错误
            return response.text
        return None
    except RequestException:
        print('请求页出错', url)
        return None

def parse_page_details(html,url):
    #内页可以html直接提取，doc中可以查看，可以用BeutifulSoup
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()
    print(title)
    #匹配gallery后面的json格式,与视频不同，头条应该是改了gallery这的格式，学一下正则表达式即可
    images_pattern = re.compile('gallery: (.*?"]}),', re.S)
    result = re.search(images_pattern, html)
    if result:
        #匹配第一个()中的内容
        #print(result.group(1))查看具体的json格式信息
        data = json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            #sub_images是列表形式，里面包含字典还有key'url'
            sub_images = data.get('sub_images')
            #构造列表对象
            images = [item.get('url') for item in sub_images]
            #添加下载图片程序
            for image in images:
                download_image(image)
            return{
                'title':title,
                'url':url,
                'images':images
            }

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到mongodb成功',result)
        return True
    return False

def download_image(url):
    print('正在下载',url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            #content返回二进制内容，text返回网页正常内容
            save_image(response.content)
        return None
    except RequestException:
        print('请求图片出错', url)
        return None

def save_image(content):
    #getcwd获取当前路径 md5校验防止重复下载
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    #判断是否存在
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()



def main(offset):
    html = get_page_index(offset, KEYWORD)
    #parse_page_index(html)由于有yield是一个generator对象，返回iterable对象
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_details(html, url)

            #不会用mongodb，显示mongodb由于计算机积极拒绝，无法连接
############if result : save_to_mongo(result)
            #print(result)

if __name__ == '__main__':
    #main()
    #对main循环，offset为0 20 40 等
    #每组20个，实现 0 20 40 60
    groups = [x*20 for x in range(GROUP_START,GROUP_END + 1)]
    #开启多进程
    #最后没有存储到mongodb中，注释掉了140行
    pool = Pool()
    pool.map(main, groups)
