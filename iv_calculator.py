from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless') # hides chrome window

browser = webdriver.Chrome(chrome_options=options)
browser.get('https://legendarypkmn.github.io/javacalc.html')

ids = ['name', 'nat', 'level-0', 'stat0-0', 'stat1-0', 'stat2-0', 'stat3-0', 'stat4-0', 'stat5-0']
inputs = ['magikarp', 'adamant', 5, 18, 7, 11, 7, 8, 14] # sample inputs

# fills in all relevant fields
for i in range(len(ids)):
    element = browser.find_element_by_id(ids[i])
    element.send_keys(inputs[i])

# clicks button to calculate IVs
btn = browser.find_element_by_id('btn-ivs')
btn.click()

# prints outputted IV spreads
for i in range(1, 6):
    xpath = "//td[@id='spr{}-0']/span[{}]"
    xpath1 = xpath.format(i, 1)
    xpath2 = xpath.format(i, 2)
    out1 = browser.find_element_by_xpath(xpath1).get_attribute('innerHTML')
    out2 = browser.find_element_by_xpath(xpath2).get_attribute('innerHTML')
    print(out1 + out2)
