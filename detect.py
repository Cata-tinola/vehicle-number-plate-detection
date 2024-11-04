# to detect number plates from cars
import cv2
from ultralytics import YOLO
import os

model=YOLO('anprYolov8s.pt')
cwd=os.getcwd()
testDir = os.path.join(cwd,'ANPR Test')

files=[os.path.join(testDir,file) for file in os.listdir(testDir)]
for file in files:
    result=model(file)
    for r in result:
        boxes=r.boxes
        for box in boxes:
            x1,y1,x2,y2=map(int,box.xyxy[0])
            img=cv2.imread(file)
            plate=img[y1:y2,x1:x2]
            plateName=file.split('\\')[-1]
            print(plateName)
            cv2.imshow('plate',plate)
            cv2.imwrite(f'./plates/{plateName}',plate)
            cv2.waitKey(1)
    
