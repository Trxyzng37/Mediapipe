
# import some libraries
import csv
import copy
import math

import cv2 as cv
import tensorflow as tf
import numpy as np
import mediapipe as mp
import time

def classifier_gesture(queue):
    hand_sign_id = 0

    cap = cv.VideoCapture(0)
    prev_time = 0

    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(
        static_image_mode = False,
        max_num_hands = 1,
        min_detection_confidence = 0.5,
        min_tracking_confidence = 0.5,
    )

    # Read labels ############################
    with open('label.csv',
              encoding='utf-8-sig') as f:
        keypoint_classifier_labels = csv.reader(f)
        keypoint_classifier_labels = [
            row[0] for row in keypoint_classifier_labels
        ]

    prev_occurence = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0
    }

    while True:
        # if user press ESC key, exit
        key = cv.waitKey(1)
        if key == 27:  # ESC
            break
        # read the camera and get frame
        ret, image = cap.read()
        if not ret:
            break
        # flip the frame for easier to see
        image = cv.flip(image, 1) 

        # image.flags.writeable = False
        # get the result from mediapipe
        results = hands.process(image)
        # image.flags.writeable = True
        #calculate fps
        curr_time = cv.getTickCount()
        time_taken = (curr_time - prev_time) / cv.getTickFrequency()
        fps = math.ceil(1/time_taken)
        prev_time = curr_time

        # process the result from mediapipe and find which hand gesture is it
        # if result from mediapipe is not None
        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                
                # calculate bounding box for detected hand
                bounding_box = calc_bounding_box(image, hand_landmarks)
                #convert keypoint value in range (0,1) from mediapipe result to key point value base on image size
                landmark_list = calc_landmark_list(image, hand_landmarks)
                # normalized key point value base on image size from -1 to 1
                normalized_processed_landmark_list = calc_normalized_processed_landmark_list(landmark_list)
                # Hand sign classification
                hand_sign_id = key_point_classifier(normalized_processed_landmark_list)

                # Drawing part
                image = draw_bounding_box(image, bounding_box)
                image = draw_landmarks(image, landmark_list)
                image = draw_info_text(
                    image,
                    bounding_box,
                    handedness,
                    keypoint_classifier_labels,
                    hand_sign_id
                )

                if queue is None:
                    pass
                else:
                    if prev_occurence[hand_sign_id] == 0:
                        prev_occurence[hand_sign_id] = int(time.time())
                        queue.put(hand_sign_id)
                        print("put to queue: "+str(hand_sign_id))
                    else:
                        if time.time() - prev_occurence[hand_sign_id] >= 3:
                            queue.put(hand_sign_id)
                            print("put to queue: "+str(hand_sign_id))
                            prev_occurence[hand_sign_id] = time.time()
                        else:
                            pass


        # draw fps on frame
        image = draw_fps(image, fps)

        # show frame with data
        cv.imshow('Hand Gesture Recognition', image)
        
    # return hand_sign_id

    cap.release()
    cv.destroyAllWindows()



# calculate the bounding box for hand on image
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


# process the result key point value from medapipe in range (0,1) to value base on image size
def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]
    landmark_point = []
    for landmark in landmarks.landmark:
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_point.append([landmark_x, landmark_y])
    # return a list with each element is a list contain x,y value    
    return landmark_point

# process the key point value base on image size, and normalize it into value in range (-1,1) 
def calc_normalized_processed_landmark_list(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)
    # Convert to relative coordinates base on the wrist position
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]
        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y
    # Convert a list of list into a single list
    # temp_landmark_list = list(
    #     itertools.chain.from_iterable(temp_landmark_list))
    temp_landmark_list = sum(temp_landmark_list, [])
    #print(temp_landmark_list)
    #for each value in the list, find the absolute value of it, then find the maximum value in the list
    max_value = max(list(map(abs, temp_landmark_list)))
    def normalize_(n):
        return n / max_value
    # for each value in list, divide it with the maximum value in the list
    temp_landmark_list = list(map(normalize_, temp_landmark_list))
    return temp_landmark_list

# from the result from mediapipe, run it through the classifier to detect which hand gesture is it
def key_point_classifier(landmark_list, model_path='keypoint_classifier.tflite', num_threads=1):
    interpreter = tf.lite.Interpreter(model_path = model_path, num_threads=num_threads)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    input_details_tensor_index = input_details[0]['index']
    interpreter.set_tensor(input_details_tensor_index, np.array([landmark_list], dtype=np.float32))
    interpreter.invoke()
    output_details_tensor_index = output_details[0]['index']
    result = interpreter.get_tensor(output_details_tensor_index)
    # find the maximum probability class
    max_result_probability = np.max(np.squeeze(result))
    #print(max_result_probability)
    if max_result_probability > 0.9:
        result_index = np.argmax(np.squeeze(result))
    # if all probability for classes is less than 0.9, output None
    else:
        result_index = None
    return result_index

# draw the landmark
def draw_landmarks(image, landmark_point):
    if len(landmark_point) > 0:
        # Thumb

        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                (255, 255, 255), 1)

        # Index finger

        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                (255, 255, 255), 1)

        # Middle finger

        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                (255, 255, 255), 1)

        # Ring finger

        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                (255, 255, 255), 1)

        # Little finger

        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                (255, 255, 255), 1)

        # Palm

        cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                (255, 255, 255), 1)

        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                (255, 255, 255), 1)

    # Key Points
    for index, landmark in enumerate(landmark_point):
        if index == 0:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 1:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 2:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 3:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 4:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 5:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 6:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 7:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 8:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 9:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 10:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 11:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 12:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 13:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 14:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 15:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 16:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 17:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 18:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 19:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
        if index == 20:  
            cv.circle(image, (landmark[0], landmark[1]), 3, (0, 0, 255),
                      -1)
    return image

# draw the bounding box
def draw_bounding_box(image, bounding_box):
    cv.rectangle(image, (bounding_box[0], bounding_box[1]), (bounding_box[2], bounding_box[3]),(0, 0, 0), 1)
    return image

# draw hand gesture result
def draw_info_text(image, bounding_box, handedness, keypoint_classifier_labels, hand_sign_id):
    cv.rectangle(image, (bounding_box[0], bounding_box[1]), (bounding_box[2], bounding_box[1] - 22), (0, 0, 0), -1)
    info_text = handedness.classification[0].label[0:]
    if hand_sign_id == None:
        info_text = info_text + ':' + "No result"
    else:
        info_text = info_text + ':' + keypoint_classifier_labels[hand_sign_id] + str(hand_sign_id)
    cv.putText(image, info_text, (bounding_box[0] + 5, bounding_box[1] - 4), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)
    return image

# draw fps
def draw_fps(image, fps):
    cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv.LINE_AA)
    return image


if __name__ == '__main__':
    classifier_gesture()
