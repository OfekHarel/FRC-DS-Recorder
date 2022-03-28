from math import ceil, floor
import cv2
from networktables import NetworkTables
import numpy as np
import pyautogui
import os
import time

class MatchRecorder:

    def __init__(self, FPS, output):
        self.SCREEN_SIZE = tuple(pyautogui.size())
        self.FPS = FPS
        self.OUT_PATH = output
        self.MATCH_TYPE_MAP = {0: 'NA', 1: 'PM', 2: 'QM', 3: 'EM'}
        self.vid_out = None
        self.was_init = False
        self.init_time = None
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.table = NetworkTables.getTable('FMSInfo')
        
        os.system("cls")


    def _get_match_discription(self):
        match_type = self.table.getNumber('MatchType', 0)
        match_number = self.table.getNumber('MatchNumber', 0)
        replay_number = self.table.getNumber('ReplayNumber', 0)
        
        return "_".join([str(self.MATCH_TYPE_MAP[match_type]), str(match_number), str(replay_number)])


    def _get_vid_out(self):
        return cv2.VideoWriter(f"{os.path.join(self.OUT_PATH, self._get_match_discription())}.avi", self.fourcc, self.FPS, (self.SCREEN_SIZE))


    def get_match_time(self) -> str:
        if self.was_init:
            return str(int(floor(time.time() - self.init_time)))
        else:
            return str(0)


    def next_frame(self):

        if not self.was_init:
            print(f"starting... {self._get_match_discription()}")
            self.vid_out = self._get_vid_out()
            self.was_init = True
            self.init_time = time.time()

        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.putText(frame, self.get_match_time().zfill(3), (self.SCREEN_SIZE[0] - 170, self.SCREEN_SIZE[1] - 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)
        self.vid_out.write(frame)
    
    def stop(self):
        print("closing...")
        self.vid_out.release()
        self.was_init = False
