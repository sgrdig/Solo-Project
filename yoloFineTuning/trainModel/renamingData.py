import os
import shutil
import random
import tqdm
import xml.etree.ElementTree as ET


"""
This File is used to rename images and labels for YOLOv8 fine-tuning.
Rename images and labels to a common format as following.
Do it for all images and labels in the trainModel/rawData folder.

"""


# def renameAndAdaptToYolo(imageDir, outputImageDir, outputLabelDir, classId, prefix, trainRatio=0.8):
#     trainImageDir = os.path.join(outputImageDir, "train")
#     valImageDir = os.path.join(outputImageDir, "val")
#     trainLabelDir = os.path.join(outputLabelDir, "train")
#     valLabelDir = os.path.join(outputLabelDir, "val")

#     for directory in [trainImageDir, valImageDir, trainLabelDir, valLabelDir]:
#         os.makedirs(directory, exist_ok=True)

#     imageFiles = [f for f in os.listdir(imageDir) if f.endswith(".jpg") or f.endswith(".png")]
#     random.shuffle(imageFiles)

#     splitIndex = int(len(imageFiles) * trainRatio)
#     trainFiles, valFiles = imageFiles[:splitIndex], imageFiles[splitIndex:]

#     fileCounter = 1
#     for dataset, fileList, imgDir, lblDir in [("train", trainFiles, trainImageDir, trainLabelDir), 
#                                                ("val", valFiles, valImageDir, valLabelDir)]:
#         for fileName in tqdm.tqdm(fileList, desc=f"Processing {prefix} -> {dataset}"):
#             baseName = os.path.splitext(fileName)[0]
#             oldImagePath = os.path.join(imageDir, fileName)
#             oldLabelPath = os.path.join(imageDir, baseName + ".txt")

#             newBaseName = f"{prefix}_{fileCounter:04d}"
#             newImagePath = os.path.join(imgDir, newBaseName + ".jpg")
#             newLabelPath = os.path.join(lblDir, newBaseName + ".txt")

#             shutil.copy(oldImagePath, newImagePath)

#             if os.path.exists(oldLabelPath):
#                 with open(oldLabelPath, "r") as file:
#                     lines = file.readlines()

#                 newLines = [f"{classId} " + " ".join(line.strip().split()[1:]) for line in lines]

#                 with open(newLabelPath, "w") as file:
#                     file.write("\n".join(newLines) + "\n")

#             fileCounter += 1

#     print(f"✅ {prefix} : {len(trainFiles)} train / {len(valFiles)} val")


def convertXmlToYolo(xmlPath):
    """
    Convertit un fichier XML (format Pascal VOC) en format YOLO.
    Retourne une liste de lignes YOLO.
    """
    tree = ET.parse(xmlPath)
    root = tree.getroot()

    imageWidth = int(root.find("size/width").text)
    imageHeight = int(root.find("size/height").text)

    yoloLines = []
    for obj in root.findall("object"):
        bbox = obj.find("bndbox")
        xmin = int(bbox.find("xmin").text)
        ymin = int(bbox.find("ymin").text)
        xmax = int(bbox.find("xmax").text)
        ymax = int(bbox.find("ymax").text)

        # Convertir en format YOLO (normalisé)
        x_center = ((xmin + xmax) / 2) / imageWidth
        y_center = ((ymin + ymax) / 2) / imageHeight
        width = (xmax - xmin) / imageWidth
        height = (ymax - ymin) / imageHeight

        yoloLines.append(f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")  # class_id=0 par défaut

    return yoloLines



def renameAndAdaptToYolo(dataDir, outputImageDir, outputLabelDir, prefix, trainRatio=0.8):
    """
    Gère le renommage, la conversion et le split entre train/val pour des fichiers .xml et .txt dans un même dossier.
    """
    # Print the number of files in the data directory
    print(f"Number of files in {dataDir}: {len(os.listdir(dataDir))}")
    # Création des répertoires de sortie
    trainImageDir = os.path.join(outputImageDir, "train")
    valImageDir = os.path.join(outputImageDir, "val")
    trainLabelDir = os.path.join(outputLabelDir, "train")
    valLabelDir = os.path.join(outputLabelDir, "val")

    for directory in [trainImageDir, valImageDir, trainLabelDir, valLabelDir]:
        os.makedirs(directory, exist_ok=True)

    # Récupération des fichiers d'images
    imageFiles = [f for f in os.listdir(dataDir) if f.endswith(".jpg") or f.endswith(".png")]
    random.shuffle(imageFiles)

    # Split train / validation
    splitIndex = int(len(imageFiles) * trainRatio)
    trainFiles, valFiles = imageFiles[:splitIndex], imageFiles[splitIndex:]

    fileCounter = 1
    for dataset, fileList, imgDir, lblDir in [("train", trainFiles, trainImageDir, trainLabelDir), 
                                               ("val", valFiles, valImageDir, valLabelDir)]:
        for fileName in tqdm.tqdm(fileList, desc=f"Processing {prefix} -> {dataset}"):
            baseName = os.path.splitext(fileName)[0]
            oldImagePath = os.path.join(dataDir, fileName)

            # Déterminer les chemins
            newBaseName = f"{prefix}_{fileCounter:04d}"
            newImagePath = os.path.join(imgDir, newBaseName + ".jpg")
            newLabelPath = os.path.join(lblDir, newBaseName + ".txt")

            # Copier l'image
            shutil.copy(oldImagePath, newImagePath)

            # Vérifier si l'annotation existe sous format .txt ou .xml
            oldTxtPath = os.path.join(dataDir, baseName + ".txt")
            oldXmlPath = os.path.join(dataDir, baseName + ".xml")

            yoloAnnotations = []
            if os.path.exists(oldTxtPath):  
                with open(oldTxtPath, "r") as file:
                    yoloAnnotations = file.readlines()

            elif os.path.exists(oldXmlPath): 
                yoloAnnotations = convertXmlToYolo(oldXmlPath)

            if yoloAnnotations:
                with open(newLabelPath, "w") as file:
                    file.write("\n".join(yoloAnnotations) + "\n")

            fileCounter += 1

    print(f"✅ {prefix} : {len(trainFiles)} train / {len(valFiles)} val")


def verifyImageLabels(imageDir, labelDir):
    imageFiles = {os.path.splitext(f)[0] for f in os.listdir(imageDir) if f.endswith(('.jpg', '.png'))}
    labelFiles = {os.path.splitext(f)[0] for f in os.listdir(labelDir) if f.endswith('.txt')}

    missingLabels = imageFiles - labelFiles
    missingImages = labelFiles - imageFiles

    if missingLabels:
        print(f"⚠️ {len(missingLabels)} missing in {imageDir}:")
        print(missingLabels)

    if missingImages:
        print(f"⚠️ {len(missingImages)} missing in {labelDir}:")
        print(missingImages)

    if not missingLabels and not missingImages:
        print(f"✅ {imageDir} & {labelDir} !")



if __name__ == "__main__":
    # renameAndAdaptToYolo(
    #     dataDir="datasets/rawData/Uav", 
    #     outputImageDir="datasets/images",
    #     outputLabelDir="datasets/labels", 
    #     prefix="Uav"
    # )

    # print("Uav done.")
    # print("Passing to Drones...")

    # renameAndAdaptToYolo(
    #     dataDir="datasets/rawData/Drones", 
    #     outputImageDir="datasets/images",
    #     outputLabelDir="datasets/labels", 
    #     prefix="Drones"
    # )
    # print("Drones done.")
    # print("Passing to Verification...")
    print(len(os.listdir("datasets/images/train")))
    print(len(os.listdir("datasets/labels/train")))

    print(len(os.listdir("datasets/images/val")))
    print(len(os.listdir("datasets/labels/val")))

    verifyImageLabels(
        imageDir="datasets/images/train", 
        labelDir="datasets/labels/train"
    )

    verifyImageLabels(
        imageDir="datasets/images/val", 
        labelDir="datasets/labels/val"
    )

