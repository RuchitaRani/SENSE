import numpy as np
import argparse
import time
import cv2
import os
import pyttsx3

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--confidence", type=float, default=0.5,
    help="minimum probability to filter weak detections, IoU threshold")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
    help="threshold when applying non-maxima suppression")
args = vars(ap.parse_args())

labelsPath = 'yolo-coco\\coco.names'
LABELS = open(labelsPath).read().strip().split("\n")

COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
    dtype="uint8")


weightsPath = 'yolo-coco\\yolov3.weights'
configPath = 'yolo-coco\\yolov3.cfg'


net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# Initialize the video stream
print("[INFO] starting video stream...")
vs = cv2.VideoCapture(0)


engine = pyttsx3.init()

start_time = time.time()


while True:

    ret, frame = vs.read()
    if not ret:
        break

    
    (H, W) = frame.shape[:2]

    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                  swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    boxes = []
    confidences = []
    classIDs = []

    for output in layerOutputs:
        for detection in output:

            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > args["confidence"]:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
                            args["threshold"])

    
    if time.time() - start_time >= 3:
        if len(idxs) > 0:
            objects_detected = []
            for i in idxs.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                object_label = LABELS[classIDs[i]]
                cv2.putText(frame, object_label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, color, 2)

                objects_detected.append(object_label)

            objects_text = ', '.join(objects_detected)

            engine.say("Objects detected: " + objects_text)
            engine.runAndWait()

        start_time = time.time()  # Reset the timer

    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

vs.release()
cv2.destroyAllWindows()
