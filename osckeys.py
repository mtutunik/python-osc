import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server
from typing import List
from typing import Any
from pynput.keyboard import Key, Controller

keyboard = Controller()

def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

def handle_osckeys(address: str, *args: List[Any]) -> None:
  #print("handle_osckey: {address}")
  if not address[:len("/unity/key/")] == "/unity/key/":
      print("Uknown osc address: {address}")
      return
  for key in args:
    print(f"Key: {key}")  
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
  dispatcher.map("/unity/key/*", handle_osckeys)

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()
