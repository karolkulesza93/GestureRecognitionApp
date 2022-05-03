import cv2
from datetime import datetime
from logger import Logger

def saveImg(img):
    name = 'Img_' + str(datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3])
    cv2.imwrite(f'C:/Users/KarolKulesza/Studia/MASTERS DEGREE DATA SCIENCE IN PRACTICE/img/{name}.jpg', img)
    Logger.message(f'Screenshot saved as {name}.jpg')