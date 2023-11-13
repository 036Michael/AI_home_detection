import numpy as np
import cv2 as cv
from datetime import datetime
import time
import pyautogui
import os


cap = cv.VideoCapture(0)
# cap.set(cv.CAP_PROP_FRAME_WIDTH,640)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT,480)

last_screenshot_time = time.time()
o = 0


# os.makedirs(output_directory, exist_ok=True)

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
    if cv.waitKey(1) == ord('a') :  # 每10秒截圖一次    
        formatted_time = datetime.now().strftime("%Y年%m月%d日%H時%M分%S秒")
    
        # 保存圖片
        cv.imwrite('D:/project code/imge/{}.png'.format(o), frame) 
        
        o = o + 1
        

        # 提取年月日時分秒
        year = formatted_time[:4]
        month = formatted_time[5:7]
        day = formatted_time[8:10]
        hour = formatted_time[11:13]
        minute = formatted_time[14:16]
        second = formatted_time[17:19]

        print(f"年: {year}, 月: {month}, 日: {day}, 時: {hour}, 分: {minute}, 秒: {second}")

        last_screenshot_time = current_time
    
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()


