from selenium import webdriver
import threading, importlib, time
import config, bot, commands
from functions import *

options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=google-chrome-whatsapp")
driver = webdriver.Chrome(options)
driver.get("https://web.whatsapp.com/")
t = None
l = threading.Lock()
args = {"t":t,"l":l,"driver":driver,"names":config.names}
print("browser loaded")

reload(args)
while True:
  comm = input()
  print("> %s" % (comm,))
  commands.execute(comm,args)
