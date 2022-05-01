import utils
from handLandmarksHelper import HandLandMarksHelper as hnd
import cv2
from logger import Logger


class GestureDetector():
    def __init__(self):
        self._consoleLog = False

    def detectOneHandedGestures(self, hand, img):
        screenLogs = []
        
        screenLogs.append(str(self._fingerCount(hand, img)))
        if self._ok(hand, img):
            self._log("OK")
            screenLogs.append("OK")
        if self._peace(hand, img):
            self._log("PEACE")
            screenLogs.append("PEACE")
        if self._rock(hand, img):
            self._log("ROCK")
            screenLogs.append("ROCK")
        if self._indexFinger(hand, img):
            self._log("Index finger")
            screenLogs.append("Index finger")
        if self._middleFinger(hand, img):
            self._log("Middle finger")
            screenLogs.append("Middle finger")
        if self._ringFinger(hand, img):
            self._log("Ring finger")
            screenLogs.append("Ring finger")
        if self._pinky(hand, img):
            self._log("Pinky")
            screenLogs.append("Pinky")

        for i in range(len(screenLogs)):
            self._screenLog(screenLogs[i], img, y = 30 + 30 * i)

    def detectTwoHandedGestures(self, hands, img):
        pass
    
    def _log(self, name):
        if self._consoleLog:
            Logger.detection(f"Gesture detected: \'{name}\'")

    def _screenLog(self, name, img, y = 30, color = (0, 255, 0)):
        cv2.putText(img, name, (5, y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    
#region Fingers

    def _indexFinger(self, hand, img):
        pos = utils.getPositionsWithId(hand.landmark, img)
        return hnd.INDEX_FINGER_TIP(pos)[2] < hnd.INDEX_FINGER_PIP(pos)[2]

    def _middleFinger(self, hand, img):
        pos = utils.getPositionsWithId(hand.landmark, img)
        return hnd.MIDDLE_FINGER_TIP(pos)[2] < hnd.MIDDLE_FINGER_PIP(pos)[2]

    def _ringFinger(self, hand, img):
        pos = utils.getPositionsWithId(hand.landmark, img)
        return hnd.RING_FINGER_TIP(pos)[2] < hnd.RING_FINGER_PIP(pos)[2]

    def _pinky(self, hand, img):
        pos = utils.getPositionsWithId(hand.landmark, img)
        return hnd.PINKY_TIP(pos)[2] < hnd.PINKY_PIP(pos)[2]

    def _fingerCount(self, hand, img):
        count = 0
        if self._indexFinger(hand, img): count = count + 1
        if self._middleFinger(hand, img): count = count + 1
        if self._ringFinger(hand, img): count = count + 1
        if self._pinky(hand, img): count = count + 1
        return count

#endregion Fingers

#region Gestures

    def _ok(self, hand, img):
        pos = utils.getPositionsWithId(hand.landmark, img)
        a = hnd.THUMB_TIP(pos)
        b = hnd.INDEX_FINGER_TIP(pos)
        l = utils.length(a, b)
        if l < 10:
            return True
        return False

    def _peace(self, hand, img):
        return self._indexFinger(hand, img) and self._middleFinger(hand, img)

    def _rock(self, hand, img):
        return self._indexFinger(hand, img) and self._pinky(hand, img)

#endregion Gestures

if __name__ == '__main__':
    main()