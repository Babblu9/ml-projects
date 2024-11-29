import cv2

# Initialize video capture and load Haar cascades
video = cv2.VideoCapture(0)
faceCascade = cv2.CascadeClassifier("C:/Users/Sai Kumar/Documents/SAI/ML PROJECTS/Smile Selfie Capture Project  [OPEN CV]/dataset/haarcascade_frontalface_default.xml")
smileCascade = cv2.CascadeClassifier("C:/Users/Sai Kumar/Documents/SAI/ML PROJECTS/Smile Selfie Capture Project  [OPEN CV]/dataset/haarcascade_smile.xml")

while True:
    success, img = video.read()
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(grayImg, 1.1, 4)
    keyPressed = cv2.waitKey(1)

    for x, y, w, h in faces:
        # Draw a rectangle around the detected face
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 3)
        smiles = smileCascade.detectMultiScale(grayImg, 1.8, 15)

        for sx, sy, sw, sh in smiles:
            # Draw a rectangle around the detected smile
            img = cv2.rectangle(img, (sx, sy), (sx + sw, sy + sh), (100, 100, 100), 5)

            # Display message and exit immediately
            print("Smile detected!")
            video.release()
            cv2.destroyAllWindows()
            exit()

    # Show live video feed
    cv2.imshow('Live Video', img)

    # Quit if 'q' is pressed
    if keyPressed & 0xFF == ord('q'):
        break

# Release resources
video.release()
cv2.destroyAllWindows()
