import frida
import time
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

def on_message(message, data):
  if message['type'] == 'send':
    print("[*] {0}".format(message['payload']))
  else:
    print(message)

os.system("adb shell am force-stop com.zhiliaoapp.musically")

device = frida.get_usb_device(timeout=5)
pid = device.spawn(["com.zhiliaoapp.musically"])
device.resume(pid)
time.sleep(1)
session = device.attach(pid)
print("[*] start hook")
print(session)

js = open('xargus.js', 'r', encoding='utf8').read()
script = session.create_script(js)
script.on('message', on_message)
script.load()
api = script.exports

@app.route('/', methods = ['POST']) 
def gen():
  data = request.get_json(silent=True)
  if "url" in data and "headers" in data:
    url = data["url"]
    headers = data["headers"]
    r = api.generate(url, headers)
    return jsonify(r)

  else:
    return "err: url and headers are required."

if __name__ == '__main__':
  port = 1235
  print(">>>> Running on http://0.0.0.0:" + str(port))
  app.run(host='0.0.0.0', port=port, threaded=False, debug=False)
