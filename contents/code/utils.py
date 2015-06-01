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

import commands

def isInt(x):
	try: t = int(x)
	except: return False
	return True

def runCmd(s):
	return commands.getstatusoutput(s)

def cmd(s):
	return runCmd(s)[1].strip()

def bytesToHuman(b):
	b = float(b)
	if(b <= 1024):
		return str(b)+" B"
	if(b > 1024 and b < 1e6):
		return str(round(b/1024,2))+" KB"
	if(b >= 1e6 and b < 1e9):
		return str(round((b/1024)/1024,2))+" MB"
	if(b >= 1e9 and b < 1e12):
		return str(round(((b/1024)/1024)/1024,2))+" GB"
	if(b >= 1e12 and b < 1e15):
		return str(round((((b/1024)/1024)/1024)/1024,2))+" TB"
	if(b >= 1e15 and b < 1e18):
		return str(round(((((b/1024)/1024)/1024)/1024)/1024,2))+" PB"
	if(b >= 1e18):
		return str(round((((((b/1024)/1024)/1024)/1024)/1024)/1024,2))+" EB"
