import pandas as pd
import json
import traceback

fileN = input("type document name: ")
fileName = fileN + '.txt'
file = open(fileName, mode='r', encoding='utf-8')
zl_jobs = pd.DataFrame(columns=['company_name', 'company_type', 'company_loc', 'company_size', 'job_name',
                                    'job_salary', 'edu_level', 'emp_type', 'job_welfare', 'company_score'])
for response in file.readline():
    if response.startswith(u'\ufeff'):
        response = response.encode('utf8')[3:].decode('utf8')
    globals = {
        'true': 0,
        'false': 0,
        'null': 0
    }
    dict = json.loads(response)  # 字符串->dict
    joblist = dict["data"]["results"]
    for job in joblist:
        company_name = job["company"]["name"]
        company_type = job["company"]["type"]["name"]
        company_loc = job["city"]["display"]
        company_size = job["company"]["size"]["name"]
        job_name = job["jobName"]
        job_salary = job["salary"]
        edu_level = job["eduLevel"]
        emp_type = job["emplType"]
        job_welfare = job["jobTag"]["searchTag"]
        company_score = job["score"]
        zl_jobs = zl_jobs.append({'No': len(zl_jobs) + 1, 'company_name': company_name, 'company_type': company_type,
                                  'company_loc': company_loc, 'company_size': company_size, 'job_name': job_name,
                                  'job_salary': job_salary, 'edu_level': edu_level, 'emp_type': emp_type,
                                  'job_welfare': job_welfare, 'company_score': company_score}, ignore_index=True)
print(zl_jobs.values)
zl_jobs.to_csv('%s.csv' % (fileN), encoding='utf_8_sig')