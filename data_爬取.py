import requests
import time
import random

#https://fe-api.zhaopin.com/c/i/sou?start=90&pageSize=90&cityId=489&workExperience=-1&education=-1&companyType=-1
#&employmentType=-1&jobWelfareTag=-1&kw=JAVA%E5%BC%80%E5%8F%91&kt=3&=2001&at=65184d91b8214a5295518713d55903c1
#&rt=c335788de08e4a6c9c7359dea0c15f80&_v=0.77728626&userCode=1021480743&x-zp-page-request-id=77032d662a0e41299828275c286df298-1545722424963-430574

fileName = input("请输入文件名：")
file_handle = open('%s.txt' % (fileName), mode='r+', encoding='utf-8')
kw = input("请输入需要搜索的职位：")
for i in range(0, 9000, 90):
#先读取文件，防止上一循环的文件数据被清空
    file_handle.readline()
# 设置变化参数
    url = 'https://fe-api.zhaopin.com/c/i/sou?%s&pageSize=90&cityId=489&workExperience=-1&education=-1' \
          '&companyType=-1&employmentType=-1&jobWelfareTag=-1&%s%%E5%%BC%%80%%E5%%8F%%91&kt=3&=2001' \
          '&at=65184d91b8214a5295518713d55903c1&rt=c335788de08e4a6c9c7359dea0c15f80&_v=0.77728626' \
          '&userCode=1021480743&x-zp-page-request-id=77032d662a0e41299828275c286df298-1545722424963-430574' \
          % ('start=' + str(i), 'kw=' + kw)
# 获取数据
    response = requests.get(url).text
# 每页休眠，防止反爬
    if i/90 % 2 == 0:
        time.sleep(random.randint(5, 20))
    file_handle.write(response)
    print(response)
#关闭文件
file_handle.close()


