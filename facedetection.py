import dlib                   # 導入dlib庫
import cv2                    # 導入OpenCV庫
import os                     # 導入OS庫
import numpy as np               # 導入numpy庫
import requests
import line_notify

url = "https://notify-api.line.me/api/notify"
token = "OLYczNdlOmAzBQ8ztc07mIan87MHfkJfPHuBvW4XQXk"
headers = {
    "Authorization": f"Bearer {token}"
}
message = "OPEN Camera"
payload = {
    "message": message
}

# 做 API 呼叫
response = requests.post(url, headers=headers, data=payload)

# 檢查 HTTP 狀態碼
if response.status_code == 200:
    print("API 呼叫成功！")
else:
    print("API 呼叫失敗，狀態碼：", response.status_code)

# 打印API回應
print(response.text)
# 初始化臉部偵測器和人臉特徵提取器
face_detector = dlib.get_frontal_face_detector()  # 初始化臉部偵測器
face_recognition_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")  # 初始化人臉特徵提取器
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')  # 初始化人臉關鍵點檢測器

# 從參考照片中提取特徵
def get_face_descriptor_from_image(img_path):
    img = cv2.imread(img_path)  # 讀取圖片
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 轉換圖片顏色空間
    dets = face_detector(img_rgb, 1)  # 偵測圖片中的人臉
    if len(dets) == 0:  # 如果沒有偵測到人臉
        return None
    shape = predictor(img_rgb, dets[0])  # 獲取人臉的關鍵點
    face_descriptor = face_recognition_model.compute_face_descriptor(img_rgb, shape)  # 提取人臉特徵
    return face_descriptor

# 讀取 我 的照片並獲取其特徵
reference_descriptor = get_face_descriptor_from_image("HSB.jpg") #改為自己照片名稱

if reference_descriptor is None:  # 如果無法從我的照片中提取特徵
    print("無法從我的照片中檢測到臉部。")
    exit()

# 開始攝像頭的人臉識別
cap = cv2.VideoCapture(0)  # 開啟攝像頭
print("open camera ~")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)#更改視窗寬
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)#更改視窗高
Frame_count = 0
... # 其他程式碼保持不變

while True:
    Frame_count += 1
    ret, frame = cap.read()  # 讀取攝像頭的幀
    if Frame_count % 3 == 0 :
        if not ret:  # 如果無法讀取幀
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 轉換幀的顏色空間
        dets = face_detector(frame_rgb, 1)  # 偵測幀中的人臉
        
        for det in dets:  # 對每個偵測到的人臉進行處理
            
            # 畫出矩形，並將其顏色設為綠色
            cv2.rectangle(frame, (det.left(), det.top()), (det.right(), det.bottom()), (0, 255, 0), 2)
            
            shape = predictor(frame_rgb, det)  # 獲取人臉的關鍵點
            live_descriptor = face_recognition_model.compute_face_descriptor(frame_rgb, shape)  # 提取人臉特徵

            # 計算兩個人臉匹配程度
            similarity = np.linalg.norm(np.array(reference_descriptor) - np.array(live_descriptor))  # 計算兩個特徵之間的歐式距離
            if similarity < 0.4:  # 如果匹配程度高，匹配程度可自由調整，0.4為目前測試最合格的數值
                print("歡迎回家")
            else:  # 如果匹配程度低
                print("小偷入侵")
                url = "https://notify-api.line.me/api/notify"
                token = "OLYczNdlOmAzBQ8ztc07mIan87MHfkJfPHuBvW4XQXk"
                headers = {
                    "Authorization": f"Bearer {token}"
                }
                message = "警告，你不是大帥哥，楊宗燁超黑!!!"
                payload = {
                    "message": message
                }

                # 做 API 呼叫
                response = requests.post(url, headers=headers, data=payload)

        cv2.imshow("Frame", frame)  
        if cv2.waitKey(1) & 0xFF == ord('q'):  # 如果按下'q'鍵
            break

cap.release()  # 釋放攝像頭資源
cv2.destroyAllWindows()  # 關閉所有OpenCV視窗
