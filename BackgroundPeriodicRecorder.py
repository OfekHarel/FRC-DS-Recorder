from networktables import NetworkTables
from MatchRecorder import MatchRecorder
from NT_helper import nt_init
import os


class PeriodicRecorder:

    def __init__(self, enable_entry_path, fps=15, output='', simulation=False):
        self.enable_entry_path = enable_entry_path
        self.recorder = MatchRecorder(fps, output)
        self.started = False

        print("waiting for connections...")
        ip = '10.33.39.2' if not simulation else 'localhost'
        if simulation:
            self.enable_entry_path = "/recorder/start"
            NetworkTables.startClient(ip)
        nt_init(ip)

    
    def is_recording(self):
        return NetworkTables.getEntry(self.enable_entry_path).getBoolean(False)

    def start(self):
        while True:
            if self.is_recording():
                self.started = True
                self.recorder.next_frame()

            elif self.started:
                self.started = False
                self.recorder.stop()


if __name__ == '__main__':
    pr = PeriodicRecorder("/SmartDashboard/DS_recording/isStarted", fps=15, output=os.path.join(os.environ['USERPROFILE'], r'Videos\Captures'), simulation=False)
    pr.start()
            
