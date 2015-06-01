# -*- coding: utf-8 -*-
# main.py
#
#  Copyright 2015  Lars Pontoppidan <leverpostej@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  2.010-1301, USA.
#

#import kde and qt specific stuff
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
import os

# Our includes
from cpu import *
from network import *
from gpu import *
from system import *
from memory import *

import images_rc

#Plasmoid gained by inheritance
class InfoPan(plasmascript.Applet):
	#constructor
	def __init__(self,parent,args=None):
		plasmascript.Applet.__init__(self,parent)
		self.parent = parent
		
		self.cpumon = CpuMonitor()
		self.netmon = NetMonitor()
		self.gpumon = GpuMonitor()
		self.sysmon = SysMonitor()
		self.memmon = MemMonitor()
		self.prepare()


	#done once when initiating
	def init(self):
		self._image_prefix = ":/images/"

		self.cpuThread = QTimer()
		self.connect(self.cpuThread,SIGNAL("timeout()"),self.updateCpu)
		self.cpuThread.start(5000)

		self.netThread = QTimer()
		self.connect(self.netThread,SIGNAL("timeout()"),self.updateNet)
		self.netThread.start(1000)

		self.sysThread = QTimer()
		self.connect(self.sysThread,SIGNAL("timeout()"),self.updateSys)
		self.sysThread.start(60000)

		self.memThread = QTimer()
		self.connect(self.memThread,SIGNAL("timeout()"),self.updateMem)
		self.memThread.start(10000)

		#disable settings dialog
		self.setHasConfigurationInterface(False)
		#set size of Plasmoid
		self.resize(590, 195)
		#set aspect ratio mode
		self.setAspectRatioMode(Plasma.IgnoreAspectRatio)
		#set timer interval in ms (1000=1s)
		self.startTimer(1000)

	#done when timer is resetted
	def timerEvent(self, event):
		#call draw method
		self.update()

	#draw method
	def paintInterface(self, painter, option, rect):
		painter.save()

		#svg_current = Plasma.Svg(self)
		#curImgName = ":/images/monitor.svg"
		#svg_current.setImagePath(curImgName)
		#svg_current.resize(500,500)
		#svg_current.paint(painter,0, 0)

		# Image
		#svg1 = Plasma.Svg()
		#svg1.setImagePath(":/images/monitor.svg")
		#svg1.resize(150,150)
		#svg1.paint(painter,30, 50)
		
		textColor = Plasma.Theme.defaultTheme().color(Plasma.Theme.TextColor)
		bgColor = Plasma.Theme.defaultTheme().color(Plasma.Theme.BackgroundColor)
		textFont = Plasma.Theme.defaultTheme().font(Plasma.Theme.DefaultFont)
		fontPointSize = textFont.pointSize()
		
		rect.moveTo(20,0)
		painter.setPen(textColor)
		textFont.setPointSize(textFont.pointSize()+2)
		textFont.setBold(True)
		painter.setFont(textFont)
		painter.drawText(rect,Qt.AlignLeft,"System information")
		
		textFont.setPointSize(fontPointSize)
		textFont.setBold(False)
		painter.setFont(textFont)
		
		pixsize = painter.fontInfo().pixelSize()+2
		place = 25
		indent = 25
		
		
		txt = "SYS"
		rect.moveTo(indent,place)
		painter.setPen(Qt.darkRed)
		painter.drawText(rect,Qt.AlignLeft,txt)
		painter.setPen(textColor)
		txt = "\n\t\t"+self.systxt+" Up "+self.getSysUpdateTxt()+"\n"+"\n"
		painter.drawText(rect,Qt.AlignLeft,txt)
		
		txt = "CPU"
		place = place+(pixsize*3)
		rect.moveTo(indent,place)
		painter.setPen(Qt.darkRed)
		painter.drawText(rect,Qt.AlignLeft,txt)
		painter.setPen(textColor)
		txt = "\n\t\t"+self.cputxt+"\n"
		txt += "\t\t"+self.getCpuUpdateTxt()+"\n"+"\n"
		painter.drawText(rect,Qt.AlignLeft,txt)
		
		txt = "GPU"
		place = place+(pixsize*4)
		rect.moveTo(indent,place)
		painter.setPen(Qt.darkRed)
		painter.drawText(rect,Qt.AlignLeft,txt)
		painter.setPen(textColor)
		txt = "\n\t\t"+self.gputxt+"\n"+"\n"
		painter.drawText(rect,Qt.AlignLeft,txt)
		
		txt = "NET"
		place = place+(pixsize*3)
		rect.moveTo(indent,place)
		painter.setPen(Qt.darkRed)
		painter.drawText(rect,Qt.AlignLeft,txt)
		painter.setPen(textColor)
		txt = "\n\t\t"+self.nettxt+"\n"
		txt += "\t\t"+self.getNetUpdateTxt()+"\n"
		painter.drawText(rect,Qt.AlignLeft,txt)
		
		txt = "MEM"
		place = place+(pixsize*5)
		rect.moveTo(indent,place)
		painter.setPen(Qt.darkRed)
		painter.drawText(rect,Qt.AlignLeft,txt)
		painter.setPen(textColor)
		
		self.resize(340,place+70)
		txt = "\n\t\t"+self.getMemUpdateTxt()+"\n"
		painter.drawText(rect,Qt.AlignLeft,txt)

		painter.restore()

	def prepare(self):
		self.cputxt = ""
		self.nettxt = ""
		self.gputxt = ""
		self.systxt = ""
		self.cpustat = self.cpumon.calcUsage()
		self.netstat = self.netmon.calcUsage()
		self.sysstat = self.sysmon.getUptime()
		self.memstat = self.memmon.getUsage()
		
		#System
		self.systxt += self.sysmon.getUser()+"@"+self.sysmon.getHostname()

		#Network
		wanip = self.netmon.getWANIP()
		if wanip != '':
			self.nettxt += "WAN "+wanip

		#GPU
		self.gputxt += self.gpumon.getVendor()

		#CPU
		self.cputxt += str(self.cpumon.getRealCores())+"("+str(self.cpumon.getCores())+")x"+self.cpumon.getVendor()+" ("+self.sysmon.getBits()+")"
		
		# Mem
		#
	
	def getCpuUpdateTxt(self):
		txt = ""
		i=0
		for cpu in self.cpustat:
			#txt += "Cpu "+str(i)+": "+str(cpu["total%"])+"% "
			txt += str(cpu["total%"])+"% "
			i+=1
		return txt

	def getNetUpdateTxt(self):
		txt = ""
		i=0
		for iface in self.netstat:
			now = self.netmon.getUsage()
			if iface["ip"] != '':
				txt += "LAN "+iface["ip"]+" ("+iface["interface"]+iface["number"]+") "+iface["mac"]
				txt += "\n\t\t\t\t"+now[i]["in"]["human"]+" / "+now[i]["out"]["human"]
				txt += " "+iface["in"]["human"]+"/s"+" / "+iface["out"]["human"]+"/s"
				txt += "\n"
			i+=1
		return txt

	def getSysUpdateTxt(self):
		txt = ""
		txt += self.sysstat
		return txt

	def getMemUpdateTxt(self):
		txt = ""
		mem = self.memstat
		txt += "Real: Total "+mem["human"]["MemTotal"]+" Used "+mem["human"]["MemUsed"]+" Free "+mem["human"]["MemFree"]
		txt += "\n\t\tSwap: Total "+mem["human"]["SwapTotal"]+" Used "+mem["human"]["SwapUsed"]+" Free "+mem["human"]["SwapFree"]
		return txt

	def updateNet(self):
		self.netstat = self.netmon.calcUsage()
	def updateCpu(self):
		self.cpustat = self.cpumon.calcUsage()
	def updateSys(self):
		self.sysstat = self.sysmon.getUptime()
	def updateMem(self):
		self.memstat = self.memmon.getUsage()
	

def CreateApplet(parent):
	return InfoPan(parent)
