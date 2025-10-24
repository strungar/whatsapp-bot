from selenium import webdriver
import threading, importlib, time, platform
import config, bot, commands
from functions import *

print("libs loaded")
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=google-chrome-whatsapp")
#options.add_argument("--headless")
if platform.system() == "Windows":
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument("--in-process-gpu")
  options.add_argument('--remote-debugging-port=9222')
  options.binary_location = "./chrome-win32/chrome.exe"
  service = webdriver.chrome.service.Service(executable_path="./chromedriver-win32/chromedriver.exe")
  print("options defined")
  driver = webdriver.Chrome(service=service,options=options)
else:
  print("options defined")
  driver = webdriver.Chrome(options=options)
driver.get("https://web.whatsapp.com/")
print("browser loaded")
t = None
l = threading.Lock()
args = {"t":t,"l":l,"driver":driver,"names":config.names}
print("all set")

reload(args)
while True:
  comm = input()
  print("> %s" % (comm,))
  commands.execute(comm,args)
