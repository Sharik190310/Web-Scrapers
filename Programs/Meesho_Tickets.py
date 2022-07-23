import functools as ft
from math import ceil
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from random import randint
from bs4 import BeautifulSoup
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd


user_name = input('Enter the username : ')
pass_word = input('Enter the password : ')
percent = float(input('Enter the percent : '))

ticket_id = []
date_time = []
issue = []
status = []
id = []
mydict = {}
total_pages = 0
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver_cookies = driver.get_cookies()


def login(user_name, pass_word):
    username = user_name
    password = pass_word
    global support_url
    driver.get('https://supplier.meesho.com/panel/v2/new/login')
    time.sleep(5)

    driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(username)

    driver.find_element(
        By.XPATH, '//*[@id="password"]').send_keys(password)

    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/div[2]/form/div[3]/button').click()
    time.sleep(5)
    support_url = driver.find_element(By.XPATH,
                                      '//*[@id="root"]/div/div[1]/div/ul/li[10]/a').get_attribute('href')
    driver.implicitly_wait(10)


def pages():
    # url = 'http:https://supplier.meesho.com/'+support_url
    driver.get(support_url)
    time.sleep(randint(1, 5))
    global ticket_url
    global individual_ticket_url
    url = driver.current_url
    ticket_url = url+'/tickets/'
    individual_ticket_url = url+'/ticket/'
    driver.get(ticket_url+'1')

    page = driver.find_element(
        By.XPATH, '//*[@id="mainWrapper"]/div/div/div/div[4]/div/div[6]/button').text
    driver.implicitly_wait(10)
    return page


def tickets(page):
    total_pages = ceil(float(page)*float(percent/100.0))
    for x in range(1, total_pages+1):
        driver.get(ticket_url + f'{x}')
        time.sleep(randint(1, 5))

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        details = soup.find_all(
            'tr', {'class': 'MuiTableRow-root MuiTableRow-hover css-i6c5ts'})

        for detail in details:
            date_time.append(detail.find(
                'p', {'class': 'MuiTypography-root MuiTypography-body1 css-79faw5'}).text)
            ticket_id.append(detail.find(
                'p', {'class': 'MuiTypography-root MuiTypography-body1 css-1caykv'}).text)
            issue.append(detail.find(
                'p', {'class': 'MuiTypography-root MuiTypography-body1 css-3hy9li'}).text)

            # if(detail.find('p', {'class': 'MuiTypography-root MuiTypography-body1 css-wkk1wy'}).text
            # == 'Closed' or detail.find('p', {'class': 'MuiTypography-root MuiTypography-body1 css-mgu717'}).text == 'In Progess' or detail.find(
            #         'p', {'class': 'MuiTypography-root MuiTypography-body1 css-1woyr6v'}).text =='Issue Raised'):
            #         status.append(individual_status)


def info(ticket_id):
    for ticket in ticket_id:
        driver.get(individual_ticket_url+f'{ticket}')
        time.sleep(randint(2, 5))
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        updates = []
        catalog_ids = soup.find(
            'p', {'class': 'MuiTypography-root MuiTypography-body1 css-4qpcpn'})
        for i in catalog_ids:
            id.append(i.text)

        update_list = soup.find_all(
            'li', {'class': 'css-usjqm9'})
        for list in update_list:
            updates.append(
                list.find('p', {'class': 'MuiTypography-root MuiTypography-body2 css-xk3x4s'}).text)
        mydict[ticket] = updates


login(user_name, pass_word)
time.sleep(randint(1, 5))
page = pages()
tickets(page)
info(ticket_id)

output = pd.DataFrame.from_dict(mydict, orient="index")
output.columns = [f'Update{i+1}' for i in output]

output.index.name = 'Ticket_Id'
output.to_csv(
    'C:\\Users\\Admin\\Documents\\Webcrapping\\updates1.csv', mode='w')

ids = pd.DataFrame({'Ticket_Id': ticket_id, 'Id': id})
data = pd.DataFrame({'Ticket_Id': ticket_id, 'Date_Time': date_time,
                    'Issue': issue})
final_data = data.set_index('Ticket_Id')


dfs = [final_data, ids, output]
df_final = ft.reduce(lambda left, right: pd.merge(
    left, right, on='Ticket_Id'), dfs)
df_final.to_csv(
    'C:\\Users\\Admin\\Documents\\Webcrapping\\Final.csv', mode='w')
print(total_pages)
driver.quit()
