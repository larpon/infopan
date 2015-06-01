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


#import time
 
#TIMEFORMAT = "%m/%d/%y %H:%M:%S"
#INTERVAL = 2
 
#def getTimeList():
  #statFile = file("/proc/stat", "r")
  #timeList = statFile.readline().split(" ")[2:6]
  #statFile.close()
  #for i in range(len(timeList)) :
    #timeList[i] = int(timeList[i])
  #return timeList
 
#def deltaTime(interval) :
  #x = getTimeList()
  #time.sleep(interval)
  #y = getTimeList()
  #for i in range(len(x)) :
    #y[i] -= x[i]
  #return y

#if __name__ == "__main__" :
  #while True :
    #dt = deltaTime(INTERVAL)
    #timeStamp = time.strftime(TIMEFORMAT)
    #cpuPct = 100 - (dt[len(dt) - 1] * 100.00 / sum(dt))
    #print timeStamp + "\t" + str('%.4f' %cpuPct)


#The first line in /proc/stat says cpu and then has several numbers after it. The first 4 numbers are user, nice, system, and idle times
#(these values are simply the amount of time the cpu has spent in each since last boot).
#Should look something like this:
#cpu 3637881 11829 781587 33547506 219684 71147 256792 0
#(We're only concerned with the bolded values)
#To get the average system load over any given amount of time you read those four values into variable
#(for example, ill call them u1, n1, s1, and i1). Then when you're ready you read the values again into new variables, u2, n2, s2, and i2.
#Now your total usage time is equal to (u2-u1) + (n2 - n1) + (s2 - s1). And your total time overall is the usage time + (i2-i1).
#Take (100*usage)/total and you have your percent CPU Usage. :)

import commands
import re #RegEx





#def testrun(old):
	##print getCpuStat()
	##print calcCpuUsage(old,getCpuStat())
	#print calcNetInterfaceUsage(old,getNetInterfaces())

##System
#print getSysUser()+"@"+getSysHostname()

##Network
##print getNetLANIP()+"/"+getNetWANIP()+": In: "+getNetIn()+" Out: "+getNetOut()
#print getNetInterfaces()
##CPU
#print str(getCpuRealCores())+"("+str(getCpuCores())+")x"+getCpuModelName()

#old = getCpuStat()
#print old
#print calcCpuUsage(old,getCpuStat())

#old = getNetInterfaces()
#print calcNetInterfaceUsage(old,getNetInterfaces())
##old = getPerCPUStat()

#r = RepeatTimer(2.0, testrun, 3, [old])
#r.start()

#from subprocess import call
#cpu = call(["cat", "/proc/stat | grep cpu"])
#print cpu

#	m = re.search('(?<=abc)def', 'abcdef')
#	m.group(0)