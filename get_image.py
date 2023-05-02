import numpy as np
import cv2 
import os


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()


folder_type = str(input("Enter type: train/val/test\n"))
class_name = str(input("Enter class name: \n"))
folder_path = f"data_set/image/{folder_type}/{class_name}"

if os.path.exists(folder_path):
    pass
else:
    os.makedirs(folder_path)

count = 0
if os.path.exists(os.path.join(folder_path, "count.txt")):
    with open(f'{folder_path}/count.txt', 'r') as file:
        count = int(file.read())
        print(count)
else:
    file = open(f"{folder_path}/count.txt", 'w')


while True:
    ret, frame = cap.read()  # read frame/image one by one     
    
    cv2.imshow("Frame extraction", frame)   # display frame/image
    key = cv2.waitKey(1)
    if key == ord("a"):   
        cv2.imwrite(f"{folder_path}/{count}.jpg", frame)
        print("save image " + str(count) + ".jpg")
        count = count + 1
    if key == ord("q"):  # exit loop on 'q' key press
        print("write to count.txt: " + str(count))
        with open(f"{folder_path}/count.txt", 'w') as file:
            file.write(str(count))
        break
        
cap.release() # release video capture object
cv2.destroyAllWindows()  # destroy all frame windows