import cv2
from ultralytics import YOLO
import time
import os
import numpy as np

cwd = os.getcwd()
print(cwd)


def binning_2x2(image):
    return cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2), interpolation=cv2.INTER_NEAREST)


def enhance_image_clahe(frame):
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

def adaptive_brightness_contrast(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mean_brightness = np.mean(gray)

    if mean_brightness < 50: 
        alpha = 0.7 
        beta = 30  

    elif mean_brightness > 200: 
        alpha = 1.2  
        beta = -30

    else:  
        alpha = 1.0  
        beta = -30  

    enhanced_frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    return enhanced_frame


def droneDetection():
    try:
        model = YOLO("src/models/best.pt")
        model.fuse()  
        print("Model loaded and fused")
        model = model.cpu()

    except Exception as e:
        print(e)
    try:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Largeur de la frame
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)  # Hauteur de la frame
    except Exception as e:
        print(e)
        exit()

    frame_skip = 1  
    frame_counter = 0  

    while cap.isOpened():
        success, frame = cap.read()

        if success:
            frame_counter += 1

            if frame_counter % frame_skip == 0:
                frame = adaptive_brightness_contrast(frame)  # Appliquer l'adaptation de la luminosité et du contraste
                enhanced_frame = enhance_image_clahe(frame)   # Appliquer CLAHE après l'ajustement
                results = model.track(enhanced_frame, persist=True , conf =  0.15 , tracker = "bytetrack.yaml")
                annotated_frame = results[0].plot()
                cv2.imshow("Tracking", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
