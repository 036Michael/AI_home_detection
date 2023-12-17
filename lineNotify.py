import line_notify
import requests

# def lineNotifyMessage(str):
#     print(str)

def check_response_Line(name):
    url = "https://notify-api.line.me/api/notify"
    token = "" #改成自己的token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    message = "有人來了-不明人物" #提醒已啟動
    payload = {
        "message": message + name
    }
    
    # image = open('examples/HSB.jpg', 'rb')    # 以二進位方式開啟圖片
    image = open('screenshot.jpg', 'rb')    # 以二進位方式開啟圖片
    
    imageFile = {'imageFile' : image}   # 設定圖片資訊

    # 做 API 呼叫
    response = requests.post(url, headers=headers, data=payload , files=imageFile)
    
    # 檢查 HTTP 狀態碼
    if response.status_code == 200:
        print("API 呼叫成功！")
    else:
        print("API 呼叫失敗，狀態碼：", response.status_code)

    # 打印API回應
    print(response.text)
    

