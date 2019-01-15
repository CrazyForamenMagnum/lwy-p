import pandas as pd
import numpy as np

fileN = input("type your document:")
fileName = fileN+'.csv'
df_job = pd.read_csv(fileName, encoding='utf-8')

#由于薪酬格式是6k-8k，所以先进行分列->6k和8k各为一列，后将k去掉各自转换数据类型后乘以1000，计算平均工资
low_salary = []
high_salary = []
avg_salary = []
for s in df_job['job_salary']:
    if s == '薪资面议':
        low_s = np.nan
        high_s = np.nan
    else:
        low_s = s.split('-')[0].replace('K', '')
        high_s = s.split('-')[1].replace('K', '')
    low_s = float(low_s)*1000
    high_s = float(high_s)*1000
    avg_s = (low_s+high_s)/2
    low_salary.append(low_s)
    high_salary.append(high_s)
    avg_salary.append(avg_s)
df_job['low_salary'] = low_salary
df_job['high_salary'] = high_salary
df_job['avg_salary'] = avg_salary

#将带区的loc改成只有城市名，方便后续分析工作
citys = []
for loc in df_job['company_loc']:
    if loc.find('-'):
        city = loc.split('-')[0]
    else:
        city = loc
    citys.append(city)
df_job['company_city'] = citys

fileName = fileN+'_cleaned.csv'
df_job.to_csv(fileName)
