import numpy as np
import cv2 as cv
from datetime import datetime
import time
import os
# --------------------------
# 創建文件夾
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"文件夾 '{folder_path}' 創建成功")
        return folder_path
    else:
        i = 1
        while True:
            new_folder_path = f"{folder_path}({i})"
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
                print(f"文件夾 '{new_folder_path}' 創建成功")
                # print(new_folder_path)
                return new_folder_path
            i += 1

formatted_time = datetime.now().strftime("%Y年%m月%d日%H時%M分%S秒")
year = formatted_time[:4]
month = formatted_time[5:7]
day = formatted_time[8:10]
hour = formatted_time[11:13]
minute = formatted_time[14:16]
second = formatted_time[17:19]
ss = (f"{year}-{month}-{day}")

new_folder = create_folder('C:/Users/DC/Desktop/git-repository/face-detection/images/{}'.format(ss))  # 創建一個新的文件夾
# --------------------------
cap = cv.VideoCapture(0)
# 我的相機最高 1280x720
# cap.set(cv.CAP_PROP_FRAME_WIDTH,1280)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT,720)

last_screenshot_time = time.time()
o = 0

if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # print(frame.shape)
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
    current_time = time.time()  
    if current_time - last_screenshot_time >= 0.1 :  # 每n秒截圖一次    
        formatted_time = datetime.now().strftime("%Y年%m月%d日%H時%M分%S秒")
        # 提取年月日時分秒
        year = formatted_time[:4]
        month = formatted_time[5:7]
        day = formatted_time[8:10]
        hour = formatted_time[11:13]
        minute = formatted_time[14:16]
        second = formatted_time[17:19]

        # print(f"{o},{year}年{month}月{day}日,{hour}時{minute}分{second}秒")
        print(o,"張")
        ss = (f"{year}-{month}-{day},{hour}-{minute}-{second}s")#取檔案名稱
        cv.imwrite('{}/{}-{}.png'.format(new_folder,o,ss), frame)#
        # cv.imwrite('{}/{}.png'.format(new_folder,ss), frame) #如果沒 o 就會等一秒後印出
        o = o + 1
        
        last_screenshot_time = current_time
    
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()