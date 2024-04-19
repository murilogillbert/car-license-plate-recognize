import numpy as np
import cv2
import easyocr
import os
print("Running")

harcascade = "model\haarcascade_plate_number.xml"

#Setting the VideoCapture indicating the first camera connected on pc
cap = cv2.VideoCapture(0)

#Setting the width and heigth of the capture
cap.set(3,640) #width
cap.set(4,480) #height

#setting the minimal area to be considered a plate
min_area = 500

#checking the 'plates' directory and saving the number of photos in the 'count' variable
dir_path = "plates"
count = 0
for iten in os.listdir(dir_path):
    count+=1

#Executing the capture  
while True:
    succed, img = cap.read()

    plate_cascade = cv2.CascadeClassifier(harcascade)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    for (x,y,w,h) in plates:
        area = w * h

        if area >min_area:
            cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0),2)
            cv2.putText(img,"Number Plate", (x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,255),2)
        img_roi = img[y:y+h, x:x+w]
        cv2.imshow("ROI",img_roi)


    cv2.imshow("Result", img)

#If you want to save the plate, press 's'
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("plates/scaned_img_" + str(count) + ".jpg", img_roi)
        cv2.rectangle(img, (0,200), (640,300), (0,255,0), cv2.FILLED)
        cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
        cv2.imshow("Results",img)
        cv2.waitKey(500)
        count += 1
#If you want to quit the application, press 'q'
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Reading a plate image and outputing your text
reader = easyocr.Reader(['en'])
output = reader.readtext('plates\scaned_img_1.jpg')
print(output[0][1])
