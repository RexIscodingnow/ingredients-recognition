import os
# import cv2 as cv
import numpy as np
from ultralytics import YOLO
from ultralytics.engine.results import Results


class Detection:
    def __init__(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"FileNotFoundError: {path} does not exist")

        self.model = YOLO(path)


    def predict(self, img: np.ndarray, classes=[], conf=0.5) -> list[Results]:
        if classes:
            results = self.model.predict(img, classes=classes, conf=conf)
        else:
            results = self.model.predict(img, conf=conf)

        return results


    # def predict_and_detect(self, img, classes=[], conf=0.5, rectangle_thickness=2, text_thickness=1):
    #     results = self.predict(img, classes=classes, conf=conf)

    #     for result in results:
    #         for box in result.boxes:
    #             cv.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
    #                           (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (255, 0, 0), rectangle_thickness)
    #             cv.putText(img, f"{result.names[int(box.cls[0])]}",
    #                         (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
    #                         cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), text_thickness)
    #     return img, results


    # def detect(self, image, conf=0.5):
    #     return self.predict_and_detect(image, conf=conf)


def get_abspath_files(path: str):
    path = os.path.abspath(path)
    return [os.path.abspath(entry.path) for entry in os.scandir(path) if entry.is_file()]


def list_categories(result_ls: list[Results]):
    label_ls = []
    score_ls = []

    for results in result_ls:
        names = results.names
        scores = results.boxes.conf.cpu().numpy()
        classes = results.boxes.cls.cpu().numpy()

        for score, cls in zip(scores, classes):
            class_label = names[cls]
            label = f"{class_label}"
            label_ls.append(label)
            score_ls.append(float(score))

    return label_ls, score_ls


if __name__ == "__main__":
    detection = Detection(r"runs\detect\train8\weights\last.pt")

    images = get_abspath_files(r"dataset\train\Bean")[:11]
    # print(images)
    result_ls = detection.predict(images)
    lbl_ls, score_ls = list_categories(result_ls)
    print(lbl_ls)
    print(score_ls)
