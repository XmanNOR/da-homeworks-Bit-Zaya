#ТЗ
#__________________________
# https://www.rbc.ru/business/
#Таблица 1: id, Заголовок новости, ссылка на новость, ссылка на картинку, дата публикации, количество просмотров, id категории
#Таблица 2: id категории, категория
#Спарсить 100 новостей

#Запросы:
#1. Выбрать все новости, в заголовке которых фигурирует слово "США" в период, указанный в программе.
#2. Подсчитать за каждый день выборки количество новостей, и количество новостей со словом "США"
#UPD: Полную дату, категорию и количество просмотров можно найти в каждой новости, если перейти на неё

#__________________________


import time



from bs4 import BeautifulSoup
import pandas as pd

from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from fake_useragent import UserAgent

useragent=UserAgent()


def get_list_url_links(url, limit):
    with open("Backup_parser.txt", "w", encoding="utf-8") as output:

        options = webdriver.FirefoxOptions()
        options.add_argument(f'user-agent={useragent.random}')
        #options.add_argument("--headless")
        service = Service(r'D:/Programms/0.Py/Selenium/firefoxdriver/geckodriver.exe')
        driver = webdriver.Firefox(service=service, options=options)
        driver.get(url=url)
        Result_list = []
        prom_list = []

        wait = WebDriverWait(driver, 5)
        element_found = False
        while not element_found:
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[4]/div[1]/div[1]/div/div[3]/div/main/div/div[2]/div[{limit}]/div/a/span[1]/span/span/span')))
                element_found = True
            except:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))

        if element_found:
            for i in range(limit):
                title = driver.find_element(By.XPATH,
                                              f'//html/body/div[4]/div[1]/div[1]/div/div[3]/div/main/div/div[2]/div[{i+1}]/div/a/span[1]/span/span/span').text

                news_link = driver.find_element(By.XPATH,f'/html/body/div[4]/div[1]/div[1]/div/div[3]/div/main/div/div[2]/div[{i+1}]/div/a').get_attribute("href")
                pic_link = driver.find_element(By.XPATH,f'/html/body/div[4]/div[1]/div[1]/div/div[3]/div/main/div/div[2]/div[{i+1}]/div/a/span[2]/picture/img').get_attribute("src")
                prom_list.append(title)
                prom_list.append(news_link)
                prom_list.append(pic_link)
                Result_list.append(prom_list)
                prom_list = []

        else:
            print("Element not found")
        driver.close()
        driver.quit()
        return Result_list




My_data_list = get_list_url_links('https://www.rbc.ru/business/', 100)

tag_dict = {}
tag_id = 1
with tqdm(My_data_list) as pbar:
    for lists in My_data_list:
        options = webdriver.FirefoxOptions()
        options.add_argument(f'user-agent={useragent.random}')
        options.add_argument("--headless")
        service = Service(r'D:/Programms/0.Py/Selenium/firefoxdriver/geckodriver.exe')
        driver = webdriver.Firefox(service=service, options=options)
        driver.get(url=lists[1])

        news_tags = []
        try:
            soup = BeautifulSoup(driver.page_source, 'lxml')
            lists.append(driver.find_element(By.TAG_NAME, 'time').get_attribute("datetime"))
            lists.append(driver.find_element(By.CLASS_NAME, 'article__header__counter-block').text)
            all_tags = soup.find('div', class_= 'article__tags__container').find_all('a', class_='article__tags__item')
            print('Найдено')
            for i in all_tags:
                print(i.text)
                if i.text not in tag_dict.values() and len(i.text)>1:
                   tag_dict[f'{tag_id}'] = i.text
                   news_tags.append(int(tag_id))
                   tag_id += 1
                   print(tag_dict)
                elif len(i.text)>1:
                   tag_to_add = [k for k, v in tag_dict.items() if v == i.text]
                   news_tags.append(int(tag_to_add[0]))
            lists.append(news_tags)
        except Exception as ex:
            print(ex)
            print(lists[1])
        finally:
            driver.close()
            driver.quit()
        pbar.update(1)






df = pd.DataFrame(My_data_list, columns=[
    'Заголовок',
    'Ссылка',
    'Картинка',
    'Дата',
    'Просмотры',
    'Тэг ID'
])
df.to_excel('РБК.xlsx', index=False)

print(tag_dict)
df = pd.DataFrame(tag_dict.items(), columns=['Тег ID','Тег'])
df.to_excel('РБК_тэги.xlsx', index=False)