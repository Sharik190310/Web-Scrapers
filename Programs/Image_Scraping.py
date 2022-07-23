from random import randint
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os
import time
from selenium.webdriver.chrome.options import Options


url = input('Enter the url :\n')
folder_name = input('Enter the folder name :\n')

options = Options()
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
# options.headless = True

driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), chrome_options=options)
driver.maximize_window()
driver_cookies = driver.get_cookies()
action = ActionChains(driver)

login_page_link = 'https://www.flipkart.com/account/login?ret=%2Fmy-chats%3FchatType%3DBRAND'
driver.get(url)
time.sleep(randint(1, 5))
print('---------------------------------------------------------------------------------------------------')
print('Data Of Images Is Being Fetched....')
print('---------------------------------------------------------------------------------------------------')


def clicking_more_button():
    more_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[3]/div[1]/div[2]/div[5]/div/div/div[1]/div/ul/li[7]/span')))
    driver.implicitly_wait(10)
    action.move_to_element(more_button).click().perform()
    time.sleep(randint(3, 5))


def image_list():
    images_percolor = driver.find_elements(
        By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/div[1]/ul/li')
    for i in range(len(images_percolor)):
        i = i+1
        try:
            image_list_element = driver.find_element(
                By.XPATH, f'//*[@id="container"]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/div[1]/ul/li[{i}]/div')
            driver.implicitly_wait(10)
            action.move_to_element(image_list_element).pause(5).perform()
            time.sleep(randint(3, 8))
            image_element = driver.find_element(
                By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[2]/div/img')
            driver.implicitly_wait(10)
            action.move_to_element(image_element).pause(5).perform()
            img = driver.find_element(
                By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[2]/img').get_attribute('src')
            driver.implicitly_wait(10)
            imgs.append(img)
        except:
            pass


try:
    clicking_more_button()
except:
    pass

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
color_varients = soup.find_all('li', {'class': '_3V2wfe _31hAvz'})
last_link = ''

imgs = []
Color = soup.find('span', id='Color')

if(Color != None):
    if(len(color_varients) != 0):
        for i in range(len(color_varients)):
            try:
                if(i == 6):
                    clicking_more_button()
                color_varient = driver.find_element(
                    By.ID, f'swatch-{i}-color')
                action.move_to_element(color_varient).click().perform()
                time.sleep(randint(3, 5))
                current_page_link = driver.current_url
                if(current_page_link == login_page_link):
                    driver.get(last_link)
                    i = i-1
                else:
                    pass
                image_list()
                last_link = current_page_link
            except:
                break
else:
    image_list()

print('---------------------------------------------------------------------------------------------------')
print('Downloading Images....')
print('---------------------------------------------------------------------------------------------------')


def saving_images(imgs, folder):
    path = "C:\\Users\\Admin\\Documents\\WindowsPowerShell"
    try:
        os.mkdir(os.path.join(path, folder))
    except:
        pass
    os.chdir(os.path.join(path, folder))
    for img in imgs:
        if(img != None):
            link_name = img.split('/')[-1]
            img_name = link_name.split('.')[0]
            with open(img_name+'.jpeg', 'wb') as f:
                im = requests.get(img)
                time.sleep(1)
                f.write(im.content)
        else:
            pass


saving_images(imgs, folder_name)

print('---------------------------------------------------------------------------------------------------')
print('Data Fectching Is Completed.')
print('---------------------------------------------------------------------------------------------------')
driver.quit()
