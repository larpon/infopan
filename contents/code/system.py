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

# System
class SysMonitor():
	def getUser(self):
		CMD = "whoami"
		return cmd(CMD)

	def getHostname(self):
		CMD = "hostname"
		return cmd(CMD)

	def getUptime(self):
		CMD = "uptime"
		out = cmd(CMD)
		match = re.compile('up\s+\d+(:\d+)*').search(out)
		t = out[match.start():match.end()]
		#t = re.match(, out, re.I).group()
		return re.sub('up\s+','',t)

	def getBits(self):
		CMD = "file /usr/bin/uptime | awk '{print $3}'"
		out = cmd(CMD)
		return out
