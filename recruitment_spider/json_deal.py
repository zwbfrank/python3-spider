import json



if __name__ == '__main__':

    filename = 'jobInfo.json'
    job_info_file = 'job_info.txt'
    with open(filename) as f_json:
        job_list = json.load(f_json)
    for job in job_list:
        with open(job_info_file, 'a') as f_job:
            for job_dict in job:
                job_name = 'job_name: '+job_dict['job_name']+'\n'
                job_salary = 'job_salary: '+job_dict['job_salary']+'\n'
                company_name = 'company_name: '+job_dict['company']+'\n'
                job_desc = 'job_desc: '+job_dict['job_desc']+'\n\n'
                job_str = job_name+job_salary+company_name+job_desc
                f_job.write(job_str)
