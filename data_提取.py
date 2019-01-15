import pandas as pd
import json

fileN = input("type document name: ")
line = int(input("type document line:"))
fileName = fileN + '.txt'
file = open(fileName, mode='r', encoding='utf-8')
#新建一个dataframe
zl_jobs = pd.DataFrame(columns=['No', 'company_name', 'company_type', 'company_loc', 'company_size', 'job_name',
                                'work_exp', 'job_welfare', 'job_salary', 'edu_level', 'emp_type', 'company_score'])
for i in range(0, line):
    response = file.readline()
    if response.startswith(u'\ufeff'):
        response = response.encode('utf8')[3:].decode('utf8')
    globals = {
        'true': 0,
        'false': 0,
        'null': 0
    }
    print(i+1)
    dict = json.loads(response)  #字符串->dict
    joblist = dict["data"]["results"]
    for job in joblist:
        company_name = job["company"]["name"]
        company_type = job["company"]["type"]["name"]
        company_loc = job["city"]["display"]
        company_size = job["company"]["size"]["name"]
        job_name = job["jobName"]
        work_exp = job["workingExp"]["name"]
        job_welfare = job["welfare"]
        job_salary = job["salary"]
        edu_level = job["eduLevel"]["name"]
        emp_type = job["emplType"]
        #job_welfare = job["jobTag"]["searchTag"]
        company_score = job["score"]
        zl_jobs = zl_jobs.append({'No': len(zl_jobs) + 1, 'company_name': company_name, 'company_type': company_type,
                                  'company_loc': company_loc, 'company_size': company_size, 'job_name': job_name,
                                  'work_exp': work_exp, 'job_salary': job_salary, 'edu_level': edu_level,
                                  'emp_type': emp_type, 'company_score': company_score, 'job_welfare': job_welfare},
                                ignore_index=True)
print(zl_jobs.values)
zl_jobs.to_csv('%s.csv' % (fileN), encoding='utf_8_sig')