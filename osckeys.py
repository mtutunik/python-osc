import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server
from typing import List
from typing import Any
from pynput.keyboard import Key, Controller

keyboard = Controller()
key_address = "/unity/key/"

def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

def handle_osckeys(address: str, *args: List[Any]) -> None:
  print("handle_osckey: address {0}".format(address))
  
  keys = address[-(len(address) - len(key_address)):] 
  for key in keys:
    print("Key: {0}".format(key))  
    keyboard.press(key)
    keyboard.release(key)
  
  for key in args:
    print("Key: {0}".format(key))
    keyboard.press(key)
    keyboard.release(key)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=5005, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/filter", print)
  dispatcher.map("/volume", print_volume_handler, "Volume")
  dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)
  dispatcher.map(key_address + "*", handle_osckeys)

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()
