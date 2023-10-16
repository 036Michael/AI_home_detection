from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import line_notify 
import requests


# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("converted_keras\keras_model.h5", compile=False)

# Load the labels
class_names = open("converted_keras\labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

while True:
    # Grab the webcamera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    # Show the image in a window
    cv2.imshow("Webcam Image", image)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    if confidence_score < 0.5:
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")    
        
        #line notify
        url = "https://notify-api.line.me/api/notify"
        token = "Z3knL5oA7dzsVDbFrZ63fuAIiusZltjuiTLSL5poVIk"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        message = "你好，这是一条Line Notify通知！有賊！"
        
        payload = {
            "message": message
        }
        response = requests.post(url, headers=headers, data=payload)
        print(response.text)  # 打印API响应
        #line notify end

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()


