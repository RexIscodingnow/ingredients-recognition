import os
from ultralytics import YOLO


model = YOLO("yolov8n.pt")
# model = YOLO("yolov8n.pt").load(r"DetectVegetables_env\runs\detect\train14\weights\last.pt")


if __name__ == "__main__":
    model.train(
        data=os.path.abspath("./dataset/Bean_Cabbage.v1i.yolov8/data.yaml"), 
        epochs=20, 
        device='cuda'
    )
    