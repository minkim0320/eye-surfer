import tkinter as tk
from tkinter import filedialog, Text
from tkinter import *
from tkhtmlview import HTMLLabel
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .components.webNavigation import webNavigation as webnav
from .components.speechToText import speechToText as stt
from .components.textToSpeech import textToSpeech as tts

import os
import time

root = tk.Tk()
apps = []

def callback(event):
    print("You pressed Enter")
    stt.toAudioFile()
    string_words = stt.speechToText()
    noun_word = stt.extractKeywords(string_words)
    print(noun_word)
    opened = False
    nums = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen']
    if (noun_word[0] == ""):
        tts.textToSpeech("Sorry I didn't get that. Can you try again?")

    if (noun_word[0] == 'open'):
        opened = True
        info.setDriver()
        info.driver.get('https://nationalpost.com/')
        tts.textToSpeech("Opened up windows. What would you like to do next?")

    if (noun_word[0] in ['search', 'look', 'find']):
        if (noun_word[1] == ""):
            tts.textToSpeech("Sorry I didn't get that. Can you try again?")
        # info.setDriver()
        info.driver.get('https://nationalpost.com/')
        info.title_ld = webnav.search_for_news(noun_word[1], info.driver)
        title_list = webnav.data_to_title_list(info.title_ld)
        count = 0
        try:
            tts.textToSpeech("Here are the following articles with the search {}".format(noun_word[1]))
            for title in title_list:
                tts.textToSpeech(nums[count])
                tts.textToSpeech(title)
                count += 1
                if (count == 2):
                    break
                time.sleep(1)
            
            tts.textToSpeech("Which article would you like to read?")
        except KeyboardInterrupt:
            tts.textToSpeech("Stopped reading. What would you like to do next?")
            print("sound cancelled from keyboard interrupt")


    if (noun_word[0] in ['choose', 'select', 'read']):
        tts.textToSpeech("Great choice. Opening up article {}".format(noun_word[1]))
        index_news = int(noun_word[1])
        article_ls = webnav.select_news(info.title_ld, index_news, info.driver)
        try:
            for string in article_ls:
                tts.textToSpeech(string)
        except KeyboardInterrupt:
            tts.textToSpeech("Stopped reading. What would you like to do next?")
            print("sound cancelled from keyboard interrupt")


    if (noun_word[0] in ['stop', 'close']):
        tts.textToSpeech("Ok. Closing")
        webnav.close_chrome(info.driver)


class Info:
    def __init__(self):
        self.driver = None
        self.title_ld = ""
    
    def setDriver(self):
        credential_path = os.path.join(os.path.dirname(__file__), './','chromedriver.exe')
        self.driver = webdriver.Chrome(credential_path)

info = Info()
root.geometry("190x190")
root.configure(background='white')
root.bind('<Return>', callback)


# canvas = tk.Canvas(root, height=700, width=700, bg="white")
# canvas.pack()

my_label = HTMLLabel(root, html='<img src="logo2.png" width="150" height="160" />')
my_label['background']='white'
my_label.pack()
my_label.pack(pady=20, padx=20, fill="both", expand=True)


# frame = tk.Frame(root, bg="white")
# frame.place(relw=0.8, relheight=0.8, relx=0.1, rely=0.1)

# openFile = tk.Button(root, text="Open File", padx=10, pady=5, fg="white", bg="#263D42", command=addApp)
# openFile.pack()
# runApps = tk.Button(root, text="Run Apps", padx=10, pady=5, fg="white", bg="#263D42", command=runApps)
# runApps.pack()
tts.textToSpeech("Hi Christine. What would you like to do today on the web?")
root.mainloop()

