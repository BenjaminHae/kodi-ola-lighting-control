#!/usr/bin/python
#Todo: logarithmisches anpassen
import array
from ola.ClientWrapper import ClientWrapper
import time
import threading

controlInstance = None
def WrapperCallback():
    controlInstance.SendDMXFrame()
def DMXSentCallback(state):
    controlInstance.DmxSent(state)
class DMXControl:
    cDMX=[]#current
    dDMX=[]#designated
    aTime=[]#time
    TICK_INTERVAL = 40
    universe = 0
    wrapper = None
    forceResend = False
    forceStop = False
    thread = None
    active = True

    #inits the DMX Control but does not send any data
    def __init__(self, channels=4, universe=0):
        global controlInstance
        controlInstance = self
        self.universe = universe
        self.cDMX = [0.0]*channels
        self.dDMX = [0]*channels
        self.aTime = [0]*channels
        self.wrapper = ClientWrapper()
        self.wrapper.AddEvent(self.TICK_INTERVAL, WrapperCallback)
        self.thread = threading.Thread(target=self.wrapper.Run)
        self.thread.start()
        #self.wrapper.Run()
            
    def stop(self):
        self.wrapper.Stop()
        self.forceStop=True
        self.thread.join()
    def GetNextData(self):
        DMX = self.cDMX[:]
        goal = self.dDMX
        Time = self.aTime
        for i in range(0,len(DMX)):
            if Time[i]>0:
                DMX[i] += (goal[i]-DMX[i])/Time[i]*self.TICK_INTERVAL
                Time[i] -= self.TICK_INTERVAL
                if Time[i]<=0:
                    DMX[i]=float(goal[i])
                if DMX[i]<0:
                    DMX[i]=0.0
                elif DMX[i]>255:
                    DMX[i]=255.0
        return DMX

    def isThereData(self):
        return any(v>0 for v in self.aTime)

    def DmxSent(self,state):# Careful is being called as a function not a method
      if not state.Succeeded():
        self.wrapper.Stop()

    def SendDMXFrame(self):
        # schdule a function call in 100ms
        # we do this first in case the frame computation takes a long time.   i
        if (not self.forceStop) and self.isThereData():
            self.wrapper.AddEvent(self.TICK_INTERVAL, WrapperCallback)
        else:
            self.active=False
        # compute frame here
        newDMX = self.GetNextData()
        if self.forceResend or any([int(newDMX[i])!=int(self.cDMX[i]) for i in range(0, len(newDMX))]):
            data = array.array('B',[int(v) for v in newDMX])
            # send
            self.wrapper.Client().SendDmx(self.universe, data, DMXSentCallback)#calling a method as a function
            self.forceResend = False
        self.cDMX = newDMX
    
    def setChannel(self, channel, value, fadeTime=0, multiple = False):
        if fadeTime<1:
            fadeTime=1
        self.dDMX[channel] = value
        self.aTime[channel] = fadeTime
        if (not self.active) and (not multiple):
            self.active=True
            self.wrapper.AddEvent(0, WrapperCallback)
    
    def setChannels(self, value, channels=None, time=None):
        if channels == None:
            channels=[i for i in range(0, len(value))]
        if time == None:
            time=[0]*len(value)
        if isinstance( time, ( int, long ) ) and len(value)>1:
            time=[time]*len(value)
        for i in range(0,len(value)):
            self.setChannel(channels[i], value[i], time[i], True)
        if (not self.active):
            self.active=True
            self.wrapper.AddEvent(0, WrapperCallback)
    def resendDMX(self):
        self.forceResend = True
        if not self.active:
            self.active=True
            self.wrapper.AddEvent(0,WrapperCallback)

class SimpleLight:
    states={'black':0,'dark':1,'night':2,'medium':3,'bright':4,'full':5}
    dmxstate=[[0,0,0,255,0],[60,6,6,255,0],[255,120,120,255,0],[255,150,150,255,0],[255,200,200,255,0],[255,255,255,255,0]]
    fadetime=1500
    currentState=0
    dmx = None
    def __init__(self):
        self.dmx = DMXControl(4,0)
    def setStateByName(self, state):
        self.setState(self.states[state]) 
    def setState(self, state):
        self.currentState=state
        self.dmx.setChannels(self.dmxstate[state], time = self.fadetime)
    def more(self, d=1):
        d=min(d,abs(len(self.dmxstate)-self.currentState))
        self.setState(self.state+d)
    def less(self, d=1):
        d=min(d,self.currentState)
        self.setState(self.state-d)
    def stop(self):
        self.dmx.stop()
