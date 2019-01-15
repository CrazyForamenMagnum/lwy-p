import pandas as pd
import numpy as np
from pyecharts import WordCloud

df = pd.read_csv('data/response_JAVA_cleaned.csv')
wel = df['job_welfare'].tolist()
welfare = []
for w in wel:
    w = str(w)
    for ws in w.split(','):
        welfare.append(ws)
df_wel = pd.DataFrame({'welfare': welfare})
word_count = df_wel.groupby('welfare')['welfare'].agg({"计数": np.size})
word_count = word_count.reset_index().sort_values(by='计数', ascending=False)
word_count.head(20)

wc = WordCloud("待遇词云图", title_pos='center')
wc.add("", word_count['welfare'], word_count['计数'], word_size_range=[20, 70])
wc.render("待遇词云.html")