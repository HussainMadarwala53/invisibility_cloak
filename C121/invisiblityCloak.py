import cv2
import numpy as np
import time

#to save the output in avi format
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0,(640,48))
#to start the camera
cam = cv2.VideoCapture(0)
#to start the program after two seconds
time.sleep(2)
bg = 0
#to capture the background for 60 frames
for i in range(60):
    #to return the read images inside the bg var
    ret, bg = cam.read()
#to flip the bg img
bg = np.flip(bg,axis = 1)

#to read the captured images until the camera is open
while(cam.isOpened()):
    ret, img = cam.read()
    if not ret:
        break
    img = np.flip(img,axis = 1)
    #to convert the color of the img from bgr to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #to generate a mask to detect red color
    lower_red = np.array([0,120,50])
    upper_red = np.array([10,255,255])
    mask_one = cv2.inRange(hsv,lower_red,upper_red)
    
    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask_two = cv2.inRange(hsv,lower_red,upper_red)
    
    mask_one=mask_one+mask_two
    #to open and expand the img where there is mask_one color
    mask_one = cv2.morphologyEx(mask_one, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask_one = cv2.morphologyEx(mask_one, cv2.MORPH_DILATE, np.ones((3,3), np.uint8))
    
    #to select the part tat doesnot have mask one
    mask_two = cv2.bitwise_not(mask_one)
    
    #to save the part of the img without using red color
    res_one = cv2.bitwise_and(img,img,mask=mask_two)
    res_two = cv2.bitwise_and(bg,bg,mask=mask_two)
    #to generate the final output
    final_output = cv2.addWeighted(res_one, 1, res_two, 1,0)
    output_file.write(final_output)
    cv2.imshow("magic", final_output)
    cv2.waitKey(1)
    
cam.release()
#out.release()
cv2.destroyAllWindows()
