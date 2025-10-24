from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support.relative_locator import locate_with
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from datetime import datetime
from random import random
from urllib3.exceptions import MaxRetryError
from sys import exit
import time, threading, re, traceback
import commands

#options = webdriver.ChromeOptions()
#options.add_argument("--user-data-dir=/home/strungar/.config/google-chrome-whatsapp")
#driver = webdriver.Chrome()
#driver.get("https://web.whatsapp.com/")

def react(driver, msg, reaction, symbol):
  pass
'''
  ActionChains(driver)\
    .move_to_element(msg)\
    .pause(.2)\
    .perform()
  btn_react = driver.find_element(locate_with(By.XPATH, "//div[contains(@aria-label,'React')]").to_left_of(msg))
  btn_react.click()
  ActionBuilder(driver).clear_actions()
  time.sleep(.2)
  btn_more_reacts = driver.find_element(locate_with(By.XPATH, "//div[contains(@aria-label,'More reactions')]").above(btn_react))
  btn_more_reacts.click()
  time.sleep(.2)
  btn_search_reacts = driver.find_element(locate_with(By.XPATH, "//input[contains(@aria-label,'Search reaction')]"))
  btn_search_reacts.send_keys(reaction)
  time.sleep(.2)
  btn_emoji = driver.find_element(By.XPATH, "//span[contains(@data-emoji,'%s')]" % (symbol,))
  btn_emoji.click()
'''

def respond(driver, response):
#          reply = driver.find_element(By.CLASS_NAME,"selectable-text.copyable-text.x15bjb6t.x1n2onr6").below(msg_got[-1])
  reply = driver.find_element(By.XPATH, "//div[contains(@aria-placeholder,'Type a message')]")
  reply.clear()
  reply.send_keys(response)
  reply.send_keys(Keys.RETURN)

def bot(lock, driver=None, names=[]):
  print("bot: started")
  regex_num = re.compile("[0-9]+")

  print("bot: enter loop with %s, %s" % (str(driver.name if driver is not None else driver),names))
  while True:
   if not lock.locked():
    print("lock is released, dying")
    return 0
   #print("lock is busy")
   for name in names:
    if "active" in names[name] and names[name]["active"] == False:
      print("name is deactivated, skipping")
      continue
    print("bot: %s to search" % (name,))
    while True:
      try:
        person = driver.find_element(By.XPATH, "//span[contains(@title,'{}')]".format(name))
        break
      except ElementNotInteractableException:
        break
      except NoSuchElementException:
        print(".",end='')
        time.sleep(.5)
    #print("bot: %s found" % (person,))
    try:
      person.click()
    except ElementClickInterceptedException:
      pass
    except ElementNotInteractableException:
      pass

    msg_got = driver.find_elements(By.CLASS_NAME, "_ao3e.selectable-text.copyable-text")
#    msg = [message.text for message in msg_got]
    msg = [msg_got[-1].text.lower()]
    #print(msg)
    try:
      t = msg_got[-1].find_element(By.XPATH,"./../..")
      time_author = t.get_property("attributes")[1]["value"]
      ts,author = time_author.split("] ")
      author = author[:-2]
      timestamp = datetime.strptime(ts,"[%H:%M, %m/%d/%Y")
      print("%s: last message from %s was: %s" % (timestamp,author,msg[-1],))
    except:
      print("%s: last message was: %s" % (datetime.now(),msg[-1],))
    if len(msg):
      if "plain" in names[name]:
       for request in names[name]["plain"]:
        print("plain request %s: " % (request,),end='')
        if request in msg[-1]:
          if "reactions" in names[name]["plain"][msg[-1]]:
            for reaction, symbol in list(names[name]["plain"][msg[-1]]["reactions"].items()):
              react(driver,msg_got[-1],reaction,symbol)
          if "response_plain" in names[name]["plain"][msg[-1]]:
            respond(driver,names[name]["plain"][msg[-1]]["response_plain"])
          if "response" in names[name]["plain"][request]:
            print("have a calculated response to send")
            if "math" in names[name]["plain"][request]["response"]:
              if "a" in names[name]["plain"][request]["response"]:
                a = names[name]["plain"][request]["response"]["a"]
              elif "a_regex" in names[name]["plain"][request]["response"]:
                a_regex = re.compile(names[name]["plain"][request]["response"]["a_regex"])
                a = int(a_regex.search(found))
              if "b" in names[name]["plain"][request]["response"]:
                b = names[name]["plain"][request]["response"]["b"]
              elif "b_regex" in names[name]["plain"][request]["response"]:
                b_regex = re.compile(names[name]["plain"][request]["response"]["b_regex"])
                b = int(b_regex.search(found[0])[0])
              print("%s %s %s" % (a,names[name]["plain"][request]["response"]["math"],b))
              if names[name]["plain"][request]["response"]["math"] == "add":
                result = str(a + b)
              elif names[name]["plain"][request]["response"]["math"] == "sub":
                result = str(a - b)
              elif names[name]["plain"][request]["response"]["math"] == "mul":
                result = str(a * b)
              elif names[name]["plain"][request]["response"]["math"] == "div":
                result = str(a / b)
              if "prefix_cond" not in names[name]["plain"][request]["response"] or names[name]["plain"][request]["response"]["prefix_cond"] in msg[-1]:
               if "prefix" in names[name]["plain"][request]["response"]:
                result = names[name]["plain"][request]["response"]["prefix"] + result
              if "suffix_cond" not in names[name]["plain"][request]["response"] or names[name]["plain"][request]["response"]["suffix_cond"] in msg[-1]:
               if "suffix" in names[name]["plain"][request]["response"]:
                result = result + names[name]["plain"][request]["response"]["suffix"]
              print("result: %s" % (result,))
            respond(driver,result)
          if "command" in names[name]["plain"][msg[-1]]:
            commands.execute(names[name]["plain"][msg[-1]]["command"])
            respond("executed %s" % (names[name]["plain"][msg[-1]]["command"],))
        else:
          print("not found")
      else:
        print("no plain")
      if "regex" in names[name]:
       for request in names[name]["regex"]:
        print("regex request %s: " % (request,),end='')
        r = re.compile(request)
        found = r.search(msg[-1])
        if found is not None:
          print("found %s" % (found,))
          if "reactions" in names[name]["regex"][request]:
            for reaction, symbol in list(names[name]["regex"][request]["reactions"].items()):
              react(driver,msg_got[-1],reaction,symbol)
          if "response_plain" in names[name]["regex"][request]:
            respond(driver,names[name]["regex"][request]["response_plain"])
          if "response" in names[name]["regex"][request]:
            print("have a calculated response to send")
            if "math" in names[name]["regex"][request]["response"]:
              if "a" in names[name]["regex"][request]["response"]:
                a = names[name]["regex"][request]["response"]["a"]
              elif "a_regex" in names[name]["regex"][request]["response"]:
                a_regex = re.compile(names[name]["regex"][request]["response"]["a_regex"])
                a = int(a_regex.search(found))
              if "b" in names[name]["regex"][request]["response"]:
                b = names[name]["regex"][request]["response"]["b"]
              elif "b_regex" in names[name]["regex"][request]["response"]:
                b_regex = re.compile(names[name]["regex"][request]["response"]["b_regex"])
                b = int(b_regex.search(found[0])[0])
              print("%s %s %s" % (a,names[name]["regex"][request]["response"]["math"],b))
              if names[name]["regex"][request]["response"]["math"] == "add":
                result = str(a + b)
              elif names[name]["regex"][request]["response"]["math"] == "sub":
                result = str(a - b)
              elif names[name]["regex"][request]["response"]["math"] == "mul":
                result = str(a * b)
              elif names[name]["regex"][request]["response"]["math"] == "div":
                result = str(a / b)
              if "prefix_cond" not in names[name]["regex"][request]["response"] or names[name]["regex"][request]["response"]["prefix_cond"] in msg[-1]:
               if "prefix" in names[name]["regex"][request]["response"]:
                result = names[name]["regex"][request]["response"]["prefix"] + result
              if "suffix_cond" not in names[name]["regex"][request]["response"] or names[name]["regex"][request]["response"]["suffix_cond"] in msg[-1]:
               if "suffix" in names[name]["regex"][request]["response"]:
                result = result + names[name]["regex"][request]["response"]["suffix"]
              print("result: %s" % (result,))
            time.sleep(random() * 30 + 10)
            respond(driver,result)
          if "command" in names[name]["regex"][request]:
            commands.execute(names[name]["regex"][request]["command"])
            respond(driver,"executed %s" % (names[name]["regex"][request]["command"],))
        else:
          print("not found")
      else:
        print("no regex")
    else:
      print("msg empty")
    time.sleep(1)


def main(lock, driver=None, names=[]):
  while True:
    try:
      bot(lock,driver,names)
    except KeyboardInterrupt:
      exit(1)
    except MaxRetryError:
      exit(1)
    except:
      traceback.print_exc()
