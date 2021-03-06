from networktables import NetworkTables
from MatchRecorder import MatchRecorder
from NT_helper import nt_init
import os
import time

class PeriodicRecorder:

    def __init__(self, enable_entry_path, fps=15, output='', simulation=False):
        self.enable_entry_path = enable_entry_path
        self.recorder = MatchRecorder(fps, output)
        self.FPS = fps
        self.started = False

        print("waiting for connections...")
        if simulation:
            ip = 'localhost'
            self.enable_entry_path = "/recorder/start"
            NetworkTables.startClient(ip)
            ip = nt_init(ip)
        else:
            ip = nt_init('10.33.39.2', '169.254.117.18')

    
    def is_recording(self):
        if NetworkTables.isConnected():
            val = NetworkTables.getEntry(self.enable_entry_path).getBoolean(False)
        else:
            val = False
        return val

    def start(self):
        while True:
            if self.is_recording():
                self.recorder.next_frame()
                self.started = True

            elif self.started:
                self.started = False
                self.recorder.stop()


if __name__ == '__main__':
    pr = PeriodicRecorder("/SmartDashboard/DS_recording/isStarted", fps=15, output=os.path.join(os.environ['USERPROFILE'], r'Videos\Captures'), simulation=False)
    pr.start()
            
