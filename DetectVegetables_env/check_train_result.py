import os
import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO


def load_abspath_files(path: str):
    path = os.path.abspath(path)
    return [os.path.abspath(entry.path) for entry in os.scandir(path) if entry.is_file()]


model = YOLO(r"runs\detect\train14\weights\best.pt")


if __name__ == "__main__":
    df_train_result = pd.read_csv(r"runs\detect\train14\results.csv")
    df_train_result.info()
    
    test_images = ["photo.jpg", "photo (1).jpg", "yqn44-029.jpg", "211210-11613-0-wRvMe.jpg", "35e98791e79baee9b1b8.jpg", "AM_207_20240801095858_938182.jpg"]
    
    # conf (confidence) 
    results = model.predict(test_images, conf=0.6)
    
    i = 1
    for result in results:
        img = result.plot()
        cv2.imshow(f"result {i}", img)
        
        i += 1

    cv2.waitKey(0)
