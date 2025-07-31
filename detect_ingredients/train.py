import os
from ultralytics import YOLO


model = YOLO("yolov8n.pt")
# model = YOLO('yolov8n-cls.pt')

# Load the information of dataset
data = os.path.abspath("ingredients-3/data.yaml")

if __name__ == "__main__":
    # For train and validation dataset
    train_metrics = model.train(
        data=data, 
        epochs=5,
        batch=100,
        device='cuda'
    )
    print("-------------------------------------")

    model.eval()
    test_metrics = model.val(data=data, split="test")   # Only use the test dataset

    print("\n--------------- train ---------------\n")
    print(train_metrics)
    print("\n--------------- test  ---------------\n")
    print(test_metrics)
