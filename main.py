import os,time
import cv2

def connect():
    try:
        os.system('adb connect 127.0.0.1:7555')
    except:
        print('连接失败')

def click(x, y,name):
    print(name)
    print(x,y)
    os.system('adb -s '+name+' shell input tap %s %s' % (x, y))

def screenshot(name):
    path = os.path.abspath('.') + '\images.png'
    os.system('adb -s '+name+' shell screencap /data/screen.png')
    os.system('adb -s '+name+' pull /data/screen.png %s' % path)

def resize_img(img_path):
    img1 = cv2.imread(img_path, 0)
    img2 = cv2.imread('images.png', 0)
    height, width = img1.shape[:2]
    ratio = 1920 / img2.shape[1]
    size = (int(width/ratio), int(height/ratio))
    return cv2.resize(img1, size, interpolation = cv2.INTER_AREA)

def Image_to_position(image, m = 0):
    image_path = 'images/' + str(image) + '.png'
    screen = cv2.imread('images.png', 0)
    template = resize_img(image_path)
    methods = [cv2.TM_CCOEFF_NORMED, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED]
    image_x, image_y = template.shape[:2]
    result = cv2.matchTemplate(screen, template, methods[m])
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    #print(image,max_val)
    if max_val > 0.7:
        global center
        center = (max_loc[0] + image_y / 2, max_loc[1] + image_x / 2)
        return center
    else:
        return False

def mainrun(nameList,images):
    now=''
    
    for image in images:
        while True:
            screenshot(nameList[0])
            if Image_to_position(image, m = 0) != False:
                for name in nameList:
                    while True:
                        screenshot(name)
                        if Image_to_position(image, m = 0) != False:
                            print(image)
                            now=image
                            print(center)
                            click(center[0], center[1],name)
                            #time.sleep(0.5)
                            break
                break
def tohomepage(nameList):
    for i in range(0,3):
        screenshot(nameList[0])
        if Image_to_position('skip', m = 0) != False:
            for name in nameList:
                while True:
                    screenshot(name)
                    if Image_to_position('skip', m = 0) != False:
                        print('skip')
                        now='skip'
                        print(center)
                        click(center[0], center[1],name)
                        time.sleep(0.5)
                        break
                    else:
                        click(640,360,name)
            break
        else:
            click(640,360,nameList[0])

def login(name,idset):
    now=''
    
    for image in ['ID','password','login']:
        while True:
            screenshot(name)
            if Image_to_position(image, m = 0) != False:
                print(image)
                now=image
                print(center)
                click(center[0], center[1],name)
                if image=='ID':
                    os.system('adb -s '+name+' shell input text "'+idset[0]+'"')
                elif image=='password':
                    os.system('adb -s '+name+' shell input text "'+idset[1]+'"')
                break
            else:
                click(1200,50,name)

def getaccount():
    lines=[]
    with open('accountlist.txt', 'r') as f:
        lines=f.readlines()
        return lines
if __name__ == '__main__':

    accountList=getaccount()#获取账号列表
    connect()
    result = os.popen('adb devices')  
    res = result.read()
    lines=res.splitlines()[1:]
    
    for i in range(0,len(lines)):
        lines[i]=lines[i].split('\t')[0]
    lines=lines[0:-1]
    print(lines)
    #os.system('adb shell wm size')


    '''
    共25个号，5开为例
    '''    
    for step in range(0,5):
        '''
        依次登陆5个号
        '''
        for i in range(0,len(lines)):
            login(lines[i],[accountList[i+step*5].split(' ')[0],accountList[i+step*5].split(' ')[1][0:-1]])
            print(accountList[i+step*5].split(' ')[0])
        tohomepage(lines)
        mainrun(lines,['close_white'])
        '''
        地下城战斗
        '''
        mainrun(lines,['explor','underground','normalUD','ok_blue','floor1','challenge_blue'])
        mainrun(lines,['u1','pico','kkl','cat','getassist','assist','battlestart','ok_blue'])
        mainrun(lines,['next_step','ok_white','withdraw','ok_blue'])
        
        '''
        回登陆页，开始下一次iteration
        '''
        mainrun(lines,['mainpage','backtotitle','ok_blue'])
    
    os.system('adb kill-server')