from tkinter import *
import tkinter
from scipy.spatial import distance as dist
from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
from pygame import mixer

mixer.init()
mixer.music.load( "music.wav" )

main = tkinter.Tk()
main.title( "Driver Drowsiness Monitoring" )
main.geometry( "800x600" )

alarm_triggered = False  # Initialize flag for alarm

def compute_average_precision(gt, pred):
    num_frames = len(gt)
    num_objects = len(np.unique(gt))

    aps = []
    for obj_id in range(1, num_objects + 1):
        gt_obj = np.zeros(num_frames, dtype=np.int32)
        pred_obj = np.zeros(num_frames, dtype=np.int32)

        for idx, label in enumerate(gt):
            if label == obj_id:
                gt_obj[idx] = 1

        for idx, score in enumerate(pred):
            if score == obj_id:
                pred_obj[idx] = 1

        aps.append(average_precision_score(gt_obj, pred_obj))

    return aps, np.mean(aps)

def EAR(drivereye):
    point1 = dist.euclidean( drivereye[1], drivereye[5] )
    point2 = dist.euclidean( drivereye[2], drivereye[4] )
    distance = dist.euclidean( drivereye[0], drivereye[3] )
    ear_aspect_ratio = (point1 + point2) / (2.0 * distance)
    return ear_aspect_ratio


def MOR(drivermouth):
    point = dist.euclidean(drivermouth[0], drivermouth[6])
    point1 = dist.euclidean(drivermouth[2], drivermouth[10])
    point2 = dist.euclidean(drivermouth[4], drivermouth[8])
    Ypoint = (point1 + point2) / 2.0
    mouth_aspect_ratio = Ypoint / point
    return mouth_aspect_ratio

def startMonitoring():
    global alarm_triggered  # Use global flag for alarm

    pathlabel.config(text="          Webcam Connected Successfully")
    webcamera = cv2.VideoCapture(0)
    svm_predictor_path = 'shape_predictor_68_face_landmarks.dat'
    EYE_AR_THRESH = 0.25
    EYE_AR_CONSEC_FRAMES = 10
    MOU_AR_THRESH = 0.75

    COUNTER = 0
    yawnStatus = False
    yawns = 0
    svm_detector = dlib.get_frontal_face_detector()
    svm_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

    while True:
        ret, frame = webcamera.read()
        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        prev_yawn_status = yawnStatus
        rects = svm_detector(gray, 0)

        for rect in rects:
            shape = svm_predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            mouth = shape[mStart:mEnd]

            leftEAR = EAR(leftEye)
            rightEAR = EAR(rightEye)
            mouEAR = MOR(mouth)

            ear = (leftEAR + rightEAR) / 2.0
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            mouthHull = cv2.convexHull(mouth)

            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 255), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 255), 1)
            cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)

            if ear < EYE_AR_THRESH:
                COUNTER += 1
                cv2.putText(frame, "Eyes Closed ", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                if COUNTER >= EYE_AR_CONSEC_FRAMES and not alarm_triggered:
                    cv2.putText(frame, "DROWSINESS ALERT!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    mixer.music.play()
                    alarm_triggered = True
            else:
                COUNTER = 0
                cv2.putText(frame, "Eyes Open ", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                alarm_triggered = False

            cv2.putText(frame, "EAR: {:.2f}".format(ear), (480, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            if mouEAR > MOU_AR_THRESH:
                cv2.putText(frame, "Yawning, DROWSINESS ALERT! ", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                yawnStatus = True
                output_text = "Yawn Count: " + str(yawns + 1)
                cv2.putText(frame, output_text, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                if not alarm_triggered:
                    mixer.music.play()
                    alarm_triggered = True
            else:
                yawnStatus = False

            if prev_yawn_status == True and yawnStatus == False:
                yawns += 1

            cv2.putText(frame, "MAR: {:.2f}".format(mouEAR), (480, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "Visual Behaviour & Machine Learning Drowsiness Detection @ Drowsiness", (370, 470),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (153, 51, 102), 1)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    webcamera.release()

font = ('times', 16, 'italic')
title = Label(main, text='Driver Drowsiness Monitoring System using Visual\n               '
                         'Behaviour and Machine Learning', anchor=W, justify=LEFT)
title.config(bg='black', fg='white')
title.config(font=font)
title.config(height=5, width=100)
title.place(x=0, y=0)

font1 = ('times', 14, 'italic')
upload = Button(main, text="Start Behaviour Monitoring Using Webcam", command=startMonitoring)
upload.place(x=150, y=400)
upload.config(font=font1)

pathlabel = Label(main)
pathlabel.config(bg='darkorange1', fg='white')
pathlabel.config(font=font1)
pathlabel.place(x=150, y=500)

main.config(bg='chocolate1')
main.mainloop()

import numpy as np
from sklearn.metrics import average_precision_score

def compute_average_precision(gt, pred):
    num_frames = len(gt)
    num_objects = len(np.unique(gt))

    aps = []
    for obj_id in range(1, num_objects + 1):
        gt_obj = np.zeros(num_frames, dtype=np.int32)
        pred_obj = np.zeros(num_frames, dtype=np.int32)

        for idx, label in enumerate(gt):
            if label == obj_id:
                gt_obj[idx] = 1

        for idx, score in enumerate(pred):
            if score == obj_id:
                pred_obj[idx] = 1

        aps.append(average_precision_score(gt_obj, pred_obj))

    return aps, np.mean(aps)

