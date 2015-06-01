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

from utils import *

# Network
class NetMonitor:
	def __init__(self):
		self.initStat = self.getUsage()
		self.lastUpdate = self.getUsage()

	def getUsage(self):
		CMD = "ifconfig | grep -e 'eth\|wlan'"
		out = cmd(CMD)
		arr = out.split("\n")
		interfaceInfo = []
		for line in arr:
			line = line.strip()
			interface = re.match('eth|wlan', line, re.I).group()
			number = re.match('(eth|wlan)([0-9]+)', line, re.I).group(2)
			# Find MAC
			match = re.compile('([a-fA-F0-9]{2}[:]){5}[a-fA-F0-9]{2}').search(line)
			mac = line[match.start():match.end()]
			# Find IP
			ip = self.getLANIP(interface+number)
			nin = self.getIn(interface+number)
			nout = self.getOut(interface+number)
			if ip != "":
				interfaceInfo.append({ "interface" : interface, "number" : number, "mac" : mac, "ip" : ip, "in" : nin, "out" : nout })
		return interfaceInfo

	def getLANIP(self,interface):
		CMD = "ifconfig "+interface+" | grep inet | cut -f12 -d' ' | cut -f2 -d':'"
		return cmd(CMD)

	def getWANIP(self):
		CMD = "wget -q -O - checkip.dyndns.org | sed -e 's/.*Current IP Address: //' -e 's/<.*$//'"
		wanip = cmd(CMD)
		return wanip

	def getIn(self,interface):
		#CMD = "ifconfig "+interface+" | grep 'RX byte' | awk '{print $3 $4}'"
		#RX bytes
		CMD = "ifconfig "+interface+" | grep 'RX byte'"
		line = cmd(CMD)
		match = re.compile('RX bytes:[0-9]+ ').search(line)
		nin = int(re.sub('RX bytes:',"",line[match.start():match.end()]).strip())
		hin = bytesToHuman(nin)
		return { "bytes" : nin, "human" : hin }

	def getOut(self,interface):
		#TX bytes
		#CMD = "ifconfig "+interface+" | grep 'RX byte' | awk '{print $7 $8}'"
		CMD = "ifconfig "+interface+" | grep 'RX byte'"
		line = cmd(CMD)
		match = re.compile('TX bytes:[0-9]+ ').search(line)
		nout = int(re.sub('TX bytes:',"",line[match.start():match.end()]).strip())
		hout = bytesToHuman(nout)
		return { "bytes" : nout, "human" : hout }
	
	def calcUsage(self):
		old = self.lastUpdate
		new = self.getUsage()
		ret = self.lastUpdate
		i = 0
		while i<len(old):
			delta = new[i]["in"]["bytes"] - old[i]["in"]["bytes"]
			ret[i]["in"]["bytes"] = delta
			ret[i]["in"]["human"] = bytesToHuman(delta)
			delta = new[i]["out"]["bytes"] - old[i]["out"]["bytes"]
			ret[i]["out"]["bytes"] = delta
			ret[i]["out"]["human"] = bytesToHuman(delta)
			i+=1
		self.lastUpdate = new
		return ret
