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


def getModifier(keys: str): 
  mod_pos = keys.find("_")
  modifier = None
  if mod_pos <= 0 :
      return None, keys
   
  mod_str = keys[0:mod_pos]
  if mod_str == "ctrl":
    modifier = Key.ctrl
  elif mod_str == "ctrl_":
    modifier = Key.ctrl_l
  elif mod_str == "ctrl_r":
    modifier = Ker.ctrl_r
  elif mod_str == "alt":
    modifier = Key.alt
  elif mod_str == "alt_l":
    modifier = Key.alt_l
  elif mod_str == "alt_r":
    modifier = Key.alt_r
  elif mod_str == "shift":
    modifier = Key.shift
  elif mod_str == "shift_l":
    modifier = Key.shift_l
  elif mod_str == "shift_r":
    modifier = Key.shift_r
  elif mod_str == "cmd":
    modifier = Key.cmd
  elif len(mod_str) == 1:
    modifier = KeyCode.from_char(mod_str)
  else:
    modifier = None  

  return modifier, keys[mod_pos + 1:] 
       


def handle_osckeys(address: str, *args: List[Any]) -> None:
  print("handle_osckey: address {0}".format(address))
   
  keys = address[-(len(address) - len(key_address)):]

  if keys == "space":
      keyboard.press(Key.space)
      keyboard.release(Key.space)
  elif keys == "right":
      keyboard.press(Key.right)
      keyboard.release(Key.right)
  elif keys == "left":
      keyboard.press(Key.left)
      keyboard.release(Key.left)
  elif keys == "up":
      keyboard.press(Key.up)
      keyboard.release(Key.up)
  elif keys == "down":
      keyboard.press(Key.down)
      keyboard.release(Key.down) 
  elif keys == "enter":
      keyboard.press(Key.enter)
      keyboard.release(Key.enter)
  elif keys == "esc":
      keyboard.press(Key.esc)
      keyboard.release(Key.esc)
  else:
      modifier, keys = getModifier(keys)
          
      if modifier != None:
        keyboard.press(modifier)

      for key in keys:
        print("modifier key: {0} Key: {1}".format(modifier, key))  
        keyboard.press(key)
        keyboard.release(key)
      
      if modifier != None:
        keyboard.release(modifier)



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
