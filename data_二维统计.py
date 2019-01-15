import pandas as pd
from pyecharts import Page, Bar, Scatter, Line
import numpy as np

df_job = pd.read_csv('data/response_JAVA_cleaned.csv', encoding='utf-8')
page_axis2 = Page()
def toint(value):
    value = int(value)
    return value

#数据清洗
df_job = df_job[~df_job['avg_salary'].isin([125000])]
df_job = df_job[~df_job['avg_salary'].isin([0])]
df_job = df_job[~df_job['company_name'].isin(['北京独创时代科技有限公司', '深圳市深为软件技术有限公司'])]
df_job = df_job[~df_job['company_loc'].isin(['武汉-洪山区'])]
#学历数据量化

level_list = []
for v in df_job['edu_level']:
    level = 0
    if v == '中专' or v == '中技' or v == '高中':
        level = 1
    elif v == '大专':
        level = 2
    if v == '本科':
        level = 3
    if v == '硕士':
        level = 4
    level_list.append(level)
print(level_list)
df_job['edu_level_toint'] = level_list


#公司类型->平均月薪
type_sal_avg = df_job.groupby('company_type')['avg_salary'].agg({"AVG": np.mean})
type_sal_avg['AVG'] = type_sal_avg['AVG'].apply(toint)
bar_type_sal = Bar("不同类型公司的平均月薪")
bar_type_sal.add("公司类型", type_sal_avg.index, type_sal_avg['AVG'], is_label_show=True,  xaxis_interval=0,
                 xaxis_rotate=-45)

#不同工作城市->平均月薪
city_sal = df_job.groupby('company_city')['avg_salary'].agg({"AVG": np.mean})
city_sal['AVG'] = city_sal['AVG'].apply(toint)
city_sal = city_sal.sort_values(by=['AVG'], ascending=True)
bar_city_sal = Bar("工作城市对应的平均工资", title_pos='center', width=2000)
bar_city_sal.add("", city_sal.index, city_sal['AVG'], xaxis_interval=0, xaxis_rotate=-45)

#工作经验->平均月薪
exp_sal_avg = df_job.groupby('work_exp')['avg_salary'].agg({"AVG": np.mean})
exp_sal_avg['AVG'] = exp_sal_avg['AVG'].apply(toint)
exp_sal_avg = exp_sal_avg.sort_values(by="AVG", ascending=True)
bar_exp_sal = Bar("不同工作经验对应的平均月薪")
bar_exp_sal.add("工作经验", exp_sal_avg.index, exp_sal_avg['AVG'], is_label_show=True,  xaxis_interval=0,
                 xaxis_rotate=-45)
exp_sal_avg = exp_sal_avg[~exp_sal_avg.index.isin(['不限'])]
line_exp = Line("工作经验与月薪的关系")
line_exp.add("工作经验", exp_sal_avg.index, exp_sal_avg['AVG'], is_label_show=True)



#学历->月薪
edu_sal_min = df_job.groupby('edu_level')['avg_salary'].min()
edu_sal_mean = df_job.groupby('edu_level')['avg_salary'].agg({"MEAN": np.mean})
edu_sal_mean['MEAN'] = edu_sal_mean['MEAN'].apply(toint)
edu_sal_max = df_job.groupby('edu_level')['avg_salary'].max()
bar_edu = Bar("学历对月薪的影响")
bar_edu.add("最小值", edu_sal_min.index, edu_sal_min.values, is_label_show=True)
bar_edu.add("平均值", edu_sal_min.index, edu_sal_mean['MEAN'], is_label_show=True)
bar_edu.add("最大值", edu_sal_min.index, edu_sal_max.values, is_label_show=True)


scatt_edu_sal = Scatter("学历与月薪的关系/0-不限/1-中专/2-大专/3-本科/4-研究生", height=1200, width=1000)
scatt_edu_sal.add("学历", df_job['edu_level_toint'], df_job['avg_salary'])

page_axis2.add(bar_type_sal)
page_axis2.add(bar_exp_sal)
page_axis2.add(bar_edu)
page_axis2.add(scatt_edu_sal)
page_axis2.add(bar_city_sal)
page_axis2.add(line_exp)
page_axis2.render(path="二维数据分析_cleaned.html")

