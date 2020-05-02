import camlistener

import time
import sys
import socket
import config

SERVER_PORT = "1935"
STREAM_ENDPOINT = "inputs"
SERVER_IP = None

if len(sys.argv) > 1:
   for i in range(len(sys.argv)):
       if sys.argv[i] == '-h' or sys.argv[i] == '--help':
           print("Camorah\n")
           print("Tool for starting 4i 360 camera from orah\n")
           print("-h | --help	Prints this help screen.")
           print("-s | --server	Set ip address of rtmp server. (default : ip of this device)")
           print("-p | --port	Set port of rtmp server. (default : 1935)")
           print("-a | --app	Set rtmp application name. (default : inputs)")
           print("-d | --dump	Dump streams in specified dir.")
           print("\n")
           print("Example:")
           print("python3 camorah.py")
           print("python3 camorah.py -s 192.168.0.2 -p 2048 -a mystream -d ./rec/")
           print("\n")
           quit()
       if sys.argv[i] == '-s' or sys.argv[i] == '--server':
           SERVER_IP = sys.argv[i + 1]
       if sys.argv[i] == '-p' or sys.argv[i] == '--port':
           SERVER_PORT = sys.argv[i + 1]
       if sys.argv[i] == '-a' or sys.argv[i] == '--app':
           STREAM_ENDPOINT = sys.argv[i + 1]
       if sys.argv[i] == '-d' or sys.argv[i] == '--dump':
           config.DUMP = True
           config.OutDir = sys.argv[i + 1]


if SERVER_IP is None:
     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     s.connect(("8.8.8.8", 80))
     SERVER_IP = s.getsockname()[0]
     s.close()

config.STREAM_URL = "rtmp://" + SERVER_IP + ":" + SERVER_PORT + "/" + STREAM_ENDPOINT + "/"

print("RTMP SERVER : " + config.STREAM_URL)

camlistener.CamListener()

while True:
	time.sleep(5)

