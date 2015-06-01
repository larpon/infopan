# -*- coding: utf-8 -*-
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

import re
# CPU monitoring
from utils import *

class CpuMonitor:
	def __init__(self):
		self.initStat = self.getUsage()
		self.lastUpdate = self.getUsage()

	def getVendor(self):
		CMD = "cat /proc/cpuinfo | grep -m 1 'model name' | sed -e 's/.*: //'"
		out = cmd(CMD)
		return re.sub("\s{2,}", " ", out)
		
	def getRealCores(self):
		CMD = "cat /proc/cpuinfo | grep -m 1 \"cpu cores\""
		out = cmd(CMD)
		cores = ''
		for char in out:
			if(isInt(char)):
				cores += char
		return int(cores)
		
	def getCores(self):
		CMD = "cat /proc/stat | grep cpu"
		out = cmd(CMD)
		arr = out.split("\n")
		arr.pop(0)
		return len(arr)

	def getUsage(self):
		CMD = "cat /proc/stat | grep cpu"
		out = cmd(CMD)
		arr = out.split("\n")
		arr.pop(0)
		i = 0
		cpuInfo = []
		for cpuLine in arr:
			cl = cpuLine.strip().split(" ")
			cpuInfo.append({ "user" : int(cl[1]),  "nice" : int(cl[2]), "system" : int(cl[3]), "idle" : int(cl[4]), "total" : int(int(cl[1])+int(cl[2])+int(cl[3])), "total%" : 0 })
		return cpuInfo

	def calcUsage(self):
		old = self.lastUpdate #self.initStat
		new = self.getUsage()
		cpuInfo = []
		i = 0
		while i<len(old):
			usage = (new[i]["user"]-old[i]["user"]) + (new[i]["nice"]-old[i]["nice"]) + (new[i]["system"]-old[i]["system"])
			#usage = (new[i]["total"]-old[i]["total"])
			total = usage + (new[i]["idle"]-old[i]["idle"])
			percent = 0
			if(total > 0):
				percent = (100*usage/total)
			cpuInfo.append(
				{
				"user" : new[i]["user"]-old[i]["user"],
				"nice" : new[i]["nice"]-old[i]["nice"],
				"system" : new[i]["system"]-old[i]["system"],
				"idle" : new[i]["idle"]-old[i]["idle"],
				"total" : new[i]["total"]-old[i]["total"],
				"total%" : percent
				}
				#Now your total usage time is equal to (u2-u1) + (n2 - n1) + (s2 - s1). And your total time overall is the usage time + (i2-i1).
				#Take (100*usage)/total and you have your percent CPU Usage. :)
			)
			i+=1
		self.lastUpdate = new
		return cpuInfo
