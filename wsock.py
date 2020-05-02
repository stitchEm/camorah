import cameracommand

from autobahn.asyncio.websocket import WebSocketClientProtocol, WebSocketClientFactory
import threading
import time
import subprocess
import datetime
import config


def startDump():
    print("startDump")

    try:
        subprocess.call(["rtmpdump"])
    except OSError as e:
        if e.errno == errno.ENOENT:
            print("rtmpdump not found, can't dump stream")
            return

    now = datetime.datetime.now()
    out_file_name = config.OutDir + "orah_dump_" +  str(now.year) + "_" + str(now.month) + "_" + str(now.day) + "_" + str(now.hour) + "_" + str(now.minute) + "_" + str(now.second) + "_"

    subprocess.Popen(["rtmpdump", "-r", config.STREAM_URL + "0_0", "-o", out_file_name + "0_0" ] )
    subprocess.Popen(["rtmpdump", "-r", config.STREAM_URL + "0_1", "-o", out_file_name + "0_1" ])
    subprocess.Popen(["rtmpdump", "-r", config.STREAM_URL + "1_0", "-o", out_file_name + "1_0" ])
    subprocess.Popen(["rtmpdump", "-r", config.STREAM_URL + "1_1", "-o", out_file_name + "1_1" ])




class SocketProtocol(WebSocketClientProtocol):

    
    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

        time.sleep(5)
        #message = cameracommand.getCameraInfo()
        message = cameracommand.getFile(cameracommand.FactoryCalib)
        self.mfile = 0
        self.audiosync = 0
        self.sendMessage(message)


    def onMessage(self, payload, isBinary):
        print("Message from cam received")
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
            #print("{:02x}".format(payload))
            ret = cameracommand.transReply(payload)

            time.sleep(1)
            if ret == 'retry':
                if self.mfile == 0:
                    message = cameracommand.getFile(cameracommand.RigParam)
                    self.mfile = 1
                    self.sendMessage(message)
                elif self.mfile == 1:
                    message = cameracommand.startVideoCmd(config.STREAM_URL)
                    self.sendMessage(message)

            if ret == "video_ok":   
                print("SUCCESS Camera is streaming")
                message = cameracommand.CameraAudioSync()
                self.audiosync = 1
                self.sendMessage(message)

            if ret == "cam_ok" and self.audiosync == 1: 
                print("SUCCESS : Camera started and streaming A/V")
                if config.DUMP:
                    startDump()

        else:
            print("Text message received: ")
            print(payload)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
    


class WSocket:
    
    def __init__(self):
        pass

    def connect(self, url, host, port):
        try:
            import asyncio 
        except ImportError:
             # Trollius >= 0.3 was renamed
             import trollius as asyncio

        proto = [ "camctrl-protobuf/1.0" ]
        self.loop = asyncio.new_event_loop()
        self.factory = WebSocketClientFactory(url, protocols=proto, loop=self.loop)
        self.factory.protocol = SocketProtocol
        self.factory.setProtocolOptions(autoPingInterval=5, autoPingTimeout=5)

        #self.loop = asyncio.get_event_loop()
        coro = self.loop.create_connection(self.factory, host, port)
        self.loop.run_until_complete(coro)

        self.thread = threading.Thread(target=self._poll, name="Poll Camera")
        self.thread.daemon = True
        self.thread.start()


    def _poll(self):
        self.loop.run_forever() 

    def stop(self):
        self.loop.close()

    def sendRequest(self, message):
        self.factory.protocol().sendMessage(message, isBinary=True)
