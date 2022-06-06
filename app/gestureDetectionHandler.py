import os
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

class GestureDetectionHandler():
    def shutdown(self):
        print("Bye bye")
        # os.system("shutdown /s /t 1")
        
    def changeMasterVolume(self, vol):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            volume.SetMasterVolume(vol, None)
                
if __name__ == '__main__':
    main()