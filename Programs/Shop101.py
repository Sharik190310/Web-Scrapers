from random import randint
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd

user_name = input('Enter The UserName : ')
pass_word = input('Enter The Password : ')
quantity = int(input('Enter the order quantity : '))

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.maximize_window()
driver_cookies = driver.get_cookies()

last_height = 0
new_height = 0
order_id = []
sku = []
qty = []
tracking_id = []
status = []
date = []
mydir = {}


def login(user_name, pass_word):
    username = user_name
    password = pass_word

    driver.get(
        'https://www.shop101.com/whole-seller/orders/pending?modal=sellerDesktopNotificationsModal')
    cookie = driver.find_element(
        By.XPATH, "//*[@id='sellerDesktopNotificationsModalPage']/div[4]/button[2]").click()
    driver.implicitly_wait(10)

    try:
        cookie.click()
    except:
        pass

    driver.find_element(
        By.XPATH, "//*[@id='sellerLoginPrompt__box']/button").click()
    driver.implicitly_wait(10)
    time.sleep(5)
    # find password input field and insert password as well
    driver.find_element(
        By.XPATH, "//*[@id='loginPasswordPage__box__login__usernameInputGroup__usernameInput']").send_keys(username)
    driver.implicitly_wait(10)
    driver.find_element(
        By.XPATH, "//*[@id='loginPasswordPage__box__login__passwordInputGroup__passwordInput']").send_keys(password)
    driver.implicitly_wait(10)
    # time.sleep(2)
    # click login button
    driver.find_element(By.XPATH,
                        "//*[@id='loginPasswordPage__box__login__submitButton']").click()
    driver.implicitly_wait(10)
    print('Login is successful.\n')


def scroll():
    driver.get('https://www.shop101.com/whole-seller/orders/returned')
    time.sleep(randint(1, 5))
    last_height = driver.execute_script('return document.body.scrollHeight')

    i = 51
    if(quantity < i):
        time.sleep(randint(1, 5))
        html = driver.page_source
        global soup
        soup = BeautifulSoup(html, 'lxml')
        orders = soup.find_all('div', {'class': 'order'})
        order_details(orders)
    else:
        while (i < quantity):
            driver.execute_script(
                'window.scrollTo(0,document.body.scrollHeight);')
            time.sleep(randint(2, 5))

            try:
                driver.find_element(
                    By.XPATH, f"//*[@id='sellerOrdersPage']/div[3]/div/div/div[{i}]/button").click()
                driver.implicitly_wait(10)
                time.sleep(5)
                new_height = driver.execute_script(
                    'return document.body.scrollHeight')
                i = i+50
            except:
                pass
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        orders = soup.find_all('div', {'class': 'order'})
        order_details(orders)


def order_details(orders):
    for order in orders:
        order_number = order.find(
            'div', {'class': 'order-id'}).text
        order_id.append(order_number)
        sku_i = []
        count = 0
        for sku_list in order.find_all(
                'div', {'class': 'px-0 d-flex col-sm-12 col-lg-4 col-12'}):
            sku_i.append(sku_list.find(
                'div', {'class': 'suborder-info-text'}).text.strip(' \n'))
            sku.append(sku_list.find(
                'div', {'class': 'suborder-info-text'}).text.strip(' \n'))
        if(len(sku_i) > 1):
            for count in range(len(sku_i)):
                s = sku_i[count]+' '
                mydir[order_number + f'({count})'] = s.split(' ')
                count += 1
        else:
            mydir[order_number] = sku_i

    for tracking_list in soup.find_all('div', {'class': 'col col-2'}):
        if(tracking_list.find(
                'div', {'class': 'shipping-info-text'}) == None):
            pass
        else:
            tracking_id.append(tracking_list.find(
                'div', {'class': 'shipping-info-text'}).a.text)

    for qty_list in soup.find_all(
            'div', {'class': 'd-flex col-sm-12 col-lg-8 col-12'}):
        qty.append(qty_list.find(
            'div', {'class': 'order-info-text'}).text.strip(' \n'))

    for status_list in soup.find_all(
            'span', {'class': 'order-status-value'}):
        status.append(status_list.span.text.strip(' \n'))

    for date_list in soup.find_all('div', {'class': 'return-date'}):
        date.append(date_list.text.strip(' \n'))


login(user_name, pass_word)
time.sleep(randint(1, 5))
print('Data Is being fecthed...\n')
scroll()
print(len(tracking_id), len(status), len(date), len(qty))
order_id_output = pd.DataFrame.from_dict(mydir, orient="index")
order_id_output.columns = [f'SKU{i+1}' for i in order_id_output]
order_id_output.index.name = 'Order_Id'
del order_id_output['SKU2']
df1 = order_id_output.reset_index()
df1.set_index('SKU1', inplace=True)

df1.to_csv(
    'C:\\Users\\Admin\\Documents\\Webcrapping\\order_id_output.csv')


sku_output = pd.DataFrame({'SKU': sku, 'Quantity': qty,
                           'Tracking_Id': tracking_id, 'Status': status, 'Date': date})

sku_output.to_csv(
    'C:\\Users\\Admin\\Documents\\Webcrapping\\sku_output.csv', mode='w')

dfs = [df1, sku_output]
df_final = pd.concat(dfs, axis=0,
                     ignore_index=True)


df_final.to_csv(
    'C:\\Users\\Admin\\Documents\\Webcrapping\\final_order_output.csv', mode='w')
print('Data Fetching is complete.')

driver.quit()
