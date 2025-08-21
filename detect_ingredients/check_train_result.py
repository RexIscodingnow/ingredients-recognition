import os
import cv2
import numpy as np
from ultralytics import YOLO
from ultralytics.engine.results import Results


def load_abspath_files(path: str):
    path = os.path.abspath(path)
    return [os.path.abspath(entry.path) for entry in os.scandir(path) if entry.is_file()]


def plot_classification_result(result: Results):
    img = result.orig_img.copy()
    names = result.names          # 類別名稱對應字典

    if result.probs is not None:
        top1_idx = result.probs.top1                    # 預測機率最高的類別索引
        top1_conf = result.probs.top1conf.item()        # 對應的信心分數
        label = f"{names[top1_idx]}: {top1_conf:.2f}"

        # 設定文字位置和樣式
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        thickness = 2
        text_size, _ = cv2.getTextSize(label, font, font_scale, thickness)
        text_w, text_h = text_size
        margin = 10

        # 繪製背景矩形
        cv2.rectangle(img, (margin - 5, margin - 5), (margin + text_w + 5, margin + text_h + 5), (0, 0, 255), -1)
        # 繪製文字
        cv2.putText(img, label, (margin, margin + text_h), font, font_scale, (255, 255, 255), thickness)
    else:
        print("No classification probabilities found in result.")

    return img


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
        img = cv2.rectangle(img, (bbox[0], bbox[1]),
                            (bbox[2], bbox[3]),
                            color=(0, 0, 255),
                            thickness=1)
        label_size = cv2.getTextSize(label,                         # labelsize in pixels 
                                     fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                                     fontScale=1, thickness=1)
        # label width and height
        lbl_w, lbl_h = label_size[0]
        # add margins on both sides
        lbl_w += 2 * lbl_margin
        lbl_h += 2 * lbl_margin
        img = cv2.rectangle(img, (bbox[0], bbox[1]),                # plot label background
                             (bbox[0]+lbl_w, bbox[1]-lbl_h),
                             color=(0, 0, 255), 
                             thickness=-1)                          # thickness=-1 means filled rectangle
        
        # write label to the image
        cv2.putText(img, label, (bbox[0]+ lbl_margin, bbox[1]-lbl_margin), 
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.0, color=(255, 255, 255 ),
                    thickness=1)
    return img


if __name__ == "__main__":
    # model = YOLO(r"yolov8n-oiv7.pt")
    # model = YOLO(r"runs\classify\train2\weights\best.pt")
    model = YOLO(r"runs\detect\train8\weights\best.pt")
    model.eval()

    # test_images = [
    #     "photo.jpg", "photo (1).jpg", "yqn44-029.jpg", 
    #     "211210-11613-0-wRvMe.jpg", "35e98791e79baee9b1b8.jpg", "AM_207_20240801095858_938182.jpg"
    # ]
    path = r"dataset\test"

    test_images = [
        file for d in os.scandir(path) if d.is_dir() for file in load_abspath_files(d.path)[:1]
    ]

    # print(test_images)
    print(f"total: {len(test_images)}")

    # conf (confidence) 
    # results = model.predict(test_images, conf=0.45)
    results = model.predict(test_images)

    for (i, result) in enumerate(results):
        img = plot_bboxes(result)
        cv2.imshow(f"{i}", img)

    if ord('q') == cv2.waitKey(0):
        cv2.destroyAllWindows()
