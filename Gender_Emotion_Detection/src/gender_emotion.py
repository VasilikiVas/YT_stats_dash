import numpy as np
import argparse
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import json

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# command line argument
ap = argparse.ArgumentParser()
ap.add_argument("--mode",help="train/display")
#ap.add_argument('--image')
mode = ap.parse_args().mode
args=ap.parse_args()

def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn=frame.copy()
    frameHeight=frameOpencvDnn.shape[0]
    frameWidth=frameOpencvDnn.shape[1]
    blob=cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections=net.forward()
    faceBoxes=[]
    for i in range(detections.shape[2]):
        confidence=detections[0,0,i,2]
        if confidence>conf_threshold:
            x1=int(detections[0,0,i,3]*frameWidth)
            y1=int(detections[0,0,i,4]*frameHeight)
            x2=int(detections[0,0,i,5]*frameWidth)
            y2=int(detections[0,0,i,6]*frameHeight)
            faceBoxes.append([x1,y1,x2,y2])
            cv2.rectangle(frameOpencvDnn, (x1,y1), (x2,y2), (0,255,0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn,faceBoxes

faceProto="opencv_face_detector.pbtxt"
faceModel="opencv_face_detector_uint8.pb"
genderProto="gender_deploy.prototxt"
genderModel="gender_net.caffemodel"

MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
genderList=['Male','Female']

faceNet=cv2.dnn.readNet(faceModel,faceProto)
genderNet=cv2.dnn.readNet(genderModel,genderProto)

for frame_name in os.listdir("../../data/thumbnails-not-cropped"):
    gender_list = []
    emotion_list = []
    frame_dict = "../../data/thumbnails-not-cropped/"+frame_name
    print(frame_name)
    frame = cv2.imread(frame_dict)
    if frame is None:
        print('Wrong path:', frame_dict)
    else:
        l = []
        resultImg,faceBoxes=highlightFace(faceNet,frame)
        if not faceBoxes:
            print("No face detected")

        # Create the model
        model = Sequential()

        model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
        model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(1024, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(7, activation='softmax'))

        # emotions will be displayed on your face from the webcam feed
        if mode == "display":
            model.load_weights('model.h5')

            # prevents openCL usage and unnecessary logging messages
            cv2.ocl.setUseOpenCL(False)

            # dictionary which assigns each label an emotion (alphabetical order)
            emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        pl = 0
        for (x, y, w, h) in faceBoxes:
            pl += 1
            face=frame[max(0,y-10):
                        min(h+10,frame.shape[0]-1),max(0,x-10)
                        :min(w+10, frame.shape[1]-1)]
            if face.shape[0] != 0 and face.shape[1] !=0 :
                blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
                genderNet.setInput(blob)
                genderPreds=genderNet.forward()
                gender=genderList[genderPreds[0].argmax()]
                print(f'Gender: {gender}')
                #save faces
                #cv2.imwrite("face"+str(pl)+".jpg", face)
                #create the bounding box
                cv2.rectangle(frame, (max(0,x-20), max(0,y-20)), (min(w+10, frame.shape[1]-1), min(h+10,frame.shape[0]-1)), (255, 0, 0), 2)
                roi_gray = gray[max(0,y-10):
                            min(h+10,frame.shape[0]-1),max(0,x-10)
                            :min(w+10, frame.shape[1]-1)]
                cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
                prediction = model.predict(cropped_img)
                maxindex = int(np.argmax(prediction))
                print(emotion_dict[maxindex])
                cv2.putText(frame, f'{gender}', (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, f'{emotion_dict[maxindex]}', (x-20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                x = {"number": pl,
                    "gender": gender,
                    "emotion": emotion_dict[maxindex],
                    "box_dim": [max(0,x-20), max(0,y-20), min(w+10, frame.shape[1]-1), min(h+10,frame.shape[0]-1)]}
                l.append(x)
        y = json.dumps(l)
        with open("../result_json/"+frame_name.split(".")[0]+".json", 'w') as outfile:
            outfile.write(y)
        cv2.imwrite("../result_images/"+frame_name, frame)
