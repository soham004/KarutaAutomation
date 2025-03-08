class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(bcolors.OKGREEN+"Importing Packages....")

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
import numpy as np
from playsound import playsound
import cv2



print(bcolors.OKGREEN+"Starting Bot")
print(bcolors.OKGREEN+"Initialising OCR....")
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
    img1 = np.array(img.crop(boundingBox))

    gray = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)

    # Apply thresholding (binary inversion)
    _, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
    # Apply morphological operations to remove noise
    kernel = np.ones((1, 1), np.uint8)
    processed_img = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    
    results = reader.readtext(processed_img, allowlist='0123456789 ', min_size = 5)

    return results

def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    """Return a sharpened version of the image, using an unsharp mask."""
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened

def ocr(image):
    numArr = []
    for i in range(0,3):
        length = 60
        if i == 0:
            x = 153
        elif i == 1:
            x = 427
        else:
            x = 701
        cropped = image[372:385, x:x+length]
        upscaled = cv2.resize(cropped, (0,0), fx = 8, fy = 8)
        gray = cv2.cvtColor(upscaled, cv2.COLOR_RGB2GRAY)
        _, thresholded = cv2.threshold(gray, 64, 255,
            cv2.THRESH_BINARY_INV)

        blurred = cv2.GaussianBlur(thresholded, (3, 3), 1)
        sharpened = unsharp_mask(blurred, kernel_size=(3,3))

        OcrImage = sharpened
        results = reader.readtext(OcrImage, allowlist='0123456789. ', min_size = 5)
        numArr.append(int((results[0][1].lstrip().split(" ")[0].split(".")[0][:5])))
    return numArr

def countdown(t): 
    
    while t: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\r") 
        time.sleep(1) 
        t -= 1

def tprint(string, colourCode=bcolors.ENDC):
    """Takes a string and prints it with a timestamp prefix."""
    print(colourCode , '[{}] {}'.format(time.strftime("%Y-%m-%d %H:%M:%S") , string))

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

loginEmailField = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "uid_32")))

loginEmailField.send_keys(discord_email)

driver.implicitly_wait(2)

passwordField = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'uid_34')))
passwordField.send_keys(discord_password)

driver.implicitly_wait(2)

# loginButton = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/button[2]')))
loginButton = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
loginButton.click()

tprint("Logged in", colourCode=bcolors.OKGREEN)

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'messageListItem__5126c')))

loop=True


def ocrGrabFromSecondLastWithRightLeg(statindex):

    if(messeges[statindex].find_elements(By.CLASS_NAME, 'username_c19a55')[1].text != "Queen's Right Leg"):
            raise Exception("Queen's Right Leg stats Not Found")
    tprint("Queen's Right Leg Stats Found", colourCode=bcolors.OKGREEN)

    cardsMsg = messeges[(statindex-1)]


    cardImageUrl = cardsMsg.find_element(By.CLASS_NAME, 'originalLink_af017a').get_attribute('href')
    tprint(f"Card Image Url - {cardImageUrl}", colourCode=bcolors.OKBLUE)

    resp = requests.get(cardImageUrl, stream=True).raw
    im = np.asarray(bytearray(resp.read()), dtype="uint8")
    im = cv2.imdecode(im, cv2.IMREAD_COLOR)

    cardnumData = ocr(im)

    try:
        cardNum1 = cardnumData[0]
    except IndexError:
        cardNum1 = 1
    try:
        cardNum2 = cardnumData[1]
    except IndexError:
        cardNum2 = 1
    try:
        cardNum3 = cardnumData[2]
    except IndexError:
        cardNum3 = 1
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
        tprint(f"Found reaction button {i}", colourCode=bcolors.OKGREEN)
        i = i+1
    print("")
    droppedStatsMsg = messeges[statindex]
    wishStatsElements = droppedStatsMsg.find_elements(By.CLASS_NAME, 'inline')
    wishDict = {
        0:int(wishStatsElements[0].text.replace('♡','')),
        1:int(wishStatsElements[1].text.replace('♡','')),
        2:int(wishStatsElements[2].text.replace('♡','')),
    }
    for key in wishDict:
        tprint(f"Cars {key+1} Wishlisted: {wishDict[key]}", colourCode=bcolors.OKGREEN)
    if(min(cardNum1, cardNum2, cardNum3)<1000):
        tprint("Found a low print card.", colourCode=bcolors.OKBLUE)
        bestCardIndex = min(cardsNumDict, key=cardsNumDict.get)
    else:
        aggregateWishDict = {
            0:((100000-cardNum1)/10000)+wishDict[0],
            1:((100000-cardNum2)/10000)+wishDict[1],
            2:((100000-cardNum3)/10000)+wishDict[2],
        }
        tprint("Card 1 Aggregate Points: {}".format(aggregateWishDict[0]), colourCode=bcolors.OKGREEN)
        tprint("Card 2 Aggregate Points: {}".format(aggregateWishDict[1]), colourCode=bcolors.OKGREEN)
        tprint("Card 3 Aggregate Points: {}".format(aggregateWishDict[2]), colourCode=bcolors.OKGREEN)
        bestCardIndex = max(aggregateWishDict, key=aggregateWishDict.get)

    tprint(f"Best card is: {bestCardIndex+1}", colourCode=bcolors.OKGREEN)
    tprint(f"Clicking {bestCardIndex+1}", colourCode=bcolors.OKGREEN)
    reactionButtons[bestCardIndex].click()
    if (cardsNumDict[bestCardIndex]>60000):
        time.sleep(5)
        tprint("Adding burn tag", colourCode=bcolors.WARNING)
        ActionChains(driver)\
            .send_keys("kt burn")\
            .send_keys(Keys.RETURN)\
            .perform()

def ocrGrabWithoutRightLeg(statindex):
    cardsMsg = messeges[statindex]
    cardImageUrl = cardsMsg.find_element(By.CLASS_NAME, 'originalLink_af017a').get_attribute('href')
    tprint(f"Card Image Url - {cardImageUrl}", colourCode=bcolors.OKBLUE)

    resp = requests.get(cardImageUrl, stream=True).raw
    im = np.asarray(bytearray(resp.read()), dtype="uint8")
    im = cv2.imdecode(im, cv2.IMREAD_COLOR)

    cardnumData = ocr(im)
    try:
        cardNum1 = cardnumData[0]
    except IndexError:
        cardNum1 = 1
    try:
        cardNum2 = cardnumData[1]
    except IndexError:
        cardNum2 = 1
    try:
        cardNum3 = cardnumData[2]
    except IndexError:
        cardNum3 = 1

    tprint(f"Card 1: {cardNum1}", colourCode=bcolors.OKGREEN)
    tprint(f"Card 2: {cardNum2}", colourCode=bcolors.OKGREEN)
    tprint(f"Card 3: {cardNum3}", colourCode=bcolors.OKGREEN)
    cardsNumDict = {
        0:cardNum1,
        1:cardNum2,
        2:cardNum3,
    }
    bestCardIndex = min(cardsNumDict, key=cardsNumDict.get)
    reactionButtons = cardsMsg.find_elements(By.CLASS_NAME, 'reactionInner__23977')
    i=1
    for reactionButton in reactionButtons:
        tprint(f"Found reaction button {i}", colourCode=bcolors.OKGREEN)
        i = i+1
    
    tprint(f"Best card is: {bestCardIndex+1} with {cardsNumDict[bestCardIndex]} print", colourCode=bcolors.OKBLUE)
    tprint(f"Clicking {bestCardIndex+1}", colourCode=bcolors.OKGREEN)
    reactionButtons[bestCardIndex].click()
    if (cardsNumDict[bestCardIndex]>60000):
        time.sleep(5)
        tprint("Adding burn tag", colourCode=bcolors.WARNING)
        ActionChains(driver)\
            .send_keys("kt burn")\
            .send_keys(Keys.RETURN)\
            .perform()

def randomGrab(statindex):
    cardsMsg = messeges[statindex]
    cardsMsg = messeges[(statindex)]
    reactionButtons = cardsMsg.find_elements(By.CLASS_NAME, 'reactionInner__23977')
    for reactionButton in reactionButtons:
        tprint("Found a reaction button", colourCode=bcolors.OKGREEN)
    cardindex = random.randint(0,2)
    tprint(f"Clicking {cardindex}", colourCode=bcolors.WARNING)
    reactionButtons[cardindex].click()

while loop:
    playsound(notificationPath) if notify else None
    print("\n\n\n")
    tprint("Dropping Cards.....", colourCode=bcolors.OKGREEN)

    ActionChains(driver)\
        .send_keys("kd")\
        .send_keys(Keys.RETURN)\
        .perform()

    time.sleep(dropToGrabDelay)

    messeges = driver.find_elements(By.CLASS_NAME, 'messageListItem__5126c')

    statindex = -1

    try:
        ocrGrabFromSecondLastWithRightLeg(statindex)
    except Exception as e:
        tprint(e, colourCode=bcolors.FAIL)
        try:
            tprint("Trying to select card in last msg", colourCode=bcolors.WARNING)
            ocrGrabWithoutRightLeg(statindex) # Ocr Grab from last element
        except Exception as e:
            try:
                tprint("Error! Trying to select card in second last msg", colourCode=bcolors.WARNING)
                ocrGrabWithoutRightLeg((statindex-1)) # Ocr Grab from second last element
            except Exception as e:
                tprint(e)
                try:
                    tprint("Error! Trying to select random card in second last msg", colourCode=bcolors.WARNING)
                    randomGrab(statindex-1)
                except Exception as e:
                    tprint(e)
                    try:
                        tprint("Error, trying to select random card in last msg", colourCode=bcolors.WARNING)
                        randomGrab(statindex)
                    except Exception as e:
                        tprint(e)
                        tprint("Cannot find cards to collect", colourCode=bcolors.FAIL)
    
    waitTime = drop_delay+random.randint(randomDropDelayMin, randomDropDelayMax)
    tprint(f"Waiting {waitTime}s for next drop", colourCode=bcolors.OKCYAN)
    countdown(waitTime)

driver.quit()