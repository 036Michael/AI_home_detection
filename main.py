from keras.models import load_model
import cv2
import numpy as np
import lineNotify
# import screenshot

# Load the model
model = load_model("converted_keras\keras_model.h5", compile=False)

# Load the labels
class_names = open("converted_keras\labels.txt", "r").readlines()

# Load the face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# CAMERA can be 0 or 1 based on the default camera of your computer
camera = cv2.VideoCapture(0)

while True:
    # Grab the web camera's image.
    ret, image = camera.read()

    # Resize the raw image for better performance
    small_image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)

    # Convert the image to grayscale for face detection
    gray_image = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    # faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.2, minNeighbors=5, minSize=(25, 25))
    
    for (x, y, w, h) in faces:
        # Draw a green rectangle around the detected face
        color = (0, 255, 0)  # Green color in BGR
        cv2.rectangle(small_image, (x, y), (x+w, y+h), color, 2)

        # Extract the face from the image
        face = small_image[y:y+h, x:x+w]

        # Resize the face for the model
        face = cv2.resize(face, (224, 224), interpolation=cv2.INTER_AREA)

        # Make the image a numpy array and reshape it to the model's input shape.
        face = np.asarray(face, dtype=np.float32).reshape(1, 224, 224, 3)

        # Normalize the image array
        face = (face / 127.5) - 1
        
        # Predicts the model
        prediction = model.predict(face)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]
        # Display the class name at the top-left corner
        text = f"{class_name[2:]} {str(np.round(confidence_score * 100))[:-2]}%"
        cv2.putText(small_image, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        unknown = class_names[4]
        if confidence_score > 0.8 and (class_names[0] or class_names[1] or class_names[2] or class_names[3]):
            print("是", class_name[2:], end="")
            print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
            print("-------------------------")

        elif (class_name == unknown) and (confidence_score > 0.75):
            print("是", unknown[2:], end=" ")
            print("已發送通知與截圖至LineNotify!!")
            print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
            print("-------------------------")
            cv2.imwrite('screenshot.jpg', small_image)
            class_name = class_name[2:]
            lineNotify.check_response_Line(class_name)
            
    # Show the image in a window
    cv2.imshow("Webcam Image", small_image)

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()
