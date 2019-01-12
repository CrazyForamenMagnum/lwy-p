from snownlp import SnowNLP
import pandas as pd
import jieba.analyse
import numpy as np
#from pyecharts import WordCloud

df = pd.read_csv('tb_comments.csv', encoding='utf-8')
'''
def setiment(content):
    s = SnowNLP(content)
    return s.sentiments
df['setiment'] = df['content'].apply(setiment)

df_sent = df[['content', 'setiment']]
df_sent.sort_values(by=['setiment'])
print(df['setiment'])
#为商品打分
rank_list = df['rank'].values.tolist()
max_rank = max(rank_list)
Grade = []

rank = 0
self_grade = 0
good_grade = 0
len = df.shape[0]
for index, row in df.iterrows():
    rank = row['rank']/max_rank
    self_grade = row[7]*rank*100
    Grade.append(self_grade)
good_grade = sum(Grade)/len
print("该商品综合分数为：", good_grade)
'''

#all_content = df['content'].values.tolist()
#print(df_sent)
'''
#基于 TF-IDF 算法的关键词抽取
extract_tags = jieba.analyse.extract_tags(' '.join(all_content), topK=200, withWeight=True, allowPOS=('ns', 'n'))
#print(extract_tags)
#基于textrank的关键词抽取
textrank = jieba.analyse.textrank(' '.join(all_content), topK=200, withWeight=True, allowPOS=('ns', 'n'))
#print(textrank)
'''
#高频词统计
all_content = df['content'].tolist()
segments = []
for line in all_content:
    try:
        segs = jieba.lcut(line)
        for seg in segs:
            if len(seg) > 1 and seg !='\r\n':
                segments.append(seg)
            print(seg)
    except:
        print(line)
        continue

words_df = pd.DataFrame({"segment": segments})

words_stat = words_df.groupby('segment')['segment'].agg({"计数": np.size})   #加了一列
words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)

#词云图
wordc = WordCloud(width=800, height=520)
wordc.add("评论词云", words_stat['segment'], words_stat['计数'], word_size_range=[20, 100])
wordc.render(path="评论词云.html")


