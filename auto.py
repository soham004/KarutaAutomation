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
import requests
from io import BytesIO
from PIL import Image
import numpy as np
from playsound import playsound


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
notificationPath = data['notificationPath']
notify = data['notify']
dropToGrabDelay = data['dropToGrabDelay']

def ocr(img, boundingBox):
    im1 = img.crop(boundingBox)
    img1 = np.array(im1)
    results = reader.readtext(img1)
    return results


def countdown(t): 
    
    while t: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\r") 
        time.sleep(1) 
        t -= 1

def tprint(string):
    """Takes a string and prints it with a timestamp prefix."""
    print('[{}] {}'.format(time.strftime("%Y-%m-%d %H:%M:%S"), string))

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

try:
    continueButton = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div/div/section/div[2]/button[2]/div')))
    continueButton.click()
except:
    None

loginEmailField = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "uid_32")))

loginEmailField.send_keys(discord_email)

driver.implicitly_wait(2)

passwordField = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'uid_34')))
passwordField.send_keys(discord_password)

driver.implicitly_wait(2)

# loginButton = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/button[2]')))
loginButton = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
driver.execute_script("arguments[0].click();", loginButton)

tprint("Logged in")

WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'messageListItem__5126c')))

loop=True

while loop:
    playsound(notificationPath) if notify else None
    print("\n\n\n")
    tprint("Dropping Cards.....")

    ActionChains(driver)\
        .send_keys("kd")\
        .send_keys(Keys.RETURN)\
        .perform()
    
    time.sleep(dropToGrabDelay)

    messeges = driver.find_elements(By.CLASS_NAME, 'messageListItem__5126c')

    statindex = -1

    try:
        if(messeges[statindex].find_elements(By.CLASS_NAME, 'username_c19a55')[1].text != "Queen's Right Leg"):
            raise Exception("Queen's Right Leg stats Not Found")
        tprint("Queen's Right Leg Stats Found")

        cardsMsg = messeges[(statindex-1)]


        cardImageUrl = cardsMsg.find_element(By.CLASS_NAME, 'originalLink_af017a').get_attribute('href')
        tprint(f"Card Image Url - {cardImageUrl}")

        cardImageData = requests.get(cardImageUrl).content
        im = Image.open(BytesIO(cardImageData))
        # cardNum1CropBox = (158, 371, 197, 382)
        # cardNum2CropBox = (432, 371, 471, 382)
        # cardNum3CropBox = (706, 371, 745, 382)
        bound = (21,362,808,393)
        cardnumData = ocr(im, bound)
        cardNum1 = int(cardnumData[0][1].split(" ")[0].split(".")[0].replace("Z", "7").replace("O", "0").replace("S", "5").replace("B", "8").replace("I", "1").replace("L", "1").replace("G", "6").replace("A", "4").replace("D", "0").replace("Q", "0").replace("U", "0").replace("T", "1").replace("J", "1").replace("C", "0"))
        cardNum2 = int(cardnumData[1][1].split(" ")[0].split(".")[0].replace("Z", "7").replace("O", "0").replace("S", "5").replace("B", "8").replace("I", "1").replace("L", "1").replace("G", "6").replace("A", "4").replace("D", "0").replace("Q", "0").replace("U", "0").replace("T", "1").replace("J", "1").replace("C", "0"))
        cardNum3 = int(cardnumData[2][1].split(" ")[0].split(".")[0].replace("Z", "7").replace("O", "0").replace("S", "5").replace("B", "8").replace("I", "1").replace("L", "1").replace("G", "6").replace("A", "4").replace("D", "0").replace("Q", "0").replace("U", "0").replace("T", "1").replace("J", "1").replace("C", "0"))

        tprint(f"Card 1: {cardNum1}")
        tprint(f"Card 2: {cardNum2}")
        tprint(f"Card 3: {cardNum3}")
        cardsNumDict = {
            0:cardNum1,
            1:cardNum2,
            2:cardNum3,
        }

        reactionButtons = cardsMsg.find_elements(By.CLASS_NAME, 'reactionInner__23977')
        i=1
        for reactionButton in reactionButtons:
            tprint(f"Found reaction button {i}")
            i = i+1
        print("")
        droppedStatsMsg = messeges[statindex]
        wishStatsElements = droppedStatsMsg.find_elements(By.CLASS_NAME, 'inline')
        wishDict = {
            0:int(wishStatsElements[0].text.replace('♡','').replace(',','')),
            1:int(wishStatsElements[1].text.replace('♡','').replace(',','')),
            2:int(wishStatsElements[2].text.replace('♡','').replace(',','')),
        }
        for key in wishDict:
            tprint(f"Cars {key+1} Wishlisted: {wishDict[key]}")
        if(min(cardNum1, cardNum2, cardNum3)<1000):
            tprint("Found a low print card.")
            bestCardIndex = min(cardsNumDict, key=cardsNumDict.get)
        else:
            aggregateWishDict = {
                0:((100000-cardNum1)/10000)+wishDict[0],
                1:((100000-cardNum2)/10000)+wishDict[1],
                2:((100000-cardNum3)/10000)+wishDict[2],
            }
            tprint("Card 1 Aggregate Points: {}".format(aggregateWishDict[0]))
            tprint("Card 2 Aggregate Points: {}".format(aggregateWishDict[1]))
            tprint("Card 3 Aggregate Points: {}".format(aggregateWishDict[2]))
            bestCardIndex = max(aggregateWishDict, key=aggregateWishDict.get)

        tprint(f"Best card is: {bestCardIndex+1}")
        tprint(f"Clicking {bestCardIndex+1}")
        reactionButtons[bestCardIndex].click()
        if (cardsNumDict[bestCardIndex]>60000):
            time.sleep(5)
            tprint("Adding burn tag")
            ActionChains(driver)\
                .send_keys("kt burn")\
                .send_keys(Keys.RETURN)\
                .perform()
            
    
    except Exception as e:
        tprint(e)
        try:
            cardsMsg = messeges[statindex]
            cardImageUrl = cardsMsg.find_element(By.CLASS_NAME, 'originalLink_af017a').get_attribute('href')
            tprint(f"Card Image Url - {cardImageUrl}")

            cardImageData = requests.get(cardImageUrl).content
            im = Image.open(BytesIO(cardImageData))
            bound = (21,362,808,393)
            cardnumData = ocr(im, bound)
            cardNum1 = int(cardnumData[0][1].split(" ")[0].split(".")[0].replace("Z", "7").replace("O", "0").replace("S", "5").replace("B", "8").replace("I", "1").replace("L", "1").replace("G", "6").replace("A", "4").replace("D", "0").replace("Q", "0").replace("U", "0").replace("T", "1").replace("J", "1").replace("C", "0"))
            cardNum2 = int(cardnumData[1][1].split(" ")[0].split(".")[0].replace("Z", "7").replace("O", "0").replace("S", "5").replace("B", "8").replace("I", "1").replace("L", "1").replace("G", "6").replace("A", "4").replace("D", "0").replace("Q", "0").replace("U", "0").replace("T", "1").replace("J", "1").replace("C", "0"))
            cardNum3 = int(cardnumData[2][1].split(" ")[0].split(".")[0].replace("Z", "7").replace("O", "0").replace("S", "5").replace("B", "8").replace("I", "1").replace("L", "1").replace("G", "6").replace("A", "4").replace("D", "0").replace("Q", "0").replace("U", "0").replace("T", "1").replace("J", "1").replace("C", "0"))

            tprint(f"Card 1: {cardNum1}")
            tprint(f"Card 2: {cardNum2}")
            tprint(f"Card 3: {cardNum3}")
            cardsNumDict = {
                1:cardNum1,
                2:cardNum2,
                3:cardNum3,
            }
            bestCardIndex = min(cardsNumDict, key=cardsNumDict.get)
            reactionButtons = cardsMsg.find_elements(By.CLASS_NAME, 'reactionInner__23977')
            for reactionButton in reactionButtons:
                tprint("Found a reaction button")
            tprint(f"Clicking {bestCardIndex+1}")
            reactionButtons[bestCardIndex].click()
            if (cardsNumDict[bestCardIndex]>60000):
                time.sleep(5)
                tprint("Adding burn tag")
                ActionChains(driver)\
                    .send_keys("kt burn")\
                    .send_keys(Keys.RETURN)\
                    .perform()
        except Exception as e:
            try:
                tprint("Error, trying to select random card")
                cardsMsg = messeges[(statindex-1)]
                reactionButtons = cardsMsg.find_elements(By.CLASS_NAME, 'reactionInner__23977')
                for reactionButton in reactionButtons:
                    tprint("Found a reaction button")
                cardindex = random.randint(0,2)
                tprint(f"Clicking {cardindex}")
                reactionButtons[cardindex].click()
                if (cardsNumDict[cardindex]>60000):
                    time.sleep(5)
                    tprint("Adding burn tag")
                    ActionChains(driver)\
                        .send_keys("kt burn")\
                        .send_keys(Keys.RETURN)\
                        .perform()
                    
            except Exception as e:
                try:
                    tprint("Error, trying to select random card")
                    cardsMsg = messeges[(statindex)]
                    reactionButtons = cardsMsg.find_elements(By.CLASS_NAME, 'reactionInner__23977')
                    for reactionButton in reactionButtons:
                        tprint("Found a reaction button")
                    cardindex = random.randint(0,2)
                    tprint(f"Clicking {cardindex}")
                    reactionButtons[cardindex].click()
                    if (cardsNumDict[cardindex]>60000):
                        time.sleep(5)
                        print("Adding burn tag")
                        ActionChains(driver)\
                            .send_keys("kt burn")\
                            .send_keys(Keys.RETURN)\
                            .perform()
                except Exception as e:
                    tprint(e)
                    tprint("Cannot find cards to collect")
    
    waitTime = drop_delay+random.randint(randomDropDelayMin, randomDropDelayMax)
    tprint(f"Waiting {waitTime}s for next drop")
    countdown(waitTime)

driver.quit()