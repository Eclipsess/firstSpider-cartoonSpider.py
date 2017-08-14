title= []
href = []
def get_keyword_page(current_url,title, href):
    '''递归调用网站链接名所有带“通知”二字的链接'''
    response = requests.get(current_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'html.parser')
    if soup.select('a') != None :
        for item in soup.select('a'):
            if '通知' in item.text:
                if item['href'][0:4] == 'http':
                    title.append(item.text.strip())
                    href.append(item['href'])
                    print(item.text.strip(),item['href'])
                    get_keyword_page(item['href'],title, href)
                else:
                    title.append(item.text.strip())
                    href.append(current_url[:-1]+item['href'])
                    print(item.text.strip(),current_url[:-1]+item['href'])
                    get_keyword_page(current_url[:-1]+item['href'],title, href)
    for turple in zip(title,href):
        print (turple)
    print('返回zip(titile,href)迭代器')
    return zip(title,href)
