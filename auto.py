import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random



data = None

try:
    with open('config.json') as f:
        data = json.load(f)
except:
    with open('discord_config.json') as f:
        data = json.load(f)


url = 'https://discord.com/channels/1177302607937671189/1316412274734399528'

# url ='https://bot.sannysoft.com/'

options = webdriver.ChromeOptions()
# options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False) 
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(options=options) 
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Google Inc. (Intel)",
        renderer="ANGLE (Intel, Intel(R) Iris(R) Xe Graphics (0x000046A8) Direct3D11 vs_5_0 ps_5_0, D3D11)",
        fix_hairline=True,
)

driver.get(url)
loginEmailField = WebDriverWait(driver, 30).until(
EC.presence_of_element_located((By.ID, "uid_32")))

loginEmailField.send_keys(data['email'])

driver.implicitly_wait(2)

passwordField = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'uid_34')))
passwordField.send_keys(data['password'])

driver.implicitly_wait(2)

loginButton = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/button[2]')))
loginButton.click()


WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'messageListItem__5126c')))

# # chatText.click()
# chatText.send_keys("kd")

ActionChains(driver)\
        .send_keys("kd")\
        .send_keys(Keys.RETURN)\
        .perform()

time.sleep(5)

messeges = driver.find_elements(By.CLASS_NAME, 'messageListItem__5126c')

statindex = -1
try:
    if(messeges[statindex].find_elements(By.CLASS_NAME, 'username_c19a55')[1].text != 'Queen\'s Right Leg'):
        raise Exception("droppedStatsMsg Not Found")
    print("droppedStatsMsg Found")
    cardsMsg = messeges[(statindex-1)]
    reactionButtons = cardsMsg.find_elements(By.CLASS_NAME, 'reactionInner__23977')
    for reactionButton in reactionButtons:
        print("found a reaction button")
    droppedStatsMsg = messeges[statindex]
    wishStatsElements = droppedStatsMsg.find_elements(By.CLASS_NAME, 'inline')
    wishDict = {
        0:int(wishStatsElements[0].text.replace('♡','')),
        1:int(wishStatsElements[1].text.replace('♡','')),
        2:int(wishStatsElements[2].text.replace('♡','')),
    }
    bestCardIndex = max(wishDict, key=wishDict.get)
    print(f"Best card is: {bestCardIndex+1}")
    print(f"Clicking {bestCardIndex}")
    reactionButtons[bestCardIndex].click()
except Exception as e:
    print(e)
    cardsMsg = messeges[statindex]
    reactionButtons = cardsMsg.find_elements(By.CLASS_NAME, 'reactionInner__23977')
    for reactionButton in reactionButtons:
        print("found a reaction button")
    randomIndex = random.randint(0,2)
    print(f"Clicking {randomIndex}")
    reactionButtons[randomIndex].click()

input("Press Enter to quit...")

driver.quit()