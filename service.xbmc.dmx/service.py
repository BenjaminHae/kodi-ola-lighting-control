import time
import xbmc
import xbmcaddon
import sys
import os
__addon__ = xbmcaddon.Addon('service.dmx')
__cwd__ = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__resource__ = xbmc.translatePath(os.path.join(__cwd__, 'resources', 'lib')).decode('utf-8')
sys.path.append(__resource__)
from dmx import SimpleLight

class Player(xbmc.Player):
    dispatcher = None
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
        dispatcher.play()

    def onPlayBackStopped(self):
        dispatcher.pause()

    def onPlayBackEnded(self):
        dispatcher.pause()

    def onPlayBackPaused(self):
        dispatcher.pause()

    def onPlayBackResumed(self):
        dispatcher.play()

class Monitor(xbmc.Monitor):
    dispatcher = None
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
    player = None
    def checkPlaying(self):
        return player.isPlayingVideo()

    def pause(self):
        light.setStateByName('full')

    def play(self):
        if self.checkPlaying():
            light.setStateByName('dark')

if __name__ == '__main__':
    dispatcher = Dispatcher()
    monitor = Monitor()
    player = Player()
    light = SimpleLight()
    dispatcher.light = light
    dispatcher.player = player
    monitor.dispatcher = dispatcher
    player.dispatcher = dispatcher
    dispatcher.pause()
    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds
        if monitor.waitForAbort(10):
            # Abort was requested while waiting. We should exit
            break
        xbmc.log("dmx %s" % time.time(), level=xbmc.LOGDEBUG)
    dispatcher.pause()
    light.stop()
    xbmc.log("dmx aborted %s" % time.time(), level=xbmc.LOGDEBUG)
