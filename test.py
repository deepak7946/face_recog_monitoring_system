import cv2
from time import sleep

vid_cap = cv2.VideoCapture(0)
print("Created camera pbj")

print("Starting loop")
while True:
    _, frame = vid_cap.read()
    cv2.imwrite('test.jpg', frame) 
