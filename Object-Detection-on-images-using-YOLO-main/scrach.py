import cv2
import numpy as np
import pyrealsense2 as rs

# Initialize the RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
pipeline.start(config)

# Load Haar Cascade Classifier for object detection
object_cascade = cv2.CascadeClassifier('path/to/haar_cascade.xml')  # Replace with the actual path

while True:
    # Wait for a new frame
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()

    if not color_frame or not depth_frame:
        continue

    # Convert RealSense depth frame to OpenCV format
    depth_image = np.asanyarray(depth_frame.get_data())

    # Convert color frame to grayscale for object detection
    gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

    # Object detection
    objects = object_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in objects:
        # Draw rectangle around the detected object
        cv2.rectangle(color_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Calculate the distance to the object using depth information
        depth = depth_frame.get_distance(x + w // 2, y + h // 2)
        print("Distance to object:", depth, "meters")

    # Display the frames
    cv2.imshow('Color frame', color_image)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the RealSense pipeline
pipeline.stop()
cv2.destroyAllWindows()
