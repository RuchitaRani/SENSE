# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SENSE is a computer vision project for assistive technology that combines object detection and depth sensing for visually impaired users. The system uses YOLO (You Only Look Once) for real-time object detection and Intel RealSense cameras for depth perception, with text-to-speech capabilities for audio feedback.

## Architecture

The project has two main components:

### 1. Object Detection Module (`Object-Detection-on-images-using-YOLO-main/`)
- **YOLO Implementation**: Uses YOLOv3 for object detection on images and video streams
- **Core Files**:
  - `yolo.py`: Static image object detection with command-line interface
  - `x.py`: Real-time video detection with webcam integration and text-to-speech
  - `sos.py`: Emergency alert system with GPS location sharing via email
- **Model Files**: Pre-trained YOLOv3 weights (248MB), configuration, and COCO class names in `yolo-coco/`

### 2. Distance Measurement Module (`detection and distance/`)
- **RealSense Integration**: Uses Intel RealSense cameras for depth sensing
- **Mask R-CNN**: Advanced object segmentation with instance detection
- **Core Files**:
  - `realsense_camera.py`: RealSense camera interface with depth filtering
  - `mask_rcnn.py`: Mask R-CNN implementation for object segmentation and distance calculation
  - `measure_object_distance.py`: Main application combining camera input with object detection

## Development Commands

### Object Detection (YOLO)
```bash
# Static image detection
cd "Object-Detection-on-images-using-YOLO-main"
python yolo.py --image images/your_image.jpg

# Real-time detection with webcam and audio feedback
python x.py --confidence 0.5 --threshold 0.3

# Emergency SOS system
python sos.py
```

### Distance Measurement (RealSense + Mask R-CNN)
```bash
# Real-time object detection with distance measurement
cd "detection and distance"
python measure_object_distance.py
```

## Dependencies

### Python Libraries
- **Computer Vision**: `opencv-python`, `numpy`
- **Deep Learning**: Pre-trained models (YOLO, Mask R-CNN)
- **Hardware**: `pyrealsense2` (Intel RealSense SDK)
- **Audio**: `pyttsx3` (text-to-speech)
- **Utilities**: `smtplib`, `geocoder`

### Hardware Requirements
- Intel RealSense depth camera (for distance measurement module)
- Standard webcam (for basic YOLO detection)

## Key Features

1. **Multi-modal Detection**: Both 2D object detection and 3D depth sensing
2. **Audio Feedback**: Text-to-speech announcements of detected objects
3. **Emergency System**: GPS-based SOS email alerts
4. **Real-time Processing**: Live camera feed processing with configurable thresholds

## File Structure Notes

- YOLO weights file (`yolov3.weights`) is 248MB and contains the pre-trained model
- Mask R-CNN models are stored in `dnn/` subdirectory
- Images for testing are stored in `images/` subdirectory
- The project uses Windows-style path separators (`\\`) in file paths

## Usage Patterns

- Press 'q' to quit video windows in real-time detection modes
- Press ESC (key code 27) to exit the distance measurement application
- Confidence and threshold parameters are adjustable for detection sensitivity