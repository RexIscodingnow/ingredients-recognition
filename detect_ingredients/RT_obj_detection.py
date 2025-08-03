"""
Open a camera for Real-Time objection detection with YOLO.


"""

import cv2 as cv
import numpy as np
from ultralytics import YOLO
from ultralytics.engine.results import Results


def list_camera_ports(n=6):
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    
    Parameter
        n: Number of ports to scan
    
    Reference: https://stackoverflow.com/questions/57577445/list-available-cameras-opencv-python
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []

    while len(non_working_ports) < n: # if there are more than 5 non working ports stop the testing. 
        camera = cv.VideoCapture(dev_port)
        
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            print(f"Port {dev_port} is not working.")

        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)

            if is_reading:
                print(f"Port {dev_port} is working and reads images ({h} x {w})")
                working_ports.append(dev_port)
            else:
                print(f"Port {dev_port} for camera ({h} x {w}) is present but does not reads.")
                available_ports.append(dev_port)

        dev_port += 1

    return available_ports, working_ports, non_working_ports


def plot_bboxes(results: Results):
    lbl_margin = 3                                                  # label margin
    img = results.orig_img                                          # original image
    names = results.names                                           # class names dict
    scores = results.boxes.conf.cpu().numpy()                       # probabilities
    classes = results.boxes.cls.cpu().numpy()                       # predicted classes
    boxes = results.boxes.xyxy.cpu().numpy().astype(np.int32)       # bboxes
    for score, cls, bbox in zip(scores, classes, boxes):            # loop over all bboxes
        class_label = names[cls]                                    # class name
        label = f"{class_label} : {score:0.2f}"                     # bbox label
        img = cv.rectangle(img, (bbox[0], bbox[1]),
                            (bbox[2], bbox[3]),
                            color=(0, 0, 255),
                            thickness=1)
        label_size = cv.getTextSize(label,                         # labelsize in pixels 
                                     fontFace=cv.FONT_HERSHEY_SIMPLEX, 
                                     fontScale=1, thickness=1)
        # label width and height
        lbl_w, lbl_h = label_size[0]
        # add margins on both sides
        lbl_w += 2 * lbl_margin
        lbl_h += 2 * lbl_margin
        img = cv.rectangle(img, (bbox[0], bbox[1]),                # plot label background
                             (bbox[0]+lbl_w, bbox[1]-lbl_h),
                             color=(0, 0, 255), 
                             thickness=-1)                          # thickness=-1 means filled rectangle
        
        # write label to the image
        cv.putText(img, label, (bbox[0]+ lbl_margin, bbox[1]-lbl_margin), 
                    fontFace=cv.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.0, color=(255, 255, 255 ),
                    thickness=1)
    return img


if __name__ == "__main__":
    cap = cv.VideoCapture(0)
    model = YOLO(r"runs\detect\train8\weights\best.pt")
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    cv.namedWindow("live", cv.WINDOW_AUTOSIZE)  # 命名一個視窗，可不寫

    while True:
        # 擷取影像
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        results = model.track(frame, stream=True)
        
        for result in results:
            plot_bboxes(result)

        cv.imshow('live', frame)

        # 按下 q 鍵離開迴圈
        if cv.waitKey(1) == ord('q'):
            break

    # 釋放該攝影機裝置
    cap.release()
    cv.destroyAllWindows()

