import pandas as pd
from pyecharts import Line, Bar, Page

df = pd.read_csv('tb_comments.csv', encoding='utf-8')

page = Page()
#创建评论数与日期的折线统计图
df['cmntcount'] = int(df.shape[0]) - df['No']
df['date_ymd'] = df['date'].apply(lambda x: x.split(' ')[0])
df_ymdcount= df.groupby('date_ymd')['cmntcount'].count()

line = Line('每日评论数统计')
line.add("日期", df_ymdcount.index, df_ymdcount.values, line_type='dotted', xaxis_interval=3, xaxis_rotate=-30)
#line.render(path="每日评论数变化.html")

#创建评论数与日期的条形统计图
bar = Bar('每日评论数统计')
bar.add("日期", df_ymdcount.index, df_ymdcount.values, grid_height=900, is_label_show=True, xaxis_interval=3,
        xaxis_rotate=-30)
#bar.render(path="评论数随日期变化条形图.html")
page.add(line)
page.add(bar)
page.render(path="销量走势.html")

