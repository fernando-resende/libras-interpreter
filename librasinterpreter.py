import math
import shutil
import string
import time
import os
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
from enum import Enum

#class LibrasDetector:
'''
Libras (Brazil's signal language) interpreter in real time.
This project use Artificial Intelligence (AI), trained with static images
of each character, except for those who need some movment. So, the project
can not recognize J, X and Z, yet...
'''

#Constants
OFFSET = 20
IMG_SIZE = 300
COLOR_MAIN = (0, 255, 0)
COLOR_CONTRAST = (255, 255, 255)
FOLDER = 'data'
ALPHABET = string.ascii_uppercase
DELAY = 100
MODE = Enum('Mode', ['Detection', 'Dataset'])
DATASET_SAMPLES = 300

period = time.time()
currentMode = MODE.Detection
collectingData = False
datasetChar = ' '
datasetPath = ' '
counter = 1
camera = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1, detectionCon=0.8, minTrackCon=0.8)
labels = open('model/labels.txt', 'r').readlines()
classifier = Classifier('model/keras_model.h5','model/labels.txt')

def getTimeInMilli(period):
    return int(round(period * 1000))

def cv2PutTextWithShadow(img, text, org = (5,15), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=COLOR_MAIN, thickness=1):
    #cv2.rectangle(img, (0,0), (300,50), color=(250,250,250), thickness=cv2.FILLED) #Background test
    cv2.putText(img, text, org, fontFace=fontFace, fontScale=fontScale, color=(100,100,100), thickness=4) #Shadow
    cv2.putText(img, text, org, fontFace=fontFace, fontScale=fontScale, color=color, thickness=thickness) #Text

while True:
    success, img = camera.read()
    hands, img = detector.findHands(img)

    #Show mode on top
    cv2PutTextWithShadow(img, f'Modo: {currentMode.name} - Pressione TAB para alterar')

    if (currentMode == MODE.Dataset) and not collectingData:
        cv2PutTextWithShadow(img, 'Faca o gesto e pressione a letra correspondente para iniciar a caputura das imagens.', (5,30), fontScale=0.35)
        cv2PutTextWithShadow(img, 'Mova sua mao em direcoes distintas, afaste, aproxime e incline para obter melhores amostras.', (5,45), fontScale=0.35)

    if hands:
        hand = hands[0]
        x, y, width, height = hand['bbox']
        imgBgBlack = np.zeros((IMG_SIZE, IMG_SIZE, 3), dtype=np.uint8)
        imgCropped = img[y - OFFSET:y + height, x- OFFSET:x + width + OFFSET]
        imgCroppedShape = imgCropped.shape
        aspectRatio = height/width

        #Calculations need to center the hand image on a fixed width/height background
        baseCalc = (IMG_SIZE / height) if aspectRatio > 1 else (IMG_SIZE / width)
        aspectCalc = math.ceil((baseCalc * width) if aspectRatio > 1 else (baseCalc * height))
        gapStart = math.ceil((IMG_SIZE - aspectCalc) / 2)
        gapEnd = gapStart + aspectCalc

        try:
            if aspectRatio > 1:
                imgResized = cv2.resize(imgCropped, (aspectCalc, IMG_SIZE))
                imgBgBlack[:, gapStart:gapEnd] = imgResized

            else:
                imgResized = cv2.resize(imgCropped, (IMG_SIZE, aspectCalc))
                imgBgBlack[gapStart:gapEnd, :] = imgResized

            imgResizedShape = imgResized.shape

            #Predict libras char
            if currentMode == MODE.Detection:
                predictions, index = classifier.getPrediction(imgBgBlack, draw=False)
                confidence = predictions[index]
                prediction = labels[index].split(' ')[1].replace('\n','') if confidence >= 0.7 else '?'

                print(f' {prediction} is the guess with {round(confidence * 100, 2)}% of confidence')

                cv2.rectangle(img, (x + width, y - OFFSET - 30), (x + width + OFFSET + 2, y - OFFSET), color=COLOR_MAIN, thickness=cv2.FILLED)
                cv2.putText(img, prediction, (x + width, y - 25), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=COLOR_CONTRAST, thickness=2)
                cv2.rectangle(img, (x - OFFSET, y - OFFSET), (x + width + OFFSET, y + height + OFFSET), color=COLOR_MAIN, thickness=3)
                
            else:
                if (datasetChar in ALPHABET) and collectingData:
                    #Show wich character is being caputured
                    cv2PutTextWithShadow(img, f'Obtendo imagens de libras da letra {datasetChar}', (5,30), fontScale=0.35)
                    cv2PutTextWithShadow(img, f'Capturando imagem {counter} de {DATASET_SAMPLES}', (5,45), fontScale=0.35)

                    if ((getTimeInMilli(time.time()) - getTimeInMilli(period)) > DELAY) and counter <= DATASET_SAMPLES:                        
                        period = time.time()
                        print(f'running every {DELAY}ms - current time {period}')
                        imgPath = f'{datasetPath}/{datasetChar}_{time.time()}.jpg'
                        cv2.imwrite(imgPath, imgBgBlack)
                        print(f'{counter} images caputured (char {datasetChar})')
                        counter += 1
                    
                    if counter > DATASET_SAMPLES:
                        datasetChar = ' '
                        counter = 1
                        collectingData = False

            #cv2.imshow('ImageCropped', imgCropped)
            #cv2.imshow('ImageBgBlack', imgBgBlack)

        except Exception as e:
            print('### ERROR FOUND ###')
            print(f'Aspect calculated: {aspectCalc}')
            print(f'Error: {e}')
    
    cv2.imshow("Detector de Libras", img)
    key = cv2.waitKey(1)

    if key > 0:

        if key == 9: #TAB
            currentMode = MODE.Detection if currentMode == MODE.Dataset else MODE.Dataset
            print(currentMode)
            continue

        if key == 27: #ESC
            print('Exiting the system...')
            break
    
        datasetChar = chr(key).upper()

        if (datasetChar in ALPHABET) and (currentMode == MODE.Dataset):
            collectingData = True
            datasetPath = f'{FOLDER}/{datasetChar}'        
            os.makedirs(datasetPath, exist_ok=True)
            for filename in os.listdir(datasetPath):
                filepath = os.path.join(datasetPath, filename)
                try:
                    shutil.rmtree(filepath)
                except OSError:
                    os.remove(filepath)

    #if key == ord('s'):
    #    pass

camera.release()
cv2.destroyAllWindows()