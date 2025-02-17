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
import easyocr

print("Starting Bot")
print("Initialising OCR....")
reader = easyocr.Reader(['en'],gpu=False, verbose=False)

print("Reading Config....")
try:
    with open('config.json') as f:
        data = json.load(f)
except:
    with open('discord_config.json') as f:
        data = json.load(f)


# Global Variables
discord_email = data['email']
discord_password = data['password']
drop_delay = data['dropDelay']
randomDropDelayMin = data['randomDropDelayMin']
randomDropDelayMax = data['randomDropDelayMax']
url = data['karutaPrivateServerTextChannelLink']
headlessRun = data['headlessRun']
verbose = data['verbose']


options = webdriver.ChromeOptions()

if headlessRun:
    options.add_argument("--headless=new")
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False) 
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
if not verbose:
    options.add_argument('log-level=3')

driver = webdriver.Chrome(options=options) 
stealth(
    driver,
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

loginEmailField.send_keys(discord_email)

driver.implicitly_wait(2)

passwordField = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'uid_34')))
passwordField.send_keys(discord_password)

driver.implicitly_wait(2)

loginButton = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/button[2]')))
loginButton.click()


WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'messageListItem__5126c')))

loop=True

while loop:
    
    print("Dropping Cards.....")

    ActionChains(driver)\
        .send_keys("kd")\
        .send_keys(Keys.RETURN)\
        .perform()

    time.sleep(5)

    messeges = driver.find_elements(By.CLASS_NAME, 'messageListItem__5126c')

    statindex = -1

    try:
        if(messeges[statindex].find_elements(By.CLASS_NAME, 'username_c19a55')[1].text != 'Queen\'s Right Leg'):
            raise Exception("Queen\'s Right Leg stats Not Found")
        print("Queen\'s Right Leg Stats Found")

        cardsMsg = messeges[(statindex-1)]
        reactionButtons = cardsMsg.find_elements(By.CLASS_NAME, 'reactionInner__23977')
        for reactionButton in reactionButtons:
            print("Found a reaction button")
        
        droppedStatsMsg = messeges[statindex]
        wishStatsElements = droppedStatsMsg.find_elements(By.CLASS_NAME, 'inline')
        wishDict = {
            0:int(wishStatsElements[0].text.replace('♡','')),
            1:int(wishStatsElements[1].text.replace('♡','')),
            2:int(wishStatsElements[2].text.replace('♡','')),
        }
        bestCardIndex = max(wishDict, key=wishDict.get)

        print(f"Best card is: {bestCardIndex+1}")
        print(f"Clicking {bestCardIndex+1}")
        reactionButtons[bestCardIndex].click()
    
    except Exception as e:
        print(e)
        try:
            cardsMsg = messeges[statindex]
            reactionButtons = cardsMsg.find_elements(By.CLASS_NAME, 'reactionInner__23977')
            for reactionButton in reactionButtons:
                print("Found a reaction button")
            randomIndex = random.randint(0,2)
            print(f"Clicking {randomIndex+1}")
            reactionButtons[randomIndex].click()
        except Exception as e:
            print("Cannot find cards to collect")
    
    waitTime = drop_delay+random.randint(randomDropDelayMin, randomDropDelayMax)
    print(f"Waiting {waitTime}s for next drop")
    time.sleep(waitTime)

driver.quit()