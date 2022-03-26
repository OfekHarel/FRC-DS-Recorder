from networktables import NetworkTables
from MatchRecorder import MatchRecorder
from NT_helper import nt_init

class PeriodicRecorder:

    def __init__(self, enable_entry_path, fps=15, output='', simulation=False):
        self.enable_entry_path = enable_entry_path
        self.recorder = MatchRecorder(fps, output)

        print("waiting for connections...")
        ip = '10.33.39.2' if not simulation else 'localhost'
        if simulation:
            NetworkTables.startClient(ip)
        nt_init(ip)
    
    def is_recording(self):
        return NetworkTables.getEntry(self.enable_entry_path).getBoolean(False)
    
    def stop(self):
        NetworkTables.getEntry(self.enable_entry_path).setBoolean(False)

    def start(self):
        while True:
            if self.is_recording():
                self.recorder.start()
                self.stop()

if __name__ == '__main__':
    pr = PeriodicRecorder("/recorder/start", fps=10, output='', simulation=True)
    pr.start()
            