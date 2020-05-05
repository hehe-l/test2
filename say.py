import pyaudio,itchat,random,cv2
import myrequest
import wave,tqdm,json,requests,os
import speech_recognition as sr
from os import path
from pydub import AudioSegment
from itchat.content import *
import test,mypc
#录音
def get_audio(name):
    record_second=3
    CHUNK=1024
    FORMAT=pyaudio.paInt16
    CHANNELS=2
    RATE=44100
    pa=pyaudio.PyAudio()
    stream=pa.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
    wf=wave.open(name,'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    print('开始录音')
    for i in range(0,int(RATE/CHUNK*record_second)):
        data=stream.read(CHUNK)
        wf.writeframes(data)
    print('完成')
    stream.stop_stream()
    stream.close()
    pa.terminate()
    wf.close()
#语音识别
def tostr(name):
#    AUDIO_FILE=path.join(path.dirname(path.realpath("C://Users\samsung\Desktop\test\output.wav")),name)
    r=sr.Recognizer()
    with sr.AudioFile(name) as source:
        audio = r.record(source)
        type(audio)
    try:
         print("Google Speech Recognition thinks you said " + r.recognize_google(audio,language='zh-CN'))
         return r.recognize_google(audio,language='zh-CN')
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
def get_sizhi_response(msg):
    apiUrl = 'https://api.ownthink.com/bot'
    apiKey = '2d95ab3f11124f418ec0a800e6ee9d52'#这里填写你自己申请的机器人apiKey
    data = {
        "spoken": msg,
        "appid": apiKey,
        "userid": 'hehe'
    }

    headers = {'content-type': 'application/json'} 
    try:
        req=requests.post(apiUrl, headers = headers, data = json.dumps(data))
        return req.json()
    except:
        return
def sizhi_msg(msg):
    return_msg = '我是个笨笨的机器人，我CPU好像挂了~_~![自动回复]'
    replyjson = get_sizhi_response(msg)
    if replyjson['message'] == 'success':
        return_msg = replyjson['data']['info']['text'].replace('小思','傻子明~').replace('思知机器人','傻子明~');
        print("自动回复："+return_msg)
    # a or b --》 如果a不为空就返回a，否则返回b
    return return_msg
def action():
    get_audio('output.wav')
    order=tostr('output.wav')
    if '拍照'==order:
        test.yface()
    elif '打开摄像头'==order:
        mypc.test2()
    elif '网页'==order:
        mypc.test('www.baidu.com')
    elif order is None:
         action()
    else:
        sizhi_msg(order)
    action()
def itchat_auto():
    @itchat.msg_register([itchat.content.TEXT,itchat.content.RECORDING],isGroupChat=True,isFriendChat=True)#,itchat.content.PICTURE
    def private_text_chat(private_msg):
        author=itchat.search_friends(nickName='木木九日车干')[0]['UserName']
        groups=itchat.get_chatrooms(update=True)
        for g in groups:
            if g['NickName']=='三乡没有温泉团':
                to_group=g['UserName']
        if private_msg['FromUserName']==to_group:#to_group
            if private_msg['Type']=='Recording':
                private_msg['Text']('output.mp3')
                dealMp3('output.mp3','output.wav')
                msg=tostr('output.wav')
                r_msg=sizhi_msg(msg)
                itchat.send_msg('傻子明：'+r_msg,toUserName=to_group)
            else:
                if private_msg.get('Text')[0]=='@':
                    print(private_msg.get('Text')[8:])
                    r_msg=myrequest.search(private_msg.get('Text')[8:])
                    itchat.send_msg('傻子明：'+r_msg,toUserName=to_group)
                else:
                    msg=private_msg['Text']
                    r_msg=sizhi_msg(msg)
                    print(msg)
                #username = g['UserName']
                    itchat.send_msg('傻子明：'+r_msg,toUserName=to_group)
        elif private_msg['FromUserName']==author:
            if private_msg['Type']=='Picture':
                #value=int(random.uniform(0,6))
                #msg=['说人话','你是傻子吗','打字会不会','呵呵','哦','好的','']
                return '' 
            elif private_msg['Type']=='Recording':
                private_msg['Text']('output.mp3')
                dealMp3('output.mp3','output.wav')
                msg=tostr('output.wav')
            else:
                msg=private_msg['Text']
            if msg=='拍照':
                cap=cv2.VideoCapture(0)
                ret,frame=cap.read()
                cv2.imwrite("static/img/123.png",frame)
                f='static/img/123.png'
                itchat.send_image(f,toUserName='filehelper')
                return ''
            elif msg=='人脸':
                test.yface()
                g='static/img/456.png'
                itchat.send_image(g,toUserName='filehelper')
                return ''
            elif msg[0]=='@':
                r_msg=myrequest.search(private_msg.get('Text')[8:])
                itchat.send_msg('傻子明：'+r_msg,toUserName='filehelper')#filehelper
                return ''
            else:
                r_msg=sizhi_msg(msg)
                itchat.send_msg('傻子明：'+r_msg,toUserName='filehelper')
#        else:
#            msg=private_msg['Text']
#            print(msg)
#            r_msg=sizhi_msg(msg)
#            itchat.send(msg='自动回复：'+r_msg,toUserName='filehelper')
    itchat.auto_login(hotReload=True)
    itchat.run()
def dealMp3(filePath,fileName):
    sound = AudioSegment.from_mp3(filePath)
    #获取原始pcm数据
    data=sound._data
    sound_wav = AudioSegment(
        #指定原始pcm文件
        # raw audio data (bytes)
        data = data,
        #指定采样深度，可选值1,2,3,4
        # 2 byte (16 bit) samples
        sample_width = 2,
        #指定采样频率
        # 44.1 kHz frame rate
        # 16kHz frame rate
        frame_rate = 16000,
        #指定声道数量
        # stereo or mono
        channels = 1
    )
    #导出wav文件到当前目录下
    sound_wav.export(fileName,format='wav')
    # 判断生成wav格式的文件成功没
    isDeal = os.path.exists(os.getcwd()+'\\'+fileName)
    #如果wav文件生成了就删除mp3文件 - -这个可以不参考
    if isDeal:
        #删除mp3文件
        os.remove(filePath)
if __name__ == '__main__':
    AudioSegment.ffmpeg = os.getcwd()+'\\ffmpeg.exe'
    AudioSegment.ffprobe = os.getcwd()+'\\ffprobe.exe'
    itchat_auto()
   
    
    
