
import cv2
import numpy as np
import time
import os

# def enhance_image_clahe(frame):
#     lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
#     l, a, b = cv2.split(lab)
#     clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
#     cl = clahe.apply(l)
#     limg = cv2.merge((cl, a, b))
#     return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

# def adaptive_brightness_contrast(frame):
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     mean_brightness = np.mean(gray)

#     if mean_brightness < 50:
#         alpha = 0.7
#         beta = 30
#     elif mean_brightness > 200:
#         alpha = 1.2
#         beta = -30
#     else:
#         alpha = 1.0
#         beta = -30

#     enhanced_frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
#     return enhanced_frame

# def preprocess_image(image, input_size):
#     blob = cv2.dnn.blobFromImage(image, 1/255.0, input_size, swapRB=True, crop=False)
#     return blob

# def postprocess_detections(detections, original_image_shape, input_size, conf_threshold=0.15):
#     boxes = []
#     confidences = []
#     class_ids = []

#     image_height, image_width = original_image_shape
#     x_factor = image_width / input_size[0]
#     y_factor = image_height / input_size[1]

#     for detection in detections:
#         scores = detection[5:]
#         class_id = np.argmax(scores)
#         confidence = scores[class_id]

#         if confidence > conf_threshold:
#             box = detection[0:4] * np.array([x_factor, y_factor, x_factor, y_factor])
#             (center_x, center_y, width, height) = box.astype("int")

#             x = int(center_x - (width / 2))
#             y = int(center_y - (height / 2))

#             boxes.append([x, y, int(width), int(height)])
#             confidences.append(float(confidence))
#             class_ids.append(class_id)

#     return boxes, confidences, class_ids

# def draw_detections(image, boxes, confidences, class_ids, class_names):
#     indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.15, 0.4)

#     for i in indices:
#         i = i[0]
#         box = boxes[i]
#         x, y, w, h = box
#         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         text = f"{class_names[class_ids[i]]}: {confidences[i]:.2f}"
#         cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# def droneDetection():
#     try:
#         # Charger le modèle ONNX
#         net = cv2.dnn.readNetFromONNX("chemin/vers/votre_modele.onnx")
#         print("Modèle chargé avec succès")
#     except Exception as e:
#         print(f"Erreur lors du chargement du modèle : {e}")
#         return

#     try:
#         cap = cv2.VideoCapture(0)
#         cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#         cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
#     except Exception as e:
#         print(f"Erreur lors de l'accès à la caméra : {e}")
#         return

#     frame_skip = 1
#     frame_counter = 0
#     input_size = (640, 640)
#     class_names = ["classe1", "classe2", "classe3"]  # Remplacez par vos noms de classes

#     while cap.isOpened():
#         success, frame = cap.read()

#         if success:
#             frame_counter += 1

#             if frame_counter % frame_skip == 0:
#                 frame = adaptive_brightness_contrast(frame)
#                 enhanced_frame = enhance_image_clahe(frame)
#                 blob = preprocess_image(enhanced_frame, input_size)
#                 net.setInput(blob)
#                 detections = net.forward()

#                 boxes, confidences, class_ids = postprocess_detections(detections[0], frame.shape[:2], input_size)
#                 draw_detections(frame, boxes, confidences, class_ids, class_names)

#                 cv2.imshow("Detection", frame)

#             if cv2.waitKey(1) & 0xFF == ord("q"):
#                 break
#         else:
#             break

#     cap.release()
#     cv2.destroyAllWindows()


#Simpler version test

def load_yolo_model(onnx_path):
    try:
        net = cv2.dnn.readNetFromONNX(onnx_path)
        print("Model loaded successfully.")
        return net
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def detect_and_draw(net, input_size=(640, 640), conf_threshold=0.5):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, input_size[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, input_size[1])

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        blob = cv2.dnn.blobFromImage(frame, 1/255.0, input_size, swapRB=True, crop=False)
        net.setInput(blob)
        detections = net.forward()

        for detection in detections[0, 0]:
            confidence = detection[2]
            if confidence > conf_threshold:
                x1, y1, x2, y2 = (detection[3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])).astype(int)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"Conf: {confidence:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("YOLO Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

onnx_path = "../models/12.onnx"
yolo_net = load_yolo_model(onnx_path)
if yolo_net:
    detect_and_draw(yolo_net)



import cv2
import numpy as np
import onnxruntime as ort

session = ort.InferenceSession("modele.onnx", providers=["CPUExecutionProvider"])

input_size = (640, 640)
conf_threshold = 0.5  

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, scalefactor=1/255.0, size=input_size, swapRB=True, crop=False)

    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: blob})

    detections = outputs[0][0]

    for det in detections:
        confidence = det[4]
        if confidence > conf_threshold:
            x, y, w, h = det[:4]
            x, y, w, h = int(x * width), int(y * height), int(w * width), int(h * height)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("YOLO ONNX - Webcam", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
