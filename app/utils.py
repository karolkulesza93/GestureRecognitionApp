import cv2
import math
from datetime import datetime
from logger import Logger

def getPositionsWithId(landmarks, img):
    positions = []
    for id, lm in enumerate(landmarks):
        h, w, c = img.shape
        cx, cy = int(lm.x * w), int(lm.y * h)
        positions.append((id, cx, cy))
    return positions

def getPosition(pos):
    return (pos[1], pos[2])

def highlightPoint(img, pos, radius = 15):
    cv2.circle(img, (pos[1:3]), radius, (255,0,255), cv2.FILLED)

def length(a, b):
    return math.sqrt((a[1] - b[1])**2 + (a[2] - b[2])**2)

def saveImg(img):
    name = 'Img_' + str(datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3])
    cv2.imwrite(f'C:/Users/KarolKulesza/Studia/MASTERS DEGREE DATA SCIENCE IN PRACTICE/img/{name}.jpg', img)
    Logger.message(f'Screenshot saved as {name}.jpg')

if __name__ == '__main__':
    main()