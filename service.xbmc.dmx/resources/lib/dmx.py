#!/usr/bin/python
import array
from ola.ClientWrapper import ClientWrapper
import time

class DMXControl:
	cDMX=[]#current
	dDMX=[]#designated
	aTime=[]#time
	TICK_INTERVAL = 30
	universe = 0
	wrapper = None
	forceResend = False

	#inits the DMX Control but does not send any data
	def __init__(self, channels=4, universe=0):
		self.universe = universe
		self.cDMX = [0.0]*channels
		self.dDMX = [0]*channels
		self.aTime = [0]*channels
		self.wrapper = ClientWrapper()
		wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
		wrapper.Run()
	
	def stop(self):
		wrapper.Stop()

	def GetNextData(self):
		DMX = self.cDMX
		goal = self.dDMX
		Time = self.aTime
		for i in range(0,len(DMX)):
			if Time[i]>0:
				DMX[i] += (goal[i]-DMX[i])/Time[i]*self.TICK_INTERVAL
				Time[i] -= self.TICK_INTERVAL
				if Time[i]<=0:
					DMX[i]=goal[i]
				if DMX[i]<0:
					DMX[i]=0.0
				elif DMX[i]>255:
					DMX[i]=255.0
		return DMX

	def isThereData(self):
		return any(v>0 for v in self.aTime)

	def DmxSent(state):# Careful
	  if not state.Succeeded():
	    wrapper.Stop()

	def SendDMXFrame(self):
	  # schdule a function call in 100ms
	  # we do this first in case the frame computation takes a long time.	i
	  wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
	  
	  # compute frame here
	  newDMX = self.GetNextData()
	  if forceResend or any(int(newDMX[i])!=int(self.cDMX[i]) for i in range(0, len(newDMX))):
		  data = array.array('B',[int(v) for v in cDMX])
		  # send
		  wrapper.Client().SendDmx(universe, data, DmxSent)
		  forceResend = False
	  self.cDMX = newDMX
	
	def setChannel(self, channel, value, fadeTime=0):
	  if fadeTime<1:
	  	fadeTime=1
	  self.dDMX[channel] = value
	  self.aTime[channel] = fadeTime
	
	def setChannels(self, value, channels=None, time=None):
		if channels=None:
			channels=[i for i in range(0, len(value))]
		if time=None:
			time=[0]*len(value)
		for i in range(0,len(value)):
			self.setChannel(channels[i], value[i], time[i])
	
	def resendDMX(self):
		self.forceResend = True
