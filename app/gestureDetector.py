import utils
import cv2
from logger import Logger

class GestureDetector():
    def __init__(self):
        self._consoleLog = False

    def detectOneHandedGestures(self, hand, img):
        if self._ok(hand, img):
            self._log("OK")
            self._screenLog("OK", img, 30)
        if self._peace(hand, img):
            self._log("PEACE")
            self._screenLog("PEACE", img, 60)

    def detectTwoHandedGestures(self, hands, img):
        pass

    def _log(self, name):
        if self._consoleLog:
            Logger.detection(f"Gesture detected: \'{name}\'")

    def _screenLog(self, name, img, y = 30, color = (0, 255, 0)):
        cv2.putText(img, name, (5, y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    def _ok(self, hand, img):
        pos = utils.getPositionWithId(hand.landmark, img)
        a = pos[4]
        b = pos[8]
        l = utils.length(a, b)
        if l < 6:
            return True
        return False

    def _peace(self, hand, img):
        pos = utils.getPositionWithId(hand.landmark, img)
        
        return False