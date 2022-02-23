import cv2
import keyboard
import mediapipe as mp
from gestureDetector import GestureDetector
from logger import Logger

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
                    for handLms in results.multi_hand_landmarks:
                        self._mpDraw.draw_landmarks(img, handLms, self._mpHands.HAND_CONNECTIONS)
                        self._detector.detectOneHandedGestures(handLms, img)

                cv2.imshow("Hands", img)
                cv2.waitKey(1)

                if keyboard.is_pressed('q'):
                    Logger.message("Terminating application...")
                    break;
            except BaseException as ex:
                Logger.error(str(ex))