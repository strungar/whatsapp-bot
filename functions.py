import importlib, threading, time
import config, bot

def reload(args):
  print("reloading bot")

  importlib.reload(config)
  #report_config(config)

  args["names"]=config.names
  importlib.reload(bot)
  if args["l"].locked():
    print("releasing lock")
    args["l"].release()
  print("t is %s" %(args["t"],))
  if args["t"] is not None:
   print("waiting for the thread to die")
   while args["t"].is_alive():
    time.sleep(.1)
  print("acquiring a new lock")
  args["l"].acquire(blocking=True)
  print("defining a new thread")
  args["t"] = threading.Thread(target=bot.main, args=(args["l"],args["driver"],args["names"]))
  print("starting bot")
  args["t"].start()
  print("bot started")
