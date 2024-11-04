#To oranginze the files for training yolo

from bs4 import BeautifulSoup
import os
import shutil
import random


pwd = os.getcwd()
source = os.path.join(pwd, 'images')
os.makedirs('train/images', exist_ok=True)
os.makedirs('train/labels', exist_ok=True)
os.makedirs('val/images', exist_ok=True)
os.makedirs('val/labels', exist_ok=True)
trainImgDir = os.path.join(pwd, 'train/images')
trainLabelDir = os.path.join(pwd, 'train/labels')
valImgDir = os.path.join(pwd, 'val/images')
valLabelDir = os.path.join(pwd, 'val/labels')

def moveImgages():
    for dir, _, files in os.walk(source):
        for file in files:
            if file.endswith('jpeg'):
                imgSrcPath = os.path.join(source, file)
                imgDestPath = os.path.join(trainImgDir, file)
                shutil.move(imgSrcPath, imgDestPath)
    print("All images moved !")


def normalizeValues(values):
    xmin = values['xmin']/values['width']
    xmax = values['xmax']/values['width']
    ymin = values['ymin']/values['height']
    ymax = values['ymax']/values['height']

    width = xmax-xmin
    height = ymax-ymin
    center_x = xmin+width/2
    center_y = ymin+height/2

    return center_x, center_y, width, height


def parser():
    tags = ['xmin', 'xmax', 'ymin', 'ymax', 'width', 'height']
    for dir, _, files in os.walk(source):
        for file in files:
            filePath = os.path.join(source, file)
            values = {}
            with open(filePath) as f:
                soup = BeautifulSoup(f, features='lxml-xml')
                for tag in tags:
                    values[tag] = int(soup.find(tag).text)
            center_x, center_y, width, height = normalizeValues(values)
            with open(f'{trainLabelDir}/{file.split('.')[0]}'+'.txt', 'w') as txtFile:
                txtFile.write(f"0 {center_x} {center_y} {width} {height}")


def move_random_data_toVal(trainImgDir,trainLabelDir, valImgDir,valLabelDir, num_files):
    all_files = [f for f in os.listdir( trainImgDir) if os.path.isfile(os.path.join(trainImgDir, f))]

    if num_files > len(all_files):
        num_files = len(all_files)
        print(f"Only {num_files} files available to move.")

    selected_files = random.sample(all_files, num_files)

    for fileName in selected_files:
        imgSrcPath = os.path.join(trainImgDir, fileName)
        imgDestPath = os.path.join(valImgDir, fileName)
        labelName=fileName.split('.')[0]+".txt"
        labelSrcPath = os.path.join(trainLabelDir, labelName)
        labelDestPath = os.path.join(valLabelDir, labelName)
        shutil.move(imgSrcPath, imgDestPath)
        shutil.move(labelSrcPath, labelDestPath)
        print(f"Moved: {fileName} to {valImgDir}")
        print(f"Moved: {labelName} to {valLabelDir}")

def setup():
    moveImgages()
    parser()
    move_random_data_toVal(trainImgDir,trainLabelDir,valImgDir,valLabelDir,25)

setup()