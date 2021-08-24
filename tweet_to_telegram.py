# -*- coding: utf-8 -*-
key = 'Yourkey'

import telegram
from telegram.ext import Updater, MessageHandler, Filters
import pathlib
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from time import sleep 
from datetime import datetime 

#current dir
dir_ = pathlib.Path(__file__).parent.resolve()

#geckodriver path
driverpath = dir_ /  "geckodriver"

#driver options
options = Options()
options.add_argument("--headless")
options.add_argument("--width=800")
options.add_argument("--height=1400")


def screenshot(url):
    driver = webdriver.Firefox(executable_path=str(driverpath), options=options)
    if "https://twitter.com" in url:
        url = url.replace("https://twitter.com", "https://m.twitter.com")

        if "?" in url:
            url = url.split('?')[0]
        
        if "/photo/" in url:
            url = url.split('/photo/')[0]
            
    print("getting " + url)
    driver.get(url)
    sleep(10) #can change this
    tweet = driver.find_elements_by_tag_name('article')
    #tweet is a list use tweet[0]
    basename = "tweet"
    suffix = datetime.now().strftime("%d%m%y_%H%M%S")
    filename = basename + "_" + suffix + ".png"

    tweet[0].screenshot(str(dir_ / filename))
    driver.close()
    return dir_ / filename


def process(update, context):
    chat_id = update.message.chat_id
    msg_id = update.message.message_id

    text = update.message.text
    text = text.lower()
    
    if "https" in text:
        words = text.split(" ")
        for w in words:
            if "https://twitter.com/" in w:
                print(w)
                filename = screenshot(w)
                context.bot.send_photo(chat_id=chat_id, photo=open(filename, 'rb'), reply_to_message_id=msg_id, caption="Saved you a click 🐦")
                #clean up - sleep and delete
                sleep(2)
                filename.unlink()

def main():
    updater = Updater(key, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, process))    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

