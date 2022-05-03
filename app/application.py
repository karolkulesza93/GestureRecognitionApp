import cv2
import keyboard
import mediapipe as mp
from gestureDetector import GestureDetector
from logger import Logger
import helpers

class Application():
    def __init__(self):
        Logger.message("Initializing application...")
        try:
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
        while True:
            try:
                success, img = self._cap.read()
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = self._hands.process(imgRGB)

                if results.multi_hand_landmarks:
                    if len(results.multi_hand_landmarks) == 1:
                        self._mpDraw.draw_landmarks(img, results.multi_hand_landmarks[0], self._mpHands.HAND_CONNECTIONS, 
                            self._mpDraw.DrawingSpec(color=(0,0,255)),
                            self._mpDraw.DrawingSpec(color=(0,255,0)))
                        self._detector.detectOneHandedGestures(results.multi_hand_landmarks[0], img)
                    if len(results.multi_hand_landmarks) == 2:
                        self._mpDraw.draw_landmarks(img, results.multi_hand_landmarks[0], self._mpHands.HAND_CONNECTIONS, 
                            self._mpDraw.DrawingSpec(color=(0,0,255)),
                            self._mpDraw.DrawingSpec(color=(0,255,0)))
                        self._mpDraw.draw_landmarks(img, results.multi_hand_landmarks[1], self._mpHands.HAND_CONNECTIONS, 
                            self._mpDraw.DrawingSpec(color=(0,255,0)),
                            self._mpDraw.DrawingSpec(color=(0,0,255)))
                        self._detector.detectTwoHandedGestures(results.multi_hand_landmarks[0], results.multi_hand_landmarks[1], img)

                cv2.imshow("Hand Gesture Recognition App", img)
                cv2.waitKey(1)

                if keyboard.is_pressed('q'):
                    Logger.message("Terminating application...")
                    break;
                if keyboard.is_pressed('s'):
                    helpers.saveImg(img)
            except BaseException as ex:
                Logger.error(str(ex))

if __name__ == '__main__':
    main()