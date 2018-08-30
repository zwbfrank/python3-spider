# -*- coding: utf-8 -*-

import requests
import json
from lxml import etree
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep



def test_boss_spider():
    url = 'https://www.zhipin.com/c101280600-p100109/' 
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'

    }
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    sleep(3)
    driver.implicitly_wait(5)
    res = requests.get(url, headers=headers)
    html = etree.HTML(res.text)
    ls = html.xpath('//div[@class="job-list"]//li')
    i = 0
    mouseover = driver.find_element_by_xpath('//div[@class="job-list"]//li[{}]//div[@class="job-title"]'.format(i+1))

    sleep(3)

    driver.implicitly_wait(5)

    ActionChains(driver).move_to_element(mouseover).perform()

    sleep(1)

    driver.implicitly_wait(5)
    text = driver.page_source

    driver_html = etree.HTML(text)

    dls = driver_html.xpath('//div[@class="job-list"]//li')
    l = dls[0]
    job_name = l.xpath('//div[@class="job-list"]//li[{}]//div[@class="detail-top-title"]//text()'.format(i+1))
    job_salary = l.xpath('//div[@class="job-list"]//li[{}]//span[@class="red"]//text()'.format(i+1))
    job_desc = l.xpath('//div[@class="job-list"]//li[{}]//div[@class="detail-bottom-text"]//text()'.format(i+1))
    company_name = l.xpath('//*[@id="main"]/div/div[2]/ul/li[1]/div/div[2]/div/h3/a/text()')[0]
    job_desc_str = ''.join(word for word in job_desc)

    print(job_name[0]+'\n'+job_salary[0]+'\n'+job_desc_str+'\n'+company_name)


def test_url():
    url = 'https://www.zhipin.com/c101280600-p100109/' 
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'

    }
    res = requests.get(url, headers=headers)
    html = etree.HTML(res.text)
    next_page_url = html.xpath('//*[@id="main"]/div/div[2]/div[2]/a[5]/@href')[0]
    print(next_page_url)
    next_page_url = urljoin(url, next_page_url)  
    res = requests.get(next_page_url, headers=headers)

    print(res.status_code)
    print(res.text)


def test_scro_url():
    url = 'https://www.zhipin.com/c101280600-p100109/'
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'

    }   
    while url:
        res = requests.get(url, headers=headers)
        html = etree.HTML(res.text)
        next_page_url = html.xpath('//*[@id="main"]//div[@class="page"]//a[@class="next"]//@href')
        # if not next_page_url:
        #     break
        print(next_page_url)
        url = urljoin(url, next_page_url[0])
    print('done')  







if __name__ == '__main__':
    # test_boss_spider()
    test_scro_url()