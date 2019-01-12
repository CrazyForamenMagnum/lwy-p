import requests
import random
import time
from fake_useragent import UserAgent

ua = UserAgent()
file_handle = open('response1.txt', mode='r+', encoding='utf-8')
#创建用于存取数组的dataframe
#comments = pd.DataFrame(columns=['Page', 'cmntlist'])
#tb_contents = pd.DataFrame(columns=['nick', 'rank', 'sku', 'content'])
#ip = ['183.47.2.201:30278', '123.156.40.140:80', '36.33.32.158:59019','61.183.176.122:53281', '124.167.113.99:80', '117.21.191.154:32431','111.72.154.38:53128', '175.148.79.43:1133', '115.46.73.213:8123', '114.119.116.92:61066']
for i in range(2, 4):
    #先读取文件，防止上一循环的文件数据被清空
    file_handle.read()
    #t = str(time.time() * 1000)
    # 设置变化参数
    currentPage = i + 1
    url = 'https://rate.taobao.com/feedRateList.htm?auctionNumId=546651887101%s' % \
          ('&currentPageNum=' + str(currentPage))
    #设置代理ip
    # 获取数据
    #choice = random.choice(ip)
    #proxies = {"http": "http://"+choice, "https": "https://"+choice}
    headers = {"User-Agent": ua.random}
    #print(proxies)
    response = requests.get(url, headers=headers).text

    # response.to_csv('response.csv', encoding='utf-8')
    #print(response)
    '''
    globals = {
        'true': 0,
        'false': 0,
        'null': 0
    }
    diction = eval(response[1: -1], globals)
    cmntlist = diction["comments"]
    comments = comments.append({'Page': currentPage, 'cmntlist': cmntlist}, ignore_index=True)
    for cmnt in cmntlist:
        nick = cmnt["user"]["nick"]
        rank = cmnt["user"]["rank"]
        sku = cmnt["auction"]["sku"]
        content = cmnt["content"]
        tb_contents = tb_contents.append({'nick': nick, 'rank': rank, 'sku': sku, 'content': content},
                                         ignore_index=True)'''
    # 每页休眠，防止反爬
    if currentPage % 1 == 0:
        time.sleep(random.randint(5, 20))
    file_handle.write(response)
#print(tb_contents.values)
file_handle.close()  #关闭文件


#comments.to_csv('tb_comments.csv', encoding='utf-8')

