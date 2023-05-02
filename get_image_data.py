import cv2 as cv
import mediapipe as mp
import csv
import os
import numpy as np

def calc_bounding_box(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]
    landmark_array = np.empty((0, 2), int)
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_point = [np.array((landmark_x, landmark_y))]
        landmark_array = np.append(landmark_array, landmark_point, axis=0)
    x, y, w, h = cv.boundingRect(landmark_array)
    return [x, y, x + w, y + h]

def draw_bounding_box(image, bounding_box):
    cv.rectangle(image, (bounding_box[0], bounding_box[1]), (bounding_box[2], bounding_box[3]),(0, 0, 0), 1)
    return image

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv.VideoCapture(0)

folder_type = input("Enter folder type: train/val/test\n")
class_name = input("Enter class name:\n")
data_folder_path = f"data_set/data/{folder_type}"
image_folder_path = f"data_set/image/{folder_type}/{class_name}"


#make data folder if not exist
if os.path.exists(data_folder_path):
    pass
else:
    os.makedirs(data_folder_path)

#make image folder if not exist
if os.path.exists(image_folder_path):
    pass
else:
    os.makedirs(image_folder_path)


#create and clear the csv file
i = open(f"{data_folder_path}/{class_name}.csv", "w")

#for each class, there will be a txt file to count the number of image
count = 0
if os.path.exists(f"{image_folder_path}/{class_name}.txt"):
    with open(f"{image_folder_path}/{class_name}.txt", 'r') as f:
        try:
            count = int(f.read())
        except ValueError:
            count = 0
        print(count)
else:
    f = open(f"{image_folder_path}/{class_name}.txt", 'w')

while True:
    key = cv.waitKey(1)
    if key == 27:  # ESC
        print(f"write to {class_name}.txt: " + str(count))
        with open(f"{image_folder_path}/{class_name}.txt", 'w') as file:
            file.write(str(count))
        break

    ret, image = cap.read()
    image = cv.flip(image, 1)
    copy_image = image.copy()
    results = hands.process(image)

    if results.multi_hand_landmarks is not None:
        # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        # print("IMAGE SIZE: " + str(image.shape[1]) + str(image.shape[0]))
        # print("ORIGINAL: " + str(results.multi_hand_landmarks))
        # print(results.multi_hand_landmarks)

        # Process the hand result and save to csv
        for hand_landmarks in results.multi_hand_landmarks:
            landmark_list = []
            for landmark in hand_landmarks.landmark:
                bounding_box = calc_bounding_box(image, hand_landmarks)   
                image = draw_bounding_box(image, bounding_box) 

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
            #print("Final value: " + str(temp_landmark_list))

            # Save image to folder
            if key == ord("a"):
                cv.imwrite(f"{image_folder_path}/{count}.jpg", copy_image)
                print("Save image " + str(count) + ".jpg" + " to folder " + f"{image_folder_path}")
            # Write to CSV file
                with open(f"{data_folder_path}/{class_name}.csv", 'a', newline='') as f:
                    print(f"Write to {class_name}.csv data from image {count}.jpg\n")
                    writer = csv.writer(f)
                    writer.writerow([count, class_name, *temp_landmark_list])
                count += 1

    cv.imshow('Get image and data', image)
        
cap.release()
cv.destroyAllWindows()

