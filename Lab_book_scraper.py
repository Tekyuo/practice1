import time
from threading import Thread

from selenium.webdriver.support import expected_conditions as EC
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "cookie":"",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br"
}
'''
page = requests.get("https://studfile.net/search/?q=лабораторная",headers=headers)
file=open("index.html","w")
file.write(str(page.content))
print(str(page.content)'''

def save_txt(link,i):
    page =requests.get(link)
    soup = BeautifulSoup(page.content,"html.parser")
    mydivs = soup.find_all("div", {"class": "pdf_holder"})

    filename = str(i) + '.txt'

    file_path = os.path.join(os.getcwd(), SEARCH_TAG, filename)

    with open(file_path, 'w', encoding="utf8") as fl:
        fl.write(mydivs[0].get_text())

    print(i)


def get_all_docs_async_lim(links,lim):
    threads = []
    for i in range(len(links)):
        process = Thread(target=save_txt, args=[links[i], i])
        threads.append(process)
        process.start()
        if len(threads) >= lim:
            for prc in threads:
                prc.join()
            threads.clear()

    for prc in threads:
        prc.join()
    threads.clear()



for SEARCH_TAG in ['лабораторная','лабораторная работа',"контрольная работа","курсовая работа","пособие","учебное пособие","научная книга"]:

    dir = os.path.join(os.getcwd(), SEARCH_TAG)
    if not os.path.exists(dir):
        os.mkdir(dir)
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver.get("https://studfile.net/search/?q="+SEARCH_TAG)

    all_links =[]
    wait_elementid = "//a[@class='gs-title']"
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, wait_elementid)))
    links = driver.find_elements_by_css_selector("a[class='gs-title']")
    links = [i.get_attribute("data-ctorig") for i in links if i.get_attribute("data-ctorig") != None]

    all_links.extend(links)

    for page in range(2,11):
        cursor = driver.find_element_by_css_selector("div[class='gsc-cursor-page'][aria-label='Страница " + str(page) + "']")
        cursor.click()
        time.sleep(0.75)

        links = driver.find_elements_by_css_selector("a[class='gs-title']")
        links = [i.get_attribute("data-ctorig") for i in links if i.get_attribute("data-ctorig") != None]

        all_links.extend(links)

    all_links = list(set(all_links))
    print(all_links)
    get_all_docs_async_lim(all_links,32)
input()

#'https://studfile.net/preview/4171438/', 'https://studfile.net/preview/13715625/', 'https://studfile.net/preview/6873510/', 'https://studfile.net/preview/5849181/',