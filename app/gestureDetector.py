import utils
from handLandmarksHelper import HandLandMarksHelper as hnd
import cv2

class GestureDetector():
    def __init__(self):
        self._consoleLog = False
        self._touchingLenght = 20

    def detectOneHandedGestures(self, hand, img):
        screenLogs = []
        
        fingers = self.fingerCount(hand, img)
        screenLogs.append(f"Fingers: {fingers}")
        
        # length = self.scale(hand, img)
        # screenLogs.append("Lenght: {:.2f}%".format(length))
        
        if self.openedHand(hand, img):
            self._log("OPEN")
            screenLogs.append("OPEN")
        elif self.closedHand(hand, img):
            self._log("CLOSED")
            screenLogs.append("CLOSED")
        elif self.ok(hand, img):
            self._log("OK")
            screenLogs.append("OK")
        elif self.okMiddleFinger(hand, img):
            self._log("Thumb + middle finger")
            screenLogs.append("Thumb + middle finger")
        elif self.okRingFinger(hand, img):
            self._log("Thumb + ring finger")
            screenLogs.append("Thumb + ring finger")
        elif self.okPinky(hand, img):
            self._log("Thumb + pinky")
            screenLogs.append("Thumb + pinky")
        elif self.peace(hand, img):
            self._log("PEACE")
            screenLogs.append("PEACE")
        elif self.rock(hand, img):
            self._log("ROCK")
            screenLogs.append("ROCK")
        elif self.phone(hand, img):
            self._log("PHONE")
            screenLogs.append("PHONE")
        elif self.pistol(hand, img):
            self._log("PISTOL")
            screenLogs.append("PISTOL")
            
        if self.thumb(hand, img, True):
            self._log("Thumb")
            screenLogs.append("Thumb")
        
        if self.indexFinger(hand, img, True):
            self._log("Index finger")
            screenLogs.append("Index finger")
        
        if self.middleFinger(hand, img, True):
            self._log("Middle finger")
            screenLogs.append("Middle finger")
        
        if self.ringFinger(hand, img, True):
            self._log("Ring finger")
            screenLogs.append("Ring finger")
        
        if self.pinky(hand, img, True):
            self._log("Pinky")
            screenLogs.append("Pinky")

        for i in range(len(screenLogs)):
            self._screenLog(screenLogs[i], img, y = 30 + 30 * i)

    def detectTwoHandedGestures(self, hand1, hand2, img):
        screenLogs = []
        
        fingers1 = self.fingerCount(hand1, img)
        fingers2 = self.fingerCount(hand2, img)
        screenLogs.append(f'Fingers: {fingers2} + {fingers1} = {fingers1 + fingers2}')
        
        if self.heartUpward(hand1, hand2, img):
            self._log("HEART UPWARD")
            screenLogs.append("HEART UPWARD")
        elif self.frame(hand1, hand2, img):
            self._log("FRAME")
            screenLogs.append("FRAME")
        
        for i in range(len(screenLogs)):
            self._screenLog(screenLogs[i], img, y = 30 + 30 * i)
    
    def _log(self, name):
        if self._consoleLog:
            Logger.detection(f"Gesture detected: \'{name}\'")

    def _screenLog(self, name, img, y = 30, color = (0, 255, 170)):
        cv2.putText(img, name, (5, y), cv2.FONT_HERSHEY_DUPLEX, 1, color, 2, cv2.LINE_AA)
    
#region Fingers
    
    def thumb(self, hand, img, only = False):
        pos = utils.getPositionsWithId(hand.landmark, img)
        if (hnd.THUMB_MCP(pos)[1] > hnd.PINKY_MCP(pos)[1]):
            return (hnd.THUMB_TIP(pos)[1] > hnd.THUMB_IP(pos)[1]) if (not only) else (hnd.THUMB_TIP(pos)[1] > hnd.THUMB_IP(pos)[1]
                and not self.indexFinger(hand, img)
                and not self.middleFinger(hand, img)
                and not self.ringFinger(hand, img)
                and not self.pinky(hand, img))
        return (hnd.THUMB_TIP(pos)[1] < hnd.THUMB_IP(pos)[1]) if (not only) else (hnd.THUMB_TIP(pos)[1] < hnd.THUMB_IP(pos)[1]
            and not self.indexFinger(hand, img)
            and not self.middleFinger(hand, img)
            and not self.ringFinger(hand, img)
            and not self.pinky(hand, img))
    
    def indexFinger(self, hand, img, only = False):
        pos = utils.getPositionsWithId(hand.landmark, img)
        return (hnd.INDEX_FINGER_TIP(pos)[2] < hnd.INDEX_FINGER_PIP(pos)[2]) if (not only) else (hnd.INDEX_FINGER_TIP(pos)[2] < hnd.INDEX_FINGER_PIP(pos)[2]
            and not self.thumb(hand, img)
            and not self.middleFinger(hand, img)
            and not self.ringFinger(hand, img)
            and not self.pinky(hand, img))

    def middleFinger(self, hand, img, only = False):
        pos = utils.getPositionsWithId(hand.landmark, img)
        return (hnd.MIDDLE_FINGER_TIP(pos)[2] < hnd.MIDDLE_FINGER_PIP(pos)[2]) if (not only) else (hnd.MIDDLE_FINGER_TIP(pos)[2] < hnd.MIDDLE_FINGER_PIP(pos)[2]
            and not self.thumb(hand, img)
            and not self.indexFinger(hand, img)
            and not self.ringFinger(hand, img)
            and not self.pinky(hand, img))

    def ringFinger(self, hand, img, only = False):
        pos = utils.getPositionsWithId(hand.landmark, img)
        return (hnd.RING_FINGER_TIP(pos)[2] < hnd.RING_FINGER_PIP(pos)[2]) if (not only) else (hnd.RING_FINGER_TIP(pos)[2] < hnd.RING_FINGER_PIP(pos)[2]
            and not self.thumb(hand, img)
            and not self.indexFinger(hand, img)
            and not self.middleFinger(hand, img)
            and not self.pinky(hand, img))                                                                               

    def pinky(self, hand, img, only = False):
        pos = utils.getPositionsWithId(hand.landmark, img)
        return (hnd.PINKY_TIP(pos)[2] < hnd.PINKY_PIP(pos)[2]) if (not only) else (hnd.PINKY_TIP(pos)[2] < hnd.PINKY_PIP(pos)[2]
            and not self.thumb(hand, img)
            and not self.indexFinger(hand, img)
            and not self.middleFinger(hand, img)
            and not self.ringFinger(hand, img))

    def fingerCount(self, hand, img):
        count = 0
        if self.thumb(hand, img): count = count + 1
        if self.indexFinger(hand, img): count = count + 1
        if self.middleFinger(hand, img): count = count + 1
        if self.ringFinger(hand, img): count = count + 1
        if self.pinky(hand, img): count = count + 1
        return count

    def indexFingerUnitVector(self, hand, img):
        pos = utils.getPositionsWithId(hand.landmark, img)
        tip = hnd.INDEX_FINGER_TIP(pos)
        mid = hnd.INDEX_FINGER_DIP(pos)
        l = utils.length(tip, mid)
        return ((tip[1] - mid[1])/l, (tip[2] - mid[2])/l)
    
    def scale(self, hand, img):
        pos = utils.getPositionsWithId(hand.landmark, img)
        thumbTip = hnd.THUMB_TIP(pos)
        indexFingerTip = hnd.INDEX_FINGER_TIP(pos)
        mid = ((thumbTip[1] + indexFingerTip[1])/2, (thumbTip[2] + indexFingerTip[2])/2)
        cv2.line(img, indexFingerTip[1:3], thumbTip[1:3], (255,0,0), 3)
        lmax = 200
        lmin = 20
        l = utils.length(thumbTip, indexFingerTip)
        
        res = 0
        if l >= lmax: res = 1
        elif l <= lmin: res = 0
        else: res = (l-lmin/2)/lmax
        text = "{:.2f}%".format(res*100)
        cv2.putText(img, text, (int(mid[0]), int(mid[1])), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        return res        
    
#endregion Fingers

#region Gestures - one hand

    def openedHand(self, hand, img):
        return self.fingerCount(hand, img) == 5
    
    def closedHand(self, hand, img):
        return self.fingerCount(hand, img) == 0
    
    def ok(self, hand, img):
        pos = utils.getPositionsWithId(hand.landmark, img)
        return (utils.length(hnd.THUMB_TIP(pos), hnd.INDEX_FINGER_TIP(pos)) < self._touchingLenght
            and self.middleFinger(hand, img)
            and self.ringFinger(hand, img)
            and self.pinky(hand, img))

    def okMiddleFinger(self, hand, img):
        pos = utils.getPositionsWithId(hand.landmark, img)
        return (utils.length(hnd.THUMB_TIP(pos), hnd.MIDDLE_FINGER_TIP(pos)) < self._touchingLenght
            and self.indexFinger(hand, img)
            and self.ringFinger(hand, img)
            and self.pinky(hand, img))
    
    def okRingFinger(self, hand, img):
        pos = utils.getPositionsWithId(hand.landmark, img)
        return (utils.length(hnd.THUMB_TIP(pos), hnd.RING_FINGER_TIP(pos)) < self._touchingLenght
            and self.middleFinger(hand, img)
            and self.indexFinger(hand, img)
            and self.pinky(hand, img))
    
    def okPinky(self, hand, img):
        pos = utils.getPositionsWithId(hand.landmark, img)
        return (utils.length(hnd.THUMB_TIP(pos), hnd.PINKY_TIP(pos)) < self._touchingLenght
            and self.middleFinger(hand, img)
            and self.ringFinger(hand, img)
            and self.indexFinger(hand, img))
        
    def peace(self, hand, img):
        return (self.indexFinger(hand, img) 
            and self.middleFinger(hand, img)
            and not self.thumb(hand, img)
            and not self.ringFinger(hand, img)
            and not self.pinky(hand, img))

    def rock(self, hand, img):
        return (self.indexFinger(hand, img) 
            and self.pinky(hand, img)
            and not self.thumb(hand, img)
            and not self.middleFinger(hand, img)
            and not self.ringFinger(hand, img))

    def phone(self, hand, img):
        return (self.pinky(hand, img)
            and self.thumb(hand, img)
            and not self.indexFinger(hand, img) 
            and not self.middleFinger(hand, img)
            and not self.ringFinger(hand, img))
    
    def pistol(self, hand, img):
        return (self.indexFinger(hand, img)
            and self.thumb(hand, img)
            and not self.middleFinger(hand, img)
            and not self.ringFinger(hand, img)
            and not self.pinky(hand, img))
    
    def thumbsUp(self, hand, img):
        pos = utils.getPositionsWithId(hand.landmark, img)
        return (hnd.THUMB_TIP(pos)[2] < hnd.THUMB_IP(pos)[2]
            and hnd.PINKY_MCP(pos)[2] > hnd.INDEX_FINGER_MCP(pos)[2]
            and not self.thumb(hand, img)
            and not self.indexFinger(hand, img)
            and not self.middleFinger(hand, img)
            and not self.ringFinger(hand, img)
            and not self.pinky(hand, img))
    
    def thumbsDown(self, hand, img):
        pos = utils.getPositionsWithId(hand.landmark, img)
        return (hnd.THUMB_TIP(pos)[2] > hnd.THUMB_IP(pos)[2]
            and hnd.PINKY_MCP(pos)[2] < hnd.INDEX_FINGER_MCP(pos)[2]
            and not self.thumb(hand, img)
            and not self.indexFinger(hand, img)
            and not self.middleFinger(hand, img)
            and not self.ringFinger(hand, img)
            and not self.pinky(hand, img))

#endregion Gestures

#region Gestures - two hands

    def heartUpward(self, hand1, hand2, img):
        pos1 = utils.getPositionsWithId(hand1.landmark, img)
        pos2 = utils.getPositionsWithId(hand2.landmark, img)
        return (utils.length(hnd.THUMB_TIP(pos1), hnd.THUMB_TIP(pos2)) < self._touchingLenght and
            utils.length(hnd.INDEX_FINGER_TIP(pos1), hnd.INDEX_FINGER_TIP(pos2)) < self._touchingLenght)
    
    def frame(self, hand1, hand2, img):
        pos1 = utils.getPositionsWithId(hand1.landmark, img)
        pos2 = utils.getPositionsWithId(hand2.landmark, img)
        return (utils.length(hnd.THUMB_TIP(pos1), hnd.INDEX_FINGER_TIP(pos2)) < self._touchingLenght and
            utils.length(hnd.THUMB_TIP(pos2), hnd.INDEX_FINGER_TIP(pos1)) < self._touchingLenght)
    
#endregion Gestures - two hands

if __name__ == '__main__':
    main()