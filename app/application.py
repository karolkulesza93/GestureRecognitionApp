import cv2
import keyboard
import mediapipe as mp
from gestureDetector import GestureDetector
from logger import Logger
import utils
from handLandmarksHelper import HandLandMarksHelper as hnd

class Application():
    def __init__(self):
        Logger.message("Initializing application...")
        try:
            self._x = 300
            self._y = 300
            self._name = "Hand Gesture Recognition App"
            self._isRunning = True
            self._cap = cv2.VideoCapture(0)
            self._mpHands = mp.solutions.hands
            self._hands = self._mpHands.Hands()
            self._mpDraw = mp.solutions.drawing_utils
            self._detector = GestureDetector()
            Logger.success("Initialized successfully.")
        except BaseException as ex:
            Logger.error(str(ex))

    def run(self):
        self._mainLoop()
        cv2.destroyAllWindows()
        Logger.success("Terminated successfully.")

    def _mainLoop(self):
        Logger.message("Detection started.")
        while self._isRunning:
            try:
                success, img = self._cap.read()
                img = cv2.flip(img, 1)
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = self._hands.process(imgRGB)
                
                if results.multi_hand_landmarks:
                    if len(results.multi_hand_landmarks) == 1:
                        self._mpDraw.draw_landmarks(img, results.multi_hand_landmarks[0], self._mpHands.HAND_CONNECTIONS, 
                            self._mpDraw.DrawingSpec(color=(0,0,255)),
                            self._mpDraw.DrawingSpec(color=(0,255,0)))
                        self._detector.detectOneHandedGestures(results.multi_hand_landmarks[0], img)
                        # self._handleOneHandedGestures(results.multi_hand_landmarks[0], img)
                    if len(results.multi_hand_landmarks) == 2:
                        self._mpDraw.draw_landmarks(img, results.multi_hand_landmarks[0], self._mpHands.HAND_CONNECTIONS, 
                            self._mpDraw.DrawingSpec(color=(0,0,255)),
                            self._mpDraw.DrawingSpec(color=(0,255,0)))
                        self._mpDraw.draw_landmarks(img, results.multi_hand_landmarks[1], self._mpHands.HAND_CONNECTIONS, 
                            self._mpDraw.DrawingSpec(color=(0,255,0)),
                            self._mpDraw.DrawingSpec(color=(0,0,255)))
                        self._detector.detectTwoHandedGestures(results.multi_hand_landmarks[0], results.multi_hand_landmarks[1], img)
                        self._handleTwoHandedGestures(results.multi_hand_landmarks[0], results.multi_hand_landmarks[1], img)
                        
                cv2.imshow(self._name, img)
                cv2.waitKey(1)

                if keyboard.is_pressed('q'):
                    Logger.message("Terminating application...")
                    self._isRunning = False
                if keyboard.is_pressed('s'):
                    utils.saveImg(img)
            except BaseException as ex:
                Logger.error(str(ex))

    def _handleOneHandedGestures(self, hand, img):
        pass
    
    def _handleTwoHandedGestures(self, hand1, hand2, img):
        if self._detector.ok(hand1, img) and self._detector.ok(hand2, img):
            self._isRunning = False
        
        if self._detector.heartUpward(hand1, hand2, img):
            self._isRunning = False
            
        # if self._detector.closedHand(hand1, img) and self._detector.openedHand(hand2, img):
        #     cv2.moveWindow(self._name, 0, 0)
        # elif self._detector.closedHand(hand2, img) and self._detector.openedHand(hand1, img):
        #     cv2.moveWindow(self._name, 1000, 0)
            
        if self._detector.peace(hand2, img):
            pos = utils.getPositionsWithId(hand1.landmark, img)
            utils.highlightPoint(img, hnd.INDEX_FINGER_TIP(pos))
            vec = self._detector.indexFingerUnitVector(hand1, img);
            self._x = self._x + vec[0] * 5
            self._y = self._y + vec[1] * 5
            cv2.moveWindow(self._name, int(self._x), int(self._y))
        elif self._detector.peace(hand1, img):
            pos = utils.getPositionsWithId(hand2.landmark, img)
            utils.highlightPoint(img, hnd.INDEX_FINGER_TIP(pos))
            vec = self._detector.indexFingerUnitVector(hand2, img);
            self._x = self._x + vec[0] * 5
            self._y = self._y + vec[1] * 5
            cv2.moveWindow(self._name, int(self._x), int(self._y))
            
        if self._detector.closedHand(hand1, img):
            l = self._detector.scale(hand2, img)
        elif self._detector.closedHand(hand2, img):
            l = self._detector.scale(hand1, img)
            
if __name__ == '__main__':
    main()