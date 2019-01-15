import pandas as pd
from pyecharts import Page, Bar, Pie, Geo
import numpy as np

# 读取文件
fileName = input("type your full document:")
df_job = pd.read_csv(fileName, encoding='utf-8')
df_job = df_job[~df_job['avg_salary'].isin([125000])]
df_job = df_job[~df_job['company_name'].isin(['北京独创时代科技有限公司', '深圳市深为软件技术有限公司'])]
df_job = df_job[~df_job['company_loc'].isin(['武汉-洪山区'])]

# 调用page实现多图一页显示
page_c = Page("招聘相关数据分析——JAVA开发岗位（智联招聘）")
# 公司规模统计（饼图
Csize_count = df_job.groupby('company_size')['No'].count()
pie_size = Pie("公司规模统计", width=1000)
pie_size.add("规模", Csize_count.index, Csize_count.values, is_label_show=True)

# 公司类型统计（条图
Ctype_count = df_job.groupby('company_type')['No'].count()
bar_type = Bar("公司类型")
bar_type.add("类型", Ctype_count.index, Ctype_count.values, is_label_show=True,  xaxis_interval=0, xaxis_rotate=-45)


#公司分布地图
city_count = df_job.groupby('company_city')['company_city'].count()
city_data = []
nocoordinate = ['日本', '澄迈', '西平', '黔西南']
for item in zip(city_count.index, city_count.values):
    if item[0] in nocoordinate:
        continue    #跳出循环：遇到不存在经纬度的城市跳过，不用存储到city_data
    city_data.append(item)
#print(city_data)
geo = Geo("公司城市分布情况", "data from ZHILIAN", title_color="#fff", title_pos="center", width=800, height=600,
          background_color='#404a59')
attr, value = geo.cast(city_data)
geo.add("城市分布情况", attr, value, visual_range=[0, 360], visual_text_color="#fff", symbol_size=10, is_visualmap=True)

#公司分布城市统计
#删除出现次数少于10次的城市
for index, value in city_count.items():
    if value < 10:
        city_count = city_count.drop(index)
    else:
        continue
bar_city = Bar("公司分布城市统计", width=1200)
bar_city.add("城市", city_count.index, city_count.values, is_label_show=True, xaxis_interval=0, xaxis_rotate=-45)

#不同学历的职位数目
edu_count = df_job.groupby('edu_level')['No'].count()
bar_edu = Bar("不同学历的职位数目")
bar_edu.add("学历", edu_count.index, edu_count.values, is_label_show=True, xaxis_interval=0, xaxis_rotate=-45)
pie_edu = Pie("学历需求占比")
pie_edu.add("学历", edu_count.index, edu_count.values, is_label_show=True)

#不同工作经验的需求
exp_count = df_job.groupby('work_exp')['No'].count()
bar_exp = Bar("不同经验的岗位需求")
bar_exp.add("经验", exp_count.index, exp_count.values, is_label_show=True, xaxis_interval=0, xaxis_rotate=-45)

# 公司平均工资分布（条图
def salary_division(salarylist):
    """先将工资分成9个区间"""
    s_4k = 0
    s_4_6k = 0
    s_6_8k = 0
    s_8_10k = 0
    s_10_12k = 0
    s_12_14k = 0
    s_14_16k = 0
    s_16_18k = 0
    s_18_20k = 0
    s_20k = 0
    df_salary_rank = pd.DataFrame(columns=['salary_rank', 'count'])
    df_salary_rank['salary_rank'] = ['<4K', '4~6K', '6~8K', '8~10K', '10~12K', '12~14K', '14~16K', '16~18K', '18~20K',
                                     '>20K']
    for s in salarylist:
        s = int(s)
        if s < 4000:
            s_4k += 1
        if s >= 4000 and s < 6000:
            s_4_6k += 1
        if s >= 6000 and s < 8000:
            s_6_8k += 1
        if s >= 8000 and s < 10000:
            s_8_10k += 1
        if s >= 10000 and s < 12000:
            s_10_12k += 1
        if s >= 12000 and s < 14000:
            s_12_14k += 1
        if s >= 14000 and s < 16000:
            s_14_16k += 1
        if s >= 16000 and s < 18000:
            s_16_18k += 1
        if s >= 18000 and s < 20000:
            s_18_20k += 1
        if s >= 20000:
            s_20k += 1
    df_salary_rank['count'] = [s_4k, s_4_6k, s_6_8k, s_8_10k, s_10_12k, s_12_14k, s_14_16k, s_16_18k, s_18_20k, s_20k]
    return df_salary_rank

df_job = df_job[~df_job['avg_salary'].isin([0])]
df = salary_division(df_job['avg_salary'])
bar_avgs = Bar("平均工资分布表")
bar_avgs.add("工资区间", df['salary_rank'], df['count'], is_label_show=True, xaxis_interval=0, xaxis_rotate=-45)


#将所有表加到同一页下显示
page_c.add(geo)
page_c.add(bar_city)
page_c.add(pie_size)
page_c.add(bar_type)
page_c.add(bar_avgs)
page_c.add(bar_edu)
page_c.add(pie_edu)
page_c.add(bar_exp)
page_c.render(path="公司相关数据分析_cleaned.html")
