import time
import xbmc
import sys
__cwd__ = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__resource__ = xbmc.translatePath(os.path.join(__cwd__, 'resources', 'lib')).decode('utf-8')
sys.path.append(__resource__)
from dmx import SimpleLight

class Player(xbmc.Player):
    def __init__(self):
        super(Player, self).__init__()

    def onPlayBackStarted(self):
        # wait for playback to be really available
        for i in xrange(1, 40):
            if not (self.isPlayingAudio() or self.isPlayingVideo()):
                if i == 40:
                    return
                else:
                    xbmc.sleep(250)
        self.onPlayBackStartedEx()#do dmx things here

        def onPlayBackStopped(self):
            pass
        def onPlayBackEnded(self):
            pass
        def onPlayBackPaused(self):
            pass
        def onPlayBackResumed(self):
            pass

class Monitor(xbmc.Monitor):
    # Energy Savings mode
    def onDPMSActivated(self):
        pass
    def onDPMSDeactivated(self):
        pass
    def onScreensaverActivated(self):
        pass
    def onScreensaverDeactivated(self):
        pass

class Dispatcher:
    light = None
    def checkPlaying(self):
    	pass
    def pause(self):
    	light.setState('bright')
    def play(self):
    	light.setState('dark')

if __name__ == '__main__':
    monitor = xbmc.Monitor()
    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds
        if monitor.waitForAbort(10):
            # Abort was requested while waiting. We should exit
            break
        xbmc.log("dmx %s" % time.time(), level=xbmc.LOGDEBUG)
    xbmc.log("dmx aborted %s" % time.time(), level=xbmc.LOGDEBUG)

