
from renamingData import verifyImageLabels 
from src.train import train
import os

if __name__ =="__main__":

    print(os.getcwd())    
    verifyImageLabels(
        imageDir = "datasets/images/train",
        labelDir ="datasets/labels/train"
    )
    verifyImageLabels(
        imageDir = "datasets/images/val",
        labelDir = "datasets/labels/val"
    )
    train(
        modelPath = "models/yolov8n.pt",
        dataPath = "src/data.yaml")
    

    pass