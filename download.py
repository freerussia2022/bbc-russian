from selenium import webdriver
from selenium.webdriver.common.by import By
from mako.template import Template
import time
import json
import os, sys


def tryTo(op):
    try:
        op()
        time.sleep(1)
    except Exception as e:
        pass

DRIVER = 'chromedriver'
OUT_FOLDER = 'docs'
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1280x16696')
driver = webdriver.Chrome(DRIVER, options = options)
driver.maximize_window()
driver.set_page_load_timeout(30)
driver.get('https://www.bbc.com/russian')

time.sleep(1)
result = driver.execute_script("""return JSON.stringify(Array(...document.querySelectorAll("main h3 a")).map(l=>{ const rect = l.getBoundingClientRect(); return [l.href, [Math.round(rect.x),Math.round(rect.y),Math.round(rect.width),Math.round(rect.height)]]}))""")
links = json.loads(result)

os.system("rm -rf docs/img/* docs/detail/*")
links = [
    [url,coords,url.encode("utf-8").hex()]
    for (url,coords) in links
]
links_tpl = [ [
    file,
    [str(coords[0]), str(coords[1]), str(coords[0] + coords[2]), str(coords[1] + coords[3])]]
    for (url, coords, file) in links
]
tryTo(lambda: driver.find_element(by=By.XPATH, value="//button").click())
tryTo(lambda: driver.find_element(by=By.XPATH, value="//button").click())
driver.save_screenshot(f'{OUT_FOLDER}/img/home.png')

home_template = Template(filename='./tpl/home.html')
detail_template = Template(filename='./tpl/detail.html')
print(home_template.render(links = links_tpl), file = open(f'{OUT_FOLDER}/index.html','w+'))

for (url,coords,file) in links:
    print(f'saving {url}')
    try:
        driver.get(url)
        time.sleep(1)
        tryTo(lambda: driver.find_element(by=By.CSS_SELECTOR, value="p.fc-button-label").click())
        tryTo(lambda: driver.find_element(by=By.CSS_SELECTOR, value="#bbccookies-continue-button").click())
        driver.save_screenshot(f'{OUT_FOLDER}/img/{file}.png')
        print(detail_template.render(file = file), file = open(f'{OUT_FOLDER}/detail/{file}.html','w+'))
    except Exception as e:
        continue

driver.quit()