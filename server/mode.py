import argparse
import math
# from db import db_create
# from logger_db_uuid import credituuid
# from logger import connectdb
import datetime
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1", help="OSC ServerIP")
parser.add_argument("--port", type=int, default=9000, help="Lisener") 
args = parser.parse_args()
client = udp_client.SimpleUDPClient(args.ip, args.port)

def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="IP Lisen...")
  parser.add_argument("--port",
      type=int, default=9001, help="UDP Ports")
  args = parser.parse_args()

  dispatcher = Dispatcher()
  
  date = str(datetime.datetime.now())
#   rdnn = credituuid()
#   db_create(rdnn)
  
  time = str(datetime.datetime.now())
  
#   dispatcher.map("/key", print)
#   dispatcher.map("/x_origin", print)
#   dispatcher.map("/y_origin", print)
#   dispatcher.map("/z_origin", print)
#   dispatcher.map("/visi", print)
#   dispatcher.map("/json", print)
  ac = [] 
  for i in range(33):
      ac.append(dispatcher.map("/x_origin", print))
      ac.append(dispatcher.map("/y_origin", print))
      ac.append(dispatcher.map("/z_origin", print))
      ac.append(dispatcher.map("visi", print))
  print("hello")
  client.send_message("tracker-VMT_Tracker", ac)
  ac = []
#   try:
#       connectdb(rdnn, time, dispatcher.map("/key"), dispatcher.map("/x_origin", dispatcher.map("z_origin", dispatcher.map("/visi"))))
#   except:
#       print("Internal Server Is Not Response. Please Reboot : 782")
    
  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("서버로부터 정보를 수신하고 있습니다. 서버 : {}".format(server.server_address))
  server.serve_forever()