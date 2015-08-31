import time
import xbmc
import dmx

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
    pass

class Light:
    states={'black':0,'dark':1,'night':2,'medium':3,'bright':4,'full':5}
    dmxstate=[[0,0,0,255],[75,75,75,255],[120,120,120,255],[150,150,150,255],[200,200,200,255],[255,255,255,255]]
    fadetime=1000
    currentState=0
    def setStateByName(self, state):
        self.setState(states[state]) 
    def setState(self, state):
        pass
    def more(self, d=1):
    	d=min(d,abs(len(self.dmxstate)-self.currentState))
	self.setState(self.state+d)
    def less(self, d=1):
    	d=min(d,self.currentState)
	self.setState(self.state-d)

if __name__ == '__main__':
    monitor = xbmc.Monitor()
    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds
        if monitor.waitForAbort(10):
            # Abort was requested while waiting. We should exit
            break
        xbmc.log("dmx %s" % time.time(), level=xbmc.LOGDEBUG)
    xbmc.log("dmx aborted %s" % time.time(), level=xbmc.LOGDEBUG)

