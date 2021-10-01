import random
import threading
import time
import kbInput
import puzzle
import Gesture_Detector

class Game2048():
    def __init__(self):
        self.gesture = None
        self.new_gesture_flag = False
        self.flag = False
        self.GD = None

        # self._lock = threading.RLock()
        self._t_effector1 = threading.Thread(target=self.gesture_worker)
        self._t_effector1.daemon = True

        #"before the start`"
        self._t_effector1.start()

        self._t_effector2 = threading.Thread(target=self.pizzle_worker)
        self._t_effector2.daemon = True

        # "before the start`"
        self._t_effector2.start()

    def pizzle_worker(self):
        puzzle.GameGrid()

    def gesture_worker(self):
        while True:
            try:
                if self.flag == False:
                    # print("I am here")
                    self.GD = Gesture_Detector.Gesture_Detector()
                    self.flag = True
                self.gesture = self.GD.getGesture()
                # if (self.gesture != 0):
                #     print(111111111)
                # print(self.gesture)
                # self.gesture = random.randint(1,8)

                # print(self.gesture)
                kbInput.createKeyInput(self.gesture)
            except Exception as e:
                print("EXCEPTION In gesture_worker: ", e)
            # # self.new_gesture_flag = True
            time.sleep(0.08)


if __name__ == '__main__':
    my_game = Game2048()
    while True:
        # print(my_game.gesture)
        time.sleep(0.05)
