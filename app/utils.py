import cv2
import math

def getPositionWithId(landmarks, img):
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
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)