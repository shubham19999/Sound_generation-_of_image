import pyautogui
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time


greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pyautogui.FAILSAFE=False

screenWidth, screenHeight = pyautogui.size()

vs = VideoStream(src=0).start()

time.sleep(2.0)

while True:
    frame = vs.read()

    frame = cv2.resize(frame, (1960,1600))
    area1 = cv2.rectangle(frame, (0, 0), (150, 1600), (255, 0, 255), 1)
    area2 = cv2.rectangle(frame, (1810, 0), (1960, 1600), (255, 0, 255), 1)
    frame = cv2.flip(frame, 1)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:

        c = max(cnts, key = cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        print(center)
        x = center[0]
        y = center[1]

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

        pyautogui.moveTo(x, (y-250))
        if x in range(1760,1960):
            #pyautogui.press('right')
            pyautogui.click()
        if x in range(0,200):
            #pyautogui.press('left')
            pyautogui.click()

    cv2.imshow("Frame", frame)
    #cv2.imshow("HSV", hsv)
    #cv2.imshow("MASKED", mask)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

cv2.destroyAllWindows()