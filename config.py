import json

default = {
  "PUT_YOUR_NUMBER_HERE": {
    "active": True,
    "plain": {
      "ping": {
        "reactions": {
          "plus": "➕"
        },
        "response_plain": "pong"
      },
      "stop": {
        "command": "stop"
      }
    }
  }
}

try:
  names = json.load(open("config.json", "r", encoding="utf8"))
except FileNotFoundError:
  names = json.dumps(default, ensure_ascii=False, indent=2)
  with open("config.json", "w", encoding="utf8") as f:
    f.write(names)
  names = json.loads(names)

