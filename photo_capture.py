import cv2 as cv
import numpy as np
import os
import glob

def into():
    print("Please stay still and don't close your eyes")

face_cascade = cv.CascadeClassifier("haarcascade_frontalface_alt_tree.xml")

#open and check the camera
camera = cv.VideoCapture(0)
if not camera.isOpened():
    print("ERROR: Camera cannot opened")
    exit()

title = "Don't move and open your eyes"

while (True):
    # Capture the video frame
    ret, frame = camera.read()
    captured_gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #apply filter
    captured_gray_frame = cv.bilateralFilter(captured_gray_frame, 5,1,1)
    faces = face_cascade.detectMultiScale(captured_gray_frame, scaleFactor=3, minNeighbors=5)
    for (x,y,z,t) in faces:
        print("coordinates:" , x,y,z,t)
        gray_pic = captured_gray_frame[y:y+t, x:x+z]
        took_photo = "shoots/captured.png"
        font = cv.FONT_HERSHEY_COMPLEX_SMALL

        if(x==242, y==152, z==180, t==180):
           cv.imwrite(took_photo, gray_pic)
        else :
           cv.putText(frame, title, (240, 240),font, 1, (0, 255, 255), 
                2, cv.LINE_4 )

        color = (255, 0, 0)
        border = 2
        width_x_coord = x + z  #end coordination of x
        height_y_coord = y + t #end coordination of y
        cv.rectangle(frame, (x,y), (width_x_coord, height_y_coord), color, border)

    #showing 
    cv.imshow("VIDEO", frame)
    #waits for the user's response through a key press.
    #hit the q to quit 
    if(cv.waitKey(14) & 0xFF == ord('q')):
        break
#release handle
camera.release()
cv.destroyAllWindows()


#filter
path = glob.glob("shoots/*.png")
images = []
for img in path:
    image = cv.imread(str(img))
    image=cv.resize(image,(200,200))
    images.append(image)

print(images)

