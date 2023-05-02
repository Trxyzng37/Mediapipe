import cv2
import mediapipe as mp
import os
import numpy as np 
import csv
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.2, min_tracking_confidence=0.5)
    

folder_type = str(input("\nEnter folder type: (train/val/test)\n"))
class_name = str(input("Enter class name: \n"))
folder_path = f'data_set/image/{folder_type}/{class_name}'
csv_folder_path = f'data_set/data/{folder_type}'
csv_path = f'data_set/data/{folder_type}/{class_name}.csv'

if os.path.exists(csv_folder_path):
    pass
else:
    print("Folder for csv not exist. Creating......")
    os.makedirs(csv_folder_path)

f = open(csv_path, 'w')

for item in os.listdir(folder_path):
    if item.endswith('.jpg'):
        image = cv2.imread(f'{folder_path}/{item}')
        cv2.imshow("f", image)
        time.sleep(0.5)
        cv2.waitKey(1)
        results = hands.process(image)
        if results.multi_hand_landmarks is not None:
                    for hand_landmarks in results.multi_hand_landmarks:
                        landmark_list = []
                        for landmark in hand_landmarks.landmark:
                            landmark_x = min(int(landmark.x * image.shape[1]), image.shape[1] - 1)
                            landmark_y = min(int(landmark.y * image.shape[0]), image.shape[0] - 1)
                            landmark_list.append([landmark_x, landmark_y])
                        # print("Convert to pixel location: " + str(landmark_list))
                        # Pre-process landmarks to -1 to 1
                        temp_landmark_list = []
                        base_x, base_y = landmark_list[0]
                        for x, y in landmark_list:
                            temp_landmark_list.append((x - base_x, y - base_y))
                        # print("Location base on wrist: " + str(temp_landmark_list))
                        temp_landmark_list = [coord for point in temp_landmark_list for coord in point]
                        max_value = max(abs(coord) for coord in temp_landmark_list)
                        temp_landmark_list = [coord / max_value for coord in temp_landmark_list]
                        # print("Final value: " + str(temp_landmark_list))
                        # Write to CSV
                        with open(csv_path, 'a', newline='') as f:
                            print(f"Write data for image {item}")
                            writer = csv.writer(f)
                            writer.writerow([class_name, *temp_landmark_list])
        else:
             print(f"No hand in image{item}")

print("Done created data........")


