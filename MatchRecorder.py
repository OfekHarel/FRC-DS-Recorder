import cv2
from networktables import NetworkTables
import numpy as np
import pyautogui
import os

class MatchRecorder:

    def __init__(self, FPS, output):
        self.SCREEN_SIZE = tuple(pyautogui.size())
        self.FPS = FPS
        self.REC_SEC = 150
        self.OUT_PATH = output
        self.MATCH_TYPE_MAP = {0: 'NA', 1: 'PM', 2: 'QM', 3: 'EM'}
        self.vid_out = None
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.table = NetworkTables.getTable('FMSInfo')

    
    def _get_match_discription(self):
        match_type = self.table.getNumber('MatchType', 0)
        match_number = self.table.getNumber('MatchNumber', 0)
        replay_number = self.table.getNumber('ReplayNumber', 0)
        
        return "_".join([str(self.MATCH_TYPE_MAP[match_type]), str(match_number), str(replay_number)])


    def _get_vid_out(self):
        return cv2.VideoWriter(f"{os.path.join(self.OUT_PATH, self._get_match_discription())}.mp4", self.fourcc, self.FPS, (self.SCREEN_SIZE))


    def start(self):
        print("starting...")
        self.vid_out = self._get_vid_out()
        for _ in range(int(self.REC_SEC * self.FPS)):
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.vid_out.write(frame)
        print("closing...")
