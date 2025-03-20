import cv2
from ultralytics import YOLO
import os

def drone_detection():
    model = YOLO("src/models/VsModel_32_640.pt")
    model.fuse()
    model  = model.cpu()

    def binning_2x2(image):
        return cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2), interpolation=cv2.INTER_NEAREST)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame_skip = 3
    frame_counter = 0

    while cap.isOpened():
        success, frame = cap.read()

        if success:
            frame_counter += 1

            if frame_counter % frame_skip == 0:
                frame_binned = binning_2x2(frame)
                results = model.track(frame_binned, persist=True)
                annotated_frame = results[0].plot()
                cv2.imshow("Drone Tracking", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

drone_detection()
