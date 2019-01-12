import pandas as pd
import json

file = open('response1.txt', mode='r', encoding='utf-8')
tb_contents = pd.DataFrame(columns=['No', 'date', 'nick', 'rank', 'sku', 'content'])
for i in range(0, 97):
    response = file.readline()
    if response.startswith(u'\ufeff'):
        response = response.encode('utf8')[3:].decode('utf8')
    globals = {
        'true': 0,
        'false': 0,
        'null': 0
    }
    dict = json.loads(response)  #字符串->dict
    cmntlist = dict["comments"]
    print(dict["currentPageNum"])
    for cmnt in cmntlist:
        #j = cmnt.index+1
        #No = i*20 + j
        date = cmnt["date"]
        nick = cmnt["user"]["nick"]
        rank = cmnt["user"]["rank"]
        sku = cmnt["auction"]["sku"]
        content = cmnt["content"]
        tb_contents = tb_contents.append({'No': len(tb_contents)+1, 'date': date, 'nick': nick, 'rank': rank, 'sku': sku, 'content': content},
                                         ignore_index=True)
print(tb_contents.values)
tb_contents.to_csv('tb_comments.csv', encoding='utf_8_sig')