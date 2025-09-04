# this is the best known code 


import cv2
import numpy as np
import pyrealsense2 as rs

# Load YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Initialize the RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
pipeline.start(config)

# Align depth to color
align = rs.align(rs.stream.color)

while True:
    # Wait for a new frame
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)
    color_frame = aligned_frames.get_color_frame()
    depth_frame = aligned_frames.get_depth_frame()

    if not color_frame or not depth_frame:
        continue

    
    depth_image = np.asanyarray(depth_frame.get_data())

    
    color_image = np.asanyarray(color_frame.get_data())

    # Preprocess color frame for YOLO
    blob = cv2.dnn.blobFromImage(color_image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Object detection
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * 640)
                center_y = int(detection[1] * 480)
                w = int(detection[2] * 640)
                h = int(detection[3] * 480)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = (0, 255, 0)
            cv2.rectangle(color_image, (x, y), (x + w, y + h), color, 2)
            cv2.putText(color_image, label + " " + str(round(confidence, 2)), (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)

            # Calculate the distance to the object using depth information
            depth = depth_frame.get_distance(x + w // 2, y + h // 2)
            print("Distance to", label, ":", depth, "meters")

    # Display the frames
    cv2.imshow('Color frame', color_image)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the RealSense pipeline
pipeline.stop()
cv2.destroyAllWindows()
