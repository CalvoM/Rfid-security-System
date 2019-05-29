import numpy as np
import cv2 
def pigaPicha():
    cap=cv2.VideoCapture(0)

    while True:
        ret,frame=cap.read()
        cv2.imshow('img1',frame)
        k=cv2.waitKey(1)
        if k ==ord('y'):
            cv2.imwrite('Calvin.jpg',frame)
            cv2.destroyAllWindows()
            break
        elif k==ord('c'):
            print('Hey')
    cap.release()