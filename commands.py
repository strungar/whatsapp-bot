from functions import *

def execute(comm,args):
  if comm in ["pause","stop"]:
    args["l"].release()
  elif comm in ["reload", "unpause","play"]:
    reload(args)
  elif comm.split()[0] == "addchat":
    print("not implemented")
  else:
    print("don't know what %s is" % (comm,))
