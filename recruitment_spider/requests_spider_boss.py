# -*- coding: utf-8 -*-

import requests
# import os
import json
from lxml import etree
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


def driver_mouseover(url, headers):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    sleep(3)
    driver.implicitly_wait(5)  

    res = requests.get(url, headers=headers)
    html = etree.HTML(res.text)
    ls = html.xpath('//div[@class="job-list"]//li')

    for i in range(1, len(ls)+1):
        mouseover = driver.find_element_by_xpath('//div[@class="job-list"]//li[{}]//div[@class="job-title"]'.format(i))
        sleep(3)
        driver.implicitly_wait(5)
        ActionChains(driver).move_to_element(mouseover).perform()
        sleep(1)
        driver.implicitly_wait(5)

    text = driver.page_source
    driver.quit()

    return text


def get_next_url(url, headers):
    res = requests.get(url, headers=headers)
    html = etree.HTML(res.text)
    next_page_url = html.xpath('//*[@id="main"]//div[@class="page"]//a[@class="next"]//@href')
    url = urljoin(url, next_page_url[0])
    return url


def get_data(url, headers, text):
    driver_html = etree.HTML(text)
    dls = driver_html.xpath('//div[@class="job-list"]//li')

    job_info_list = []
    job_dict = {}
    for i, l in enumerate(dls):
        job_name = l.xpath('//div[@class="job-list"]//li[{}]//div[@class="detail-top-title"]//text()'.format(i+1))
        job_salary = l.xpath('//div[@class="job-list"]//li[{}]//span[@class="red"]//text()'.format(i+1))
        company_name = l.xpath('//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[2]/div/h3/a/text()'.format(i+1))
        job_desc = l.xpath('//div[@class="job-list"]//li[{}]//div[@class="detail-bottom-text"]//text()'.format(i+1))
        #job_desc is a list, turn into string
        job_desc_str = ''.join(word for word in job_desc)
        job_dict = {
            'job_name': job_name[0],
            'job_salary': job_salary[0],
            'company': company_name[0],
            'job_desc': job_desc_str,
        }

        job_info_list.append(job_dict)
    return job_info_list


def json_dump(data):
    with open('jobInfo.json', 'a') as f:
        json.dump(data, f, indent=4, separators=(',', ':'))


def main():
    url = 'https://www.zhipin.com/c101280600-p100109/'
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'

    }
    job_list = []
    while True:
        text = driver_mouseover(url, headers)
        data = get_data(url, headers, text)
        job_list.append(data)
        try:
            url = get_next_url(url, headers)        
        except IndexError:
            break
    json_dump(job_list)
    print('done')


if __name__ == '__main__':
    main()

#     url = 'https://www.zhipin.com/c101280600-p100109/'
#     headers = {
#         'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'

#     }
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     driver.get(url)
#     sleep(3)
#     driver.implicitly_wait(5)

#     res = requests.get(url, headers=headers)
#     html = etree.HTML(res.text)
#     ls = html.xpath('//div[@class="job-list"]//li')

#     for i in range(1, len(ls)+1):
#         mouseover = driver.find_element_by_xpath('//div[@class="job-list"]//li[{}]//div[@class="job-title"]'.format(i))
#         sleep(3)
#         driver.implicitly_wait(5)
#         ActionChains(driver).move_to_element(mouseover).perform()
#         sleep(1)
#         driver.implicitly_wait(5)

#     text = driver.page_source
#     driver_html = etree.HTML(text)
#     dls = driver_html.xpath('//div[@class="job-list"]//li')

#     job_info_list = []
#     job_dict = {}
#     for i, l in enumerate(dls):
#         job_name = l.xpath('//div[@class="job-list"]//li[{}]//div[@class="detail-top-title"]//text()'.format(i+1))
#         job_salary = l.xpath('//div[@class="job-list"]//li[{}]//span[@class="red"]//text()'.format(i+1))
#         company_name = l.xpath('//*[@id="main"]/div/div[2]/ul/li[{}]/div/div[2]/div/h3/a/text()'.format(i+1))
#         job_desc = l.xpath('//div[@class="job-list"]//li[{}]//div[@class="detail-bottom-text"]//text()'.format(i+1))
#         #job_desc is a list, turn into string
#         job_desc_str = ''.join(word for word in job_desc)
#         job_dict = {
#             'job_name': job_name[0],
#             'job_salary': job_salary[0],
#             'company': company_name[0],
#             'job_desc': job_desc_str,
#         }

#         job_info_list.append(job_dict)

#     with open('jobInfo.json', 'a') as f:
#         json.dump(job_info_list, f, indent=4, separators=(',', ':'))



#     # next_page_url = '//*[@id="main"]/div/div[2]/div[2]/a[5]'


# while url:
#     deal spider,
#     url = next_page_url




