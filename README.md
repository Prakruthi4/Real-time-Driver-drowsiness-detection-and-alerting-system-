# Real-time-Driver-drowsiness-detection-and-alerting-system-

The proposed project aims to implement a Driver-Drowsiness-Detection system using a webcam, OpenCV, and the SVM (Support Vector Machine) algorithm to extract facial features from the real time video and then check whether driver is blinking his eyes for consecutive 20 frames or yawning mouth then application will alert driver with Drowsiness messages. We are using SVM pre-trained drowsiness model and then using Euclidean distance function we are continuously checking or predicting EYES and MOUTH distance closer to drowsiness, if distance is closer to drowsiness then application will alert driver. The system monitors the visual behavior of a driver, detects signs of drowsiness such as blinking and yawning, and alerts the driver accordingly. Here's a brief overview of the different modules involved:

Video Recording:Utilizes the OpenCV library's VideoCapture function to connect the application to the inbuilt webcam.Enables the capturing of video frames for further processing.

Frame Extraction: This module is used to capture webcam frames, extract individual images frame by frame, and then transform each image into a two-dimensional array.

Face Detection & Facial Landmark Detection: We will identify faces in photos by applying the SVM algorithm, and we will then extract the expressions on the faces from the frames.


## SVM State Classification
A powerful predictive modelling technique called Support Vector Machines (SVMs) is widely used in driver tiredness detection systems. They are excellent at classifying data because they can create a hyperplane that effectively divides data points into multiple classes. SVMs can efficiently identify whether a motorist is alert or sleepy in the context of driver sleepiness detection by using extracted face 
data such eye aspect ratio (EAR), yawn angle, and head altitude.SVM allows for the processing of the source information to a higher-dimensional space using various kernel functions. Common kernel functions include polynomials, linear ones, and radial base function (RBF) functions. Which kernel to employ depends on the problem and the kind of data. It has hyperparameters for the kernel parameters and the regularisation parameter. To maximise the model's performance, these must be adjusted. Whether the driver is aware or sleepy is output by the model.To establish when the driver's status should cause an alert, set a threshold on the SVM's decision function. The sensitivity and specificity needs of the system can be taken into consideration while adjusting this level.
