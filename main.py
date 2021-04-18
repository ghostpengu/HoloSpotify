import time
import random
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
chrome_options = Options()
from multiprocessing import Process

import art

leasttime = 30.5
mosttime = 35.2
skiptime = float(random.uniform(leasttime, mosttime))

combospath = input('Input the path to your combos file: ')
print('')
playlist = input('Paste the link to your playlist here. Remove everything after and including "?si=", it will crash the program: ')
print('')
songnumber = int(input('How many songs does the playlist have? (or how many you wanna play from the top): '))
print('')

if (leasttime * songnumber) < 600:
    print('It will take from ' + str(int(leasttime * songnumber)) + ' seconds to ' + str(int(mosttime  * songnumber)) + ' seconds to play the whole playlist')
    print('')
if (leasttime * songnumber) > 600:
    print('It will take from approx. ' + str(int((leasttime * songnumber) / 60)) + ' minutes to ' + str(int((mosttime * songnumber) / 60)) + ' minutes to play the whole playlist')
    print('')

looptimes = int(input('How many times do you want to loop the playlist?: '))
print('')
likepercentage = input('What should be the chance to like each song (20, 80, etc...) in %: ')
print('')

instances = int(input('How many instances?: '))
print('')
print('Okay, starting the program with ' + str(instances) + ' instance(s)')
print('')

def spot():
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    #chrome_options.add_argument("--headless") #does not play songs
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1080, 780)
    driver.get('https://accounts.spotify.com/en/login/')
    driver.find_element_by_xpath('//*[@id="login-username"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="login-password"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="app"]/body/div[1]/div[2]/div/form/div[4]/div[1]/div/label').click()
    driver.find_element_by_xpath('//*[@id="login-button"]').click()
    time.sleep(2)
    try:
        element = driver.find_element_by_xpath('//*[@id="app"]/body/div/div[2]/div/div/div[4]/div/a')
        element.click()
        print('Successfully logged in with combo ' + str(combonumber))
        print('')
    except NoSuchElementException:
        print("Wrong password at combo " + str(combonumber) + ", terminating that instance now")
        print('')
        driver.quit()
    time.sleep(10)
    driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
    driver.get(playlist)
    time.sleep(4)
    print('Playing now')
    print('Looping the playlist for the 1. time')
    driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/section/div[2]/div[2]/div/button[1]').click()

    looped = 1
    skipped = 0
    while looped <= looptimes:
        while skipped < songnumber:
            time.sleep(skiptime)
            skipped = skipped + 1
            print('Skipping for the ' + str(skipped) + '. time')
            driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/button[4]').click()
            iflike = random.uniform(1, 100)
            if iflike < likepercentage:
                driver.find_element_by_class_name('_07bed3a434fa59aa1852a431bf2e19cb-scss').click()
        while skipped == songnumber:
            #play playlist
            looped = looped + 1
            print('Looping the playlist for the ' + str(looped) + '. time')
            driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/section/div[2]/div[2]/div/button[1]').click()
            skipped = skipped - songnumber
    while looped == looptimes + 1:
        print('Looped the playlist ' + str(looped - 1) + ' times, quitting now')
        driver.close()
        sys.exit()

with open(combospath, 'r') as file:
    combonumber = 0
    while combonumber < instances:
        content = file.readline()
        llll = content.split(":")
        username = llll[0]
        password = llll[1]
        combonumber = combonumber + 1
        if __name__ == '__main__':
            Process(target=spot).start()