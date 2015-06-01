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

from PyQt4.QtGui import QWidget
from configForm_ui import Ui_Dialog

class ponConfig(QWidget,Ui_Dialog):
    '''
    classdocs
    '''


    def __init__(self,parent,defaultConfig = None):
        '''
        Constructor
        '''
        QWidget.__init__(self)
        self.parent = parent
        self.setupUi(self)
        if defaultConfig:
            self.txtCity.setText(defaultConfig['city'])
            self.txtCountry.setText(defaultConfig['country'])
            idx = self.cmbUnit.findText(defaultConfig['unit'])
            self.cmbUnit.setCurrentIndex(idx)
    
    def getLocation(self):
        strCity = str.strip(str(self.txtCity.text()))
        strCountry = str.strip(str(self.txtCountry.text()))
        return strCity + "," + strCountry
    
    def getCity(self):
        strCity = str.strip(str(self.txtCity.text()))
        return strCity
    
    def getCountry(self):
        strCountry = str.strip(str(self.txtCountry.text()))
        return strCountry
    
    def getUnit(self):
        strUnit = str.strip(str(self.cmbUnit.currentText()))
        return strUnit