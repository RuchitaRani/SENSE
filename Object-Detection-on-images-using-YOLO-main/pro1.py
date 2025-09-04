import numpy as np
import argparse
import time
import cv2
import os

# Object-specific variables for distance calculation
focal_length = 450  # Focal length of the camera in pixels
object_width = 4     # Width of the object in inches

# Parse command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections, IoU threshold")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
	help="threshold when applying non-maxima suppression")
args = vars(ap.parse_args())

# Load the YOLO model
labelsPath = 'yolo-coco/coco.names'
LABELS = open(labelsPath).read().strip().split("\n")

weightsPath = 'yolo-coco/yolov3.weights'
configPath = 'yolo-coco/yolov3.cfg'

net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# Start the video stream
print("[INFO] starting video stream...")
vs = cv2.VideoCapture(0)  

# Loop over the frames from the video stream
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

                # Calculate distance from the camera
                object_pixels_width = width
                distance = (object_width * focal_length) / object_pixels_width

                # Display the distance on the frame
                cv2.putText(frame, f'Distance: {distance:.2f} inches', (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"], args["threshold"])

    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            color = [int(c) for c in np.random.randint(0, 255, size=(3,))]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

vs.release()
cv2.destroyAllWindows()