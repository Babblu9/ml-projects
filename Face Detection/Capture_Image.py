import cv2
import os


print("Enter the name: ")
img_counter=input()

cam=cv2.VideoCapture(0)
cv2.namedWindow("Capture Image")
path = 'ImagesAttendance'

while True:
  ret, frame=cam.read()
  
  if not ret:
    print("failed to grab frame")
    break

  cv2.imshow("Test", frame)

  k=cv2.waitKey(1)

  if k%256==27:
    print("Exit key pressed:")
    break

  elif k%256==32:
    img_name="{}.jpeg".format(img_counter)
    cv2.imwrite(os.path.join(path,img_name), frame)
    print("Image Captured")
    break

