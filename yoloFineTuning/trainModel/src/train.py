from ultralytics import YOLO

def train(modelPath, dataPath, epochs=100, batchSize=16, imgSize=320):
    model = YOLO(modelPath) 
    
    model.train(
        data=dataPath, 
        epochs=epochs,
        batch=batchSize,
        imgsz=imgSize,
        save=True,
        project="runs",  
        name="Vsmodel"  
    )

    print("Training complete!")