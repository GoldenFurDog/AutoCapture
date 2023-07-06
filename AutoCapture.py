# AutoCapture v1.0
# adapted from auto_screenshot v1.2.0
# by goldenfurdog

##########

from PIL import ImageGrab
from os import path, mkdir
from time import sleep
from sys import exit
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime

##########

def getJsonInfo(path='./auth.json'):
    from json import load
    from sys import exit
    from time import sleep
    try:
        with open(path,'r') as f:
            infos = load(f)
            return infos
    except:
        print(path,' open file failed')
        sleep(3)
        exit()

'''
def getAuthInfo(infos={'key':'value'},userkey='example'):
    listInfo = []
    info = infos.get(userkey)
    for i in ['Acct','SMTP','Pswd']:
        listInfo.append(info.get(i))
    return listInfo
'''

def sendEmail(sendInfo):
    # sendInfo = [Account,SMTP,Password,msg]
    import smtplib
    server = smtplib.SMTP_SSL(sendInfo[1],465)
    server.set_debuglevel(1)
    server.login(sendInfo[0],sendInfo[2])
    try:
        #print('msg',sendInfo[3])
        server.sendmail(sendInfo[0],[sendInfo[0]],sendInfo[3].as_string())
        print('sendEmail() Done')
    except:
        print('sendEmail() Failed')
    server.quit()

##########

def AutoCapture():
    userkey = input('Type in your Userkey:\n')
    infos = getJsonInfo()
    listInfo = []
    info = infos.get(userkey)
    print('Information comfirm:')
    for i in ('Acct','SMTP','Pswd'):
        p = info.get(i)
        print(i,':',p,end=' | ')
        listInfo.append(p)
    print()
    savePath = './saves'
    if not path.exists(savePath):
        try:
            mkdir(savePath)
        except:
            print('mkdir',savePath,'failed')
            sleep(3)
            exit()
    run = True
    test = False
    #test = True
    while run:    
        nowtime = int(datetime.now().strftime('%M%S'))
        while  nowtime != 0000 and nowtime != 1500 and nowtime != 3000 and nowtime != 4500 and not test:
            nowtime = int(datetime.now().strftime('%M%S'))
        imageName = './saves/image_%s.jpg'%(datetime.now().strftime('%Y_%m_%d %H_%M_%S'))
        try:
            image = ImageGrab.grab()
            image.save(imageName)
            msg = MIMEText('截图服务正常运转中..','plain','utf-8')
            msg['From'] = Header("AutoCaptureServer <%s>"%(listInfo[0]))
            msg['To'] =  Header('%s <%s>'%(userkey, listInfo[0]), 'utf-8')
            msg['Subject'] = Header('AutoCapture邮箱日志','utf-8')
            listInfo.append(msg)
            sendEmail(listInfo)
            print('截图服务正常运转中..')
        except:
            msg = MIMEText('截图服务运转异常,15分钟后重试','plain','utf-8')
            msg['From'] = Header("AutoCaptureServer <%s>"%(listInfo[0]))
            msg['To'] =  Header('%s <%s>'%(userkey, listInfo[0]), 'utf-8')
            msg['Subject'] = Header('AutoCapture邮箱日志','utf-8')
            listInfo.append(msg)
            sendEmail(listInfo)
            print('截图服务运转异常,15分钟后重试')
        if test:
            run = False
        else:
            sleep(1)

##########

if __name__ == '__main__':
    AutoCapture()
    input()

