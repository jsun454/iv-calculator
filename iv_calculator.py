from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# selenium stuff
options = Options()
options.add_argument('--headless') # hides chrome window

browser = webdriver.Chrome(chrome_options=options)
browser.get('https://legendarypkmn.github.io/javacalc.html')

# list of html element ids
field_ids = ('name', 'nat', 'level-0', 'stat0-0', 'stat1-0', 'stat2-0', 'stat3-0', 'stat4-0', 'stat5-0')

# list of cumulative IV spreads for each stat
iv_spreads = [[0,31] for i in range(6)]

def open_file(file):
    with open(file, 'r') as f:
        name = f.readline()
        nature = f.readline()
        level = f.readline()
        pokemon = [name, nature, level]
        for line in f.readlines():
            if not line.strip():
                break # stop if a line is blank
            stats = line.split()
            inputs = pokemon + stats
            calculate_ivs(inputs)
            pokemon[2] = str(int(pokemon[2])+1)

# takes in a list in the form [name, nature, level, hp, attack, defense, spattack, spdefense, speed]
def calculate_ivs(inputs):
    # fills in all the relevant input fields
    for i in range(len(field_ids)):
        element = browser.find_element_by_id(field_ids[i])
        if(i > 1):
            element.clear()
        element.send_keys(inputs[i])

    # clicks button to calculate IVs
    btn = browser.find_element_by_id('btn-ivs')
    btn.click()

    # updates the cumulative IV spreads with the IV spreads from the current level
    for i in range(6):
        xpath = "//td[@id='spr{}-0']/span[{}]"
        xpath1 = xpath.format(i, 1)
        xpath2 = xpath.format(i, 2)
        out1 = browser.find_element_by_xpath(xpath1).get_attribute('innerHTML')
        out2 = browser.find_element_by_xpath(xpath2).get_attribute('innerHTML')
        out = (out1 + out2).replace('&nbsp;', '')

        spread = out.split(', ')
        new_min = int(spread[0])
        new_max = int(spread[-1])
        if(new_min > iv_spreads[i][0]):
            iv_spreads[i][0] = new_min
        if(new_max < iv_spreads[i][1]):
            iv_spreads[i][1] = new_max

print("Calculating IVs...")

open_file('stats.txt') # test sample input file

# format of input file:
# pokemon name\n
# nature\n
# starting level\n
# line containing stats at starting level in the form: hp atk def spatk spdef spd\n
# line containing stats at next level\n
# etc.\n

print(iv_spreads)
