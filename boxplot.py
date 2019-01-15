import pandas as pd
from pyecharts import Page, Boxplot
import numpy as np

df_job = pd.read_csv('data/response_JAVA_cleaned.csv', encoding='utf-8')
page = Page()
def toint(value):
    value = int(value)
    return value

#数据清洗
df_job = df_job[~df_job['avg_salary'].isin([125000])]
df_job = df_job[~df_job['avg_salary'].isin([0])]
df_job = df_job[~df_job['company_name'].isin(['北京独创时代科技有限公司', '深圳市深为软件技术有限公司'])]
df_job = df_job[~df_job['company_loc'].isin(['武汉-洪山区'])]

#工作经验->月薪 boxplot
x_axis = ['不限', '无经验', '1年以下', '1-3年', '3-5年', '5-10年', '10年以上']
exp_random = []
exp_none = []
exp_1 = []
exp_1_3 = []
exp_3_5 = []
exp_5_10 = []
exp_10 = []
for i, j in zip(df_job['work_exp'], df_job['avg_salary']):
    if i == '不限':
        exp_random.append(j)
    elif i == '无经验':
        exp_none.append(j)
    elif i == '1年以下':
        exp_1.append(j)
    elif i == '1-3年':
        exp_1_3.append(j)
    elif i == '3-5年':
        exp_3_5.append(j)
    elif i == '5-10年':
        exp_5_10.append(j)
    elif i == '10年以上':
        exp_10.append(j)
data_exp = [exp_random, exp_none, exp_1, exp_1_3, exp_3_5, exp_5_10, exp_10]
boxplot_exp = Boxplot("JAVA开发岗——工作经验与薪酬的关系", title_pos='center', title_top='18', width=800, height=400)
y_axis = boxplot_exp.prepare_data(data_exp)
boxplot_exp.add("", x_axis, y_axis)

#六个城市->月薪盒图
city_x_axis = ['深圳', '北京', '上海', '成都', '郑州', '广州']
sz = []
bj = []
sh = []
cd = []
zz = []
gz = []
for i, j in zip(df_job['company_city'], df_job['avg_salary']):
    if i == '深圳':
        sz.append(j)
    if i == '北京':
        bj.append(j)
    if i == '上海':
        sh.append(j)
    if i == '成都':
        cd.append(j)
    if i == '郑州':
        zz.append(j)
    if i == '广州':
        gz.append(j)
data_city = [sz, bj, sh, cd, zz, gz]
boxplot_city = Boxplot("工作城市及其相应月薪", title_pos='center', title_top='18', width=800, height=400)
city_y_axis = boxplot_city.prepare_data(data_city)
boxplot_city.add("", city_x_axis, city_y_axis)

#学历与工资的关系
edu_x_axis = ['不限', '高中', '大专', '本科', '硕士']
edu_ran = []
edu_high = []
edu_big = []
edu_udg = []
edu_phd = []
for i, j in zip(df_job['edu_level'], df_job['avg_salary']):
    if i == '不限':
        edu_ran.append(j)
    if i in ['中专', '中技']:
        edu_high.append(j)
    if i == '大专':
        edu_big.append(j)
    if i == '本科':
        edu_udg.append(j)
    if i == '硕士':
        edu_phd.append(j)
data_edu = [edu_ran, edu_high, edu_big, edu_udg, edu_phd]
boxplot_edu = Boxplot("不同学历的工作薪酬", title_pos='center', title_top='18', width=800, height=400)
edu_y_axis = boxplot_city.prepare_data(data_edu)
boxplot_edu.add("", edu_x_axis, edu_y_axis)
page.add(boxplot_exp)
page.add(boxplot_city)
page.add(boxplot_edu)
page.render("boxplot.html")