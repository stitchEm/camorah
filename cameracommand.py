import CamAPI_pb2

import urllib.request
import datetime
import os
import config


FactoryCalib = "factoryPresetsProject.ptv"
RigParam = "rigParameters.json"

video_reply_op = { CamAPI_pb2.Video.Reply.RetCode.Value('UNKNOWN_ERROR') : "unknow_error",
           CamAPI_pb2.Video.Reply.RetCode.Value('SUCCESS') : "success",
           CamAPI_pb2.Video.Reply.RetCode.Value('NO_VIDEO_RUNNING') : "novideo"
          }

fs_reply_ret = {   CamAPI_pb2.Fs.Reply.RetCode.Value('UNKNOWN_ERROR') : "unknowm error",
           CamAPI_pb2.Fs.Reply.RetCode.Value('SUCCESS') : "success",
           CamAPI_pb2.Fs.Reply.RetCode.Value('INVALID_SYNTAX') : "invalid syntax",
           CamAPI_pb2.Fs.Reply.RetCode.Value('UNEXPECTED_COMMAND') : "unexpected command",
           CamAPI_pb2.Fs.Reply.RetCode.Value('UNEXPECTED_COMMAND') : "unexpected command",
           CamAPI_pb2.Fs.Reply.RetCode.Value('INVALID_INPUT_VALUE') : "invalid input value",
           CamAPI_pb2.Fs.Reply.RetCode.Value('FILE_NOT_FOUND') : "file not found",
           CamAPI_pb2.Fs.Reply.RetCode.Value('NO_SPACE') : "no space",
           CamAPI_pb2.Fs.Reply.RetCode.Value('BROKEN_LINK') : "broken link"}

cam_reply_ret = {   CamAPI_pb2.Cam.Reply.RetCode.Value('UNKNOWN_ERROR') : "unknowm error",
            CamAPI_pb2.Cam.Reply.RetCode.Value('SUCCESS') : "success"
        }

def startVideoCmd(url):
    print("Start Video")
    api = CamAPI_pb2.Api()
    api.video.op = CamAPI_pb2.Video.OpCode.Value('START')
    api.video.url = url
    return api.SerializeToString()


def getCameraInfo():
    api = CamAPI_pb2.Api()
    api.cam.op = CamAPI_pb2.Cam.OpCode.Value('GET_CAMERA_MODE')
    return api.SerializeToString()


def CameraAudioSync():
    print("Audio SYNC")
    api = CamAPI_pb2.Api()
    api.cam.op = CamAPI_pb2.Cam.OpCode.Value('AUDIO_SYNC')
    return api.SerializeToString()


def getFile(filename):
    print("get file" + filename)
    api = CamAPI_pb2.Api()
    api.fs.op = CamAPI_pb2.Fs.OpCode.Value('GET')
    api.fs.file_name = filename
    return api.SerializeToString()
    

def transReply(data):
    api = CamAPI_pb2.Api()
    api.ParseFromString(data)
    
    if api.HasField('api_reply'):
        print("Qpi reply")
        pass    
    elif api.HasField('event'):
        print("Event")
        if api.event.msg == CamAPI_pb2.Event.MsgId.Value('VIDEO_FAIL'):
            print("Cam video fail")
            return 'retry'
        if api.event.msg == CamAPI_pb2.Event.MsgId.Value('UNKMOWN'):
            print("Cam fail unknown")
            return 'retry'
    elif api.HasField('video_reply'):
        print("Video Reply")
        print(video_reply_op[api.video_reply.op])
        if api.video_reply.op == CamAPI_pb2.Video.Reply.RetCode.Value('SUCCESS'):
            return 'video_ok'

    elif api.HasField('fs_reply'):
        print("FS Reply")
        print(fs_reply_ret[api.fs_reply.ret])
        if api.fs_reply.ret == CamAPI_pb2.Fs.Reply.RetCode.Value('SUCCESS'):
            print("file url " + str(api.fs_reply.url))
            try:
                response = urllib.request.urlopen(api.fs_reply.url.decode("ascii"))
                file_content = response.read()
            except urllib.error.URLError as e:
                print(e.reason)
                return 'retry'
            now = datetime.datetime.now()
            print(os.path.basename(api.fs_reply.url))
            out_file_name = config.OutDir + os.path.basename(str(api.fs_reply.url)) + "_" + str(now.year) + "_" + str(now.month) + "_" + str(now.day) + "_" + str(now.hour) + "_" + str(now.minute)
            with open(out_file_name, "w") as outfile:
                outfile.write(file_content.decode("utf8"))
        

        return 'retry'
    elif api.HasField('cam_reply'):
        print("CAM Reply")
        if api.cam_reply.ret == CamAPI_pb2.Cam.Reply.RetCode.Value('SUCCESS'):
            print("cam reply success")
            return 'cam_ok'
        if api.cam_reply.ret == CamAPI_pb2.Cam.Reply.RetCode.Value('UNKNOWN_ERROR'):
            print("cam trply unkmown error")
