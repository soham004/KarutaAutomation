from seleniumbase import SB
import msvcrt
import time
import sys
import json
import logging
import socket

try:
    with open('config.json') as f:
        data = json.load(f)
except:
    with open('discord_config.json') as f:
        data = json.load(f)

REMOTE_SERVER = "www.discord.com"
FORMAT = '%(asctime)s : %(message)s'
discord_email = data['email']
discord_password = data['password']
logging.basicConfig(format=FORMAT, filename='autoVote.log', level=logging.INFO)

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1

def wait_for_input(timeout):
    """Waits for Enter key press with a timeout while displaying a countdown (Windows version)."""
    start_time = time.time()
    while True:
        remaining_time = timeout - (time.time() - start_time)
        if remaining_time <= 0:
            print("\nTime's up!")
            return False  # Timeout reached
        hours, remainder = divmod(remaining_time, 3600)
        mins, secs = divmod(remainder, 60)
        sys.stdout.write("\rTime left: {:02d}:{:02d}:{:02d} Press Enter to Vote Now... ".format(int(hours),int(mins), int(secs)))
        sys.stdout.flush()

        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\r':  # Enter key is detected
                print("\nUser pressed Enter!")
                return True  # Input received

        time.sleep(0.1)  # Reduce CPU usage

def voteFor(url, name=""):
    while True:
        try:
            with SB(uc=True) as sb:
                logging.info(f"Voting for {name}")
                print(f"Voting for {name}")
                sb.uc_open_with_reconnect(url, 4)
                sb.maximize_window()
                sb.wait(1)
                sb.uc_gui_click_captcha()
                sb.click('a.chakra-button')
                sb.type('input[name="email"]', discord_email)
                sb.type('input[name="password"]', discord_password)
                sb.click('button[type="submit"]')
                print("Logged In")
                logging.info("Logged In")
                sb.wait(5)
                sb.execute_script('document.getElementsByClassName("intObserver__3d3b0")[0].scrollIntoView()')
                sb.click('div.action__3d3b0>button ')
                print("Authorized")
                logging.info("Authorized")
                sb.wait(10)
                sb.click('button.chakra-button.css-7rul47')
                print(f"Voted for {name}")
                logging.info(f"Voted for {name}")
                sb.wait(10)
                return  # Exit loop on success
        except Exception as e:
            logging.error(f"Error voting for {name}: {e}")
            print(f"Error voting for {name}: {e}")
            print("Retrying in 10 seconds...")
            countdown(10)  # Wait before retrying

def is_connected(hostname):
    try:
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except Exception:
        pass  # Ignore errors
    return False

initial_wait_time = int(input("Enter Initial wait time in seconds: "))
print(f"Initial wait time: {initial_wait_time} seconds")
logging.info(f"Initial wait time: {initial_wait_time} seconds")
wait_for_input(initial_wait_time)

while True:
    
    while not is_connected(REMOTE_SERVER):
        print("Internet not connected, retrying in 10 seconds...")
        logging.error("Internet not connected")
        countdown(10)

    print("Internet connected")
    logging.info("Internet connected")

    voteFor("https://top.gg/bot/646937666251915264/vote", name="Karuta")  # Vote for Karuta
    voteFor("https://top.gg/bot/853629533855809596/vote", name="Sofi")  # Vote for Sofi
    logging.info("Waiting for 12 hours and 15 seconds")
    print("Waiting for 12 hours and 15 seconds")
    wait_for_input(43215)  # Wait for 12 hours and 15 seconds
