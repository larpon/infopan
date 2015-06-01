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

# Memory
class MemMonitor():
	def getUsage(self):
		re_parser = re.compile(r'^(?P<key>\S*):\s*(?P<value>\d*)\s*kB' )
		result = dict()
		result_human = dict()
		for line in open('/proc/meminfo'):
			match = re_parser.match(line)
			if not match:
				continue # skip lines that don't parse
			key, value = match.groups(['key', 'value'])
			if(key == "MemTotal" or key == "MemFree" or key == "SwapTotal" or key == "SwapFree"):
				result_human[key] = bytesToHuman(int(value)*1024)
				result[key] = (int(value)*1024)
		result["MemUsed"] = result["MemTotal"] - result["MemFree"]
		result_human["MemUsed"] = bytesToHuman(result["MemUsed"])
		result["SwapUsed"] = result["SwapTotal"] - result["SwapFree"]
		result_human["SwapUsed"] = bytesToHuman(result["SwapUsed"])
		return { "bytes" : result, "human" : result_human }
