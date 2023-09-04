import argparse
import math
from db import db_create
from logger_db_uuid import credituuid
from logger import connectdb
import datetime
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

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
  rdnn = credituuid()
  db_create(rdnn)
  
  time = str(datetime.datetime.now())
  frame = []
  point_data = []
  dispatcher.map("/key", print)
  x = dispatcher.map("/x_origin", print)
  y = dispatcher.map("/y_origin", print)
  z = dispatcher.map("/z_origin", print)
  visi = dispatcher.map("/visi", print)
  dispatcher.map("/json", print)
#   ups = dispatcher.map("/frame_pose", print)
#   print(ups)
  i = 0
  
  point_data[i] = {'x': x, 'y': y, 'z': z, 'vision': visi}
            # time.sleep(1)
  i += 1
            
            # Reset the dictionary after collecting information for all 33 points.
  if i == 33:
      frame.append(point_data[i])
      print(frame)
      i = 0
      point_data.clear()
#   ac = [] 
#   for i in range(33):
#       ac.append(dispatcher.map("/x_origin"))
#       ac.append(dispatcher.map("/y_origin"))
#       ac.append(dispatcher.map("/z_origin"))
#       ac.append(dispatcher.map("visi"))
#   print("hello")
#   try:
#       connectdb(rdnn, time, dispatcher.map("/key"), dispatcher.map("/x_origin", dispatcher.map("z_origin", dispatcher.map("/visi"))))
#   except:
#       print("Internal Server Is Not Response. Please Reboot : 782")
    
  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("서버로부터 정보를 수신하고 있습니다. 서버 : {}".format(server.server_address))
  server.serve_forever()