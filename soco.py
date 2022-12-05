'''
--------------------------------------------------------------------------
Copyright (C) 2021 Lukasz Laba <lukaszlaba@gmail.com>

This file is part of Gismo.

Gismo is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Gismo is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Gismo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------

'''


import os

import xlrd
from tabulate import tabulate

#import numpy as np
import matplotlib.pyplot as plt

import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtPrintSupport import QPrintDialog

from mainwindow_ui import Ui_MainWindow

opendir = os.path.dirname(__file__)#dir path for save and open
filename = None

res_dict = []


version = 'soco 0.1'

# class RESPOINT():#xxxxxxxxxxxxxx
# 
#     def __init__(self, id=None):
#         self.frame_number = None
#         self.station = None
#         self.id = id
#         self.size = None
#         #--
#         self.P_list = []
#         self.V2_list = []
#         self.V3_list = []
#         self.T_list = []
#         self.M2_list = []
#         self.M3_list = []
# 
#     @property
#     def Pmax(self):
#         return max(self.P_list)
#     @property
#     def Pmax_r(self):
#         return round(self.Pmax,1)
# 
#     @property
#     def Pmin(self):
#         return min(self.P_list)
#     @property
#     def Pmin_r(self):
#         return round(self.Pmin,1)
# 
#     @property
#     def V2(self):
#         return max([abs(i) for i in self.V2_list])
#     @property
#     def V2_r(self):
#         return round(self.V2,1)
# 
#     @property
#     def V3(self):
#         return max([abs(i) for i in self.V3_list])
#     @property
#     def V3_r(self):
#         return round(self.V3,1)
# 
#     @property
#     def T(self):
#         return max([abs(i) for i in self.T_list])
#     @property
#     def T_r(self):
#         return round(self.T,1)
# 
#     @property
#     def M2(self):
#         return max([abs(i) for i in self.M2_list])
#     @property
#     def M2_r(self):
#         return round(self.M2,1)
# 
#     @property
#     def M3(self):
#         return max([abs(i) for i in self.M3_list])
#     @property
#     def M3_r(self):
#         return round(self.M3,1)
# 
#     @property
#     def Vtot(self):
#         Vmax = (self.V2**2 + self.V3**2)**0.5
#         return Vmax
#     @property
#     def Vtot_r(self):
#         return round(self.Vtot,1)
# 
#     @property
#     def Mtot(self):
#         Mmax = (self.M2**2 + self.M3**2)**0.5
#         return Mmax
#     @property
#     def Mtot_r(self):
#         return round(self.Mtot,1)
# 
#     @property
#     def max_connection_tension(self):
#         fp = self.Pmax / 4
#         fm = self.M3 / 0.2 / 2
#         f = max(fp, 0) + fm
#         return f
#     @property
#     def max_connection_tension_r(self):
#         return round(self.max_connection_tension,1)
# 
#     @property
#     def max_connection_compresion(self):
#         fp = self.Pmin / 4
#         fm = - self.M3 / 0.2 / 2
#         f = min(fp, 0) + fm
#         return f
#     @property
#     def max_connection_compresion_r(self):
#         return round(self.max_connection_compresion,1)
# 
#     @property
#     def max_connection_shear(self):
#         fv = self.Vtot / 4
#         fm = self.T / 2 / (0.1**2 + 0.2**2)**0.5
#         f = fv + fm
#         return f
#     @property
#     def max_connection_shear_r(self):
#         return round(self.max_connection_shear,1)
#         
#     @property
#     def V2uplift(self):
#         if self.station == 'i' and max([i for i in self.V2_list])>=0:
#             return abs(max([i for i in self.V2_list]))
#         if self.station == 'j' and min([i for i in self.V2_list])<0:
#             return abs(min([i for i in self.V2_list]))
#         return 0.0
#     @property
#     def V2uplift_r(self):
#         return round(self.V2uplift,1)
#         
#     @property
#     def V2down(self):
#         if self.station == 'i' and min([i for i in self.V2_list])<=0:
#             return abs(min([i for i in self.V2_list]))
#         if self.station == 'j' and max([i for i in self.V2_list])>0:
#             return abs(max([i for i in self.V2_list]))
#         return 0.0
#     @property
#     def V2down_r(self):
#         return round(self.V2down,1)





def find_max(list=[[2,7,4], [43,3,-2]], col=2):
    maxrecord = list[0]
    for record in list:
        #print(record)
        if record[col] > maxrecord[col]:
            maxrecord = record
    return maxrecord[col], maxrecord

def find_min(list=[[2,7,4], [43,3,-2]], col=2):
    minrecord = list[0]
    for record in list:
        #print(record)
        if record[col] < minrecord[col]:
            minrecord = record
    return minrecord[col], minrecord

def find_maxabs(list=[[2,7,4], [43,3,-32]], col=2):
    maxabsrecord = list[0]
    for record in list:
        #print(record)
        if abs(record[col]) > abs(maxabsrecord[col]):
            maxabsrecord = record
    return maxabsrecord[col], maxabsrecord
        


class MEMEB_RES():

    def __init__(self, id=None):
        self.number = None
        self.i = None
        self.j = None
        #--
        self.res_i = []
        self.res_j = []
        #--
        self.colFx = 3
        self.colFy = 4
        self.colFz = 5
        self.colMx = 6
        self.colMy = 7
        self.colMz = 8
        self.colMtot = 9
        self.colVtot = 10
        self.colboltmaxtension = 11
        self.colmaxboltcompression = 12
        self.colmaxboltshear = 13
    
    def calc_additional_forces(self):
        self.calc_Mtot()
        self.calc_Vtot()
        self.calc_bolt_maxtension()
        self.calc_bolt_maxcompression()
        self.calc_bolt_maxshear()
    #---
    def calc_Mtot(self):
        for record in self.res_i:
            My = record[self.colMy]
            Mz = record[self.colMz]
            record.append(round((My**2 + Mz**2)**0.5, 2))
        for record in self.res_j:
            My = record[self.colMy]
            Mz = record[self.colMz]
            record.append(round((My**2 + Mz**2)**0.5, 2))

    def calc_Vtot(self):
        for record in self.res_i:
            Fy = record[self.colFy]
            Fz = record[self.colFz]
            record.append(round((Fy**2 + Fz**2)**0.5, 2))
        for record in self.res_j:
            Fy = record[self.colFy]
            Fz = record[self.colFz]
            record.append(round((Fy**2 + Fz**2)**0.5, 2))

    def calc_bolt_maxtension(self):
        for record in self.res_i:
            My = abs(record[self.colMy])
            Mz = abs(record[self.colMz])
            Fx = record[self.colFx]
            fp = Fx / 4
            fm = -My / 0.2 / 2 - My / 0.2 / 2
            f = fp + fm
            record.append(round(f, 2))
        for record in self.res_j:
            My = abs(record[self.colMy])
            Mz = abs(record[self.colMz])
            Fx = record[self.colFx]
            fp = Fx / 4
            fm = -My / 0.2 / 2 - My / 0.2 / 2
            f = fp + fm
            record.append(round(f, 2))

    def calc_bolt_maxcompression(self):
        for record in self.res_i:
            My = abs(record[self.colMy])
            Mz = abs(record[self.colMz])
            Fx = record[self.colFx]
            fp = Fx / 4
            fm = My / 0.2 / 2 + My / 0.2 / 2
            f = fp + fm
            record.append(round(f, 2))
        for record in self.res_j:
            My = abs(record[self.colMy])
            Mz = abs(record[self.colMz])
            Fx = record[self.colFx]
            fp = Fx / 4
            fm = My / 0.2 / 2 + My / 0.2 / 2
            f = fp + fm
            record.append(round(f, 2))

    def calc_bolt_maxshear(self):
        for record in self.res_i:
            Vtot = abs(record[self.colVtot])
            Mx = abs(record[self.colMx])
            fv = Vtot / 4
            fm = Mx / 2 / (0.1**2 + 0.2**2)**0.5
            f = fv + fm
            record.append(round(f, 2))
        for record in self.res_j:
            Vtot = abs(record[self.colVtot])
            Mx = abs(record[self.colMx])
            fv = Vtot / 4
            fm = Mx / 2 / (0.1**2 + 0.2**2)**0.5
            f = fv + fm
            record.append(round(f, 2))
    #---
    @property
    def Fximax(self):
        return find_max(self.res_i, self.colFx)
    @property
    def Fximin(self):
        return find_min(self.res_i, self.colFx)
    @property
    def Fxjmax(self):
        return find_max(self.res_j, self.colFx)
    @property
    def Fxjmin(self):
        return find_min(self.res_j, self.colFx)

    @property
    def Fyimax(self):
        return find_maxabs(self.res_i, self.colFy)
    @property
    def Fyjmax(self):
        return find_maxabs(self.res_j, self.colFy)
        
    @property
    def Fzimax(self):
        return find_maxabs(self.res_i, self.colFz)
    @property
    def Fzjmax(self):
        return find_maxabs(self.res_j, self.colFz)

    @property
    def Mximax(self):
        return find_maxabs(self.res_i, self.colMx)
    @property
    def Mxjmax(self):
        return find_maxabs(self.res_j, self.colMx)

    @property
    def Myimax(self):
        return find_maxabs(self.res_i, self.colMy)
    @property
    def Myjmax(self):
        return find_maxabs(self.res_j, self.colMy)

    @property
    def Mzimax(self):
        return find_maxabs(self.res_i, self.colMz)
    @property
    def Mzjmax(self):
        return find_maxabs(self.res_j, self.colMz)

    @property
    def Mzimax(self):
        return find_maxabs(self.res_i, self.colMz)
    @property
    def Mzjmax(self):
        return find_maxabs(self.res_j, self.colMz)
        
    @property
    def Mtotimax(self):
        return find_maxabs(self.res_i, self.colMtot)
    @property
    def Mtotjmax(self):
        return find_maxabs(self.res_j, self.colMtot)

    @property
    def Vtotimax(self):
        return find_maxabs(self.res_i, self.colVtot)
    @property
    def Vtotjmax(self):
        return find_maxabs(self.res_j, self.colVtot)

    @property
    def Bolttensionimax(self):
        return find_maxabs(self.res_i, self.colboltmaxtension)
    @property
    def Bolttensionjmax(self):
        return find_maxabs(self.res_j, self.colboltmaxtension)
        
    @property
    def Boltcompressionimax(self):
        return find_maxabs(self.res_i, self.colmaxboltcompression)
    @property
    def Boltcompressionjmax(self):
        return find_maxabs(self.res_j, self.colmaxboltcompression)

    @property
    def Boltshearimax(self):
        return find_maxabs(self.res_i, self.colmaxboltshear)
    @property
    def Boltshearjmax(self):
        return find_maxabs(self.res_j, self.colmaxboltshear)
    
    @property
    def report_i(self):
        record =  []
        #--
        record.append([str(self.number) + 'i', 'Fximax = '+str(self.Fximax[0])] + self.Fximax[1][1:9])
        record.append([str(self.number) + 'i', 'Fximin = '+str(self.Fximin[0])] + self.Fximin[1][1:9])
        record.append([str(self.number) + 'i', 'Fyimax = '+str(self.Fyimax[0])] + self.Fximax[1][1:9])        
        record.append([str(self.number) + 'i', 'Fzimax = '+str(self.Fzimax[0])] + self.Fzimax[1][1:9])   
        record.append([str(self.number) + 'i', 'Myimax = '+str(self.Myimax[0])] + self.Mximax[1][1:9])        
        record.append([str(self.number) + 'i', 'Mzimax = '+str(self.Mzimax[0])] + self.Mzimax[1][1:9])
        record.append([str(self.number) + 'i', 'Mtotimax = '+str(self.Mtotimax[0])] + self.Mtotimax[1][1:9])
        record.append([str(self.number) + 'i', 'Vtotimax = '+str(self.Vtotimax[0])] + self.Vtotimax[1][1:9])
        record.append([str(self.number) + 'i', 'Max bolt comp'] + self.Boltcompressionimax[1][1:9])
        record.append([str(self.number) + 'i', 'Max bolt tens'] + self.Bolttensionimax[1][1:9])
        record.append([str(self.number) + 'i', 'Max bolt shear'] + self.Boltshearimax[1][1:9])
        return record
    
    @property
    def report_j(self):
        record =  []
        #--
        record.append([str(self.number) + 'j', 'Fxjmax = '+str(self.Fxjmax[0])] + self.Fxjmax[1][1:9])
        record.append([str(self.number) + 'j', 'Fxjmin = '+str(self.Fxjmin[0])] + self.Fxjmin[1][1:9])
        record.append([str(self.number) + 'j', 'Fyjmax = '+str(self.Fyjmax[0])] + self.Fxjmax[1][1:9])        
        record.append([str(self.number) + 'j', 'Fzjmax = '+str(self.Fzjmax[0])] + self.Fzjmax[1][1:9])   
        record.append([str(self.number) + 'j', 'Myjmax = '+str(self.Myjmax[0])] + self.Mxjmax[1][1:9])        
        record.append([str(self.number) + 'j', 'Mzjmax = '+str(self.Mzjmax[0])] + self.Mzjmax[1][1:9])
        record.append([str(self.number) + 'j', 'Mtotjmax = '+str(self.Mtotjmax[0])] + self.Mtotjmax[1][1:9])
        record.append([str(self.number) + 'j', 'Vtotjmax = '+str(self.Vtotjmax[0])] + self.Vtotjmax[1][1:9])
        record.append([str(self.number) + 'j', 'Max bolt comp'] + self.Boltcompressionjmax[1][1:9])
        record.append([str(self.number) + 'j', 'Max bolt tens'] + self.Bolttensionjmax[1][1:9])
        record.append([str(self.number) + 'j', 'Max bolt shear'] + self.Boltshearjmax[1][1:9])
        return record

class MAINWINDOW(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(summary)
        self.ui.pushButton_P_M3.clicked.connect(plot_P_M3)
        self.ui.pushButton_P_M2.clicked.connect(plot_P_M2)
        self.ui.pushButton_M3_M2.clicked.connect(plot_M3_M2)
        self.ui.pushButton_V3_V2.clicked.connect(plot_V3_V2)
        self.ui.pushButton_T_Vtot.clicked.connect(plot_T_Vtot)
        self.ui.pushButton_info.clicked.connect(info)
        self.ui.pushButton_print.clicked.connect(print_report)
        self.ui.pushButton_check.clicked.connect(check)
        self.ui.actionLoadXLS.triggered.connect(load_clipboard_data)
        self.ui.pushButton_Find.clicked.connect(find)
        self.ui.pushButton_Sort.clicked.connect(sort_serch_list)
        
memb = MEMEB_RES()   

def load_clipboard_data():
    from tkinter import Tk
    root = Tk()
    root.withdraw()
    global data
    #data = root.clipboard_get()
    data ='''Beam	L/C	Node	Fx kip	Fy kip	Fz kip	Mx kip-ft	My kip-ft	Mz kip-ft
1	1001 1.4D (N-S)	1	0	18.355	18.355	18.355	18.355	-10
		2	0	18.356	18.356	18.356	18.356	-0.008
	1002 1.2D+1.6L (N-S)	1	0	-89	31.613	31.613	31.613	0
		2	0	31.615	31.615	31.615	31.615	-0.013
	1003 1.4D (E-W)	1	22	18.355	18.355	18.355	18.355	0
		2	33	18.356	18.356	18.356	18.356	-0.008
	1004 1.2D+1.6L (E-W)	1	-4	31.613	31.613	31.613	31.613	0
		2	-2	31.615	31.615	31.615	31.615	-0.013
2	1001 1.4D (N-S)	2	0	20.237	20.237	20.237	20.237	0.008
		3	0	20.237	20.237	20.237	20.237	-0.007
	1002 1.2D+1.6L (N-S)	2	0	34.856	34.856	34.856	34.856	0.013
		3	0	34.855	34.855	34.855	34.855	-0.011
	1003 1.4D (E-W)	2	22	20.237	20.237	20.237	20.237	0.008
		3	33	20.237	20.237	20.237	20.237	-0.007
	1004 1.2D+1.6L (E-W)	2	-4	34.856	34.856	34.856	34.856	0.013
		3	-2	34.855	34.855	34.855	34.855	-0.011
3	1001 1.4D (N-S)	3	0	18.356	18.356	18.356	18.356	0.007
		4	0	18.355	18.355	18.355	18.355	0
	1002 1.2D+1.6L (N-S)	3	0	31.615	31.615	31.615	31.615	0.011
		4	0	31.613	31.613	31.613	31.613	0
	1003 1.4D (E-W)	3	22	18.356	18.356	18.356	18.356	0.007
		4	33	18.355	18.355	18.355	18.355	0
	1004 1.2D+1.6L (E-W)	3	-4	31.615	31.615	31.615	31.615	0.011
		4	-2	31.613	31.613	31.613	31.613	0
4	1001 1.4D (N-S)	5	0	18.754	18.754	18.754	18.754	0
		2	0	-18.561	-18.561	-18.561	-18.561	85.515
	1002 1.2D+1.6L (N-S)	5	0	32.14	32.14	32.14	32.14	0
		2	0	-31.975	-31.975	-31.975	-31.975	146.931
	1003 1.4D (E-W)	5	22	18.754	18.754	18.754	18.754	0
		2	33	-18.561	-18.561	-18.561	-18.561	85.515
	1004 1.2D+1.6L (E-W)	5	-4	32.14	32.14	32.14	32.14	0
		2	-2	-31.975	-31.975	-31.975	-31.975	146.931
5	1001 1.4D (N-S)	2	0	-20.032	-20.032	-20.032	-20.032	-85.515
		7	0	20.211	20.211	20.211	20.211	0
	1002 1.2D+1.6L (N-S)	2	0	-34.495	-34.495	-34.495	-34.495	-146.931
		7	0	34.649	34.649	34.649	34.649	0
	1003 1.4D (E-W)	2	22	-20.032	-20.032	-20.032	-20.032	-85.515
		7	33	20.211	20.211	20.211	20.211	0
	1004 1.2D+1.6L (E-W)	2	-4	-34.495	-34.495	-34.495	-34.495	-146.931
		7	-2	34.649	34.649	34.649	34.649	0
6	1001 1.4D (N-S)	6	0	18.754	18.754	18.754	18.754	0
		3	0	-18.561	-18.561	-18.561	-18.561	85.515
	1002 1.2D+1.6L (N-S)	6	0	32.14	32.14	32.14	32.14	0
		3	0	-31.975	-31.975	-31.975	-31.975	146.93
	1003 1.4D (E-W)	6	22	18.754	18.754	18.754	18.754	0
		3	33	-18.561	-18.561	-18.561	-18.561	85.515
	1004 1.2D+1.6L (E-W)	6	-4	32.14	32.14	32.14	32.14	0
		3	-2	-31.975	-31.975	-31.975	-31.975	146.93
7	1001 1.4D (N-S)	3	0	-20.032	-20.032	-20.032	-20.032	-85.515
		8	0	20.21	20.21	20.21	20.21	0
	1002 1.2D+1.6L (N-S)	3	0	-34.495	-34.495	-34.495	-34.495	-146.93
		8	0	34.648	34.648	34.648	34.648	0
	1003 1.4D (E-W)	3	22	-20.032	-20.032	-20.032	-20.032	-85.515
		8	33	20.21	20.21	20.21	20.21	0
	1004 1.2D+1.6L (E-W)	3	-4	-34.495	-34.495	-34.495	-34.495	-146.93
		8	-2	34.648	34.648	34.648	34.648	0
'''
    data = data.replace("\r", '')
    data =  data.split('\n')
    for i in range(len(data)):#--each parameter
        tmp = data[i].split('\t')
        data[i] = tmp
    #--
    for i in range(1, len(data)-1):
        #print(i)
        if data[i][1] == '':
            data[i][1]=data[i-1][1]
    #--
    for i in range(1, len(data)-1):
        #print(i)
        record = data[i]
        for j in range(3, 9): 
            record[j] = eval(record[j])
    #--
    global res_dict
    res_dict = {}
    memb = None
    end = -1
    for i in range(1, len(data)-1):
        #print('------')
        record = data[i]
        #print(record)
        if record[0] != '':
            #print ('new-------')
            memb = MEMEB_RES()
            curent_mem_number = record[0]
            memb.number = curent_mem_number
        #print('zapis')
        if end == -1:
            memb.i = record[2]
            memb.res_i.append(record)
        if end == 1:
            memb.j = record[2]
            memb.res_j.append(record)
        end = end * -1
        res_dict[curent_mem_number] = memb
    
    for key in res_dict:
        res_dict[key].calc_additional_forces()
    
        
# def load_sap_data():#xxxxxxxxxxxxxx
#     global opendir
#     global filename
#     #----asking for filename
#     filename = QtWidgets.QFileDialog.getOpenFileName(   caption = 'Open ssmdata file',
#                                                     directory = opendir,
#                                                     filter = "xls' (*.xls)")[0]
#     print(filename)
# 
#     filename = str(filename)
#     if not filename == '': opendir = os.path.dirname(filename)
# 
#     global res_dict
#     global NUMBER
#     print(filename)
#     book = xlrd.open_workbook(filename)
#     sh = book.sheet_by_index(0)
#     NUMBER = sh.col_values(0)
#     
#     while NUMBER[-1] == '':
#         NUMBER.pop(-1)
#     
#     P = sh.col_values(5)[3:len(NUMBER)]
#     V2 = sh.col_values(6)[3:len(NUMBER)]
#     V3 = sh.col_values(7)[3:len(NUMBER)]
#     T = sh.col_values(8)[3:len(NUMBER)]
#     M2 = sh.col_values(9)[3:len(NUMBER)]
#     M3 = sh.col_values(10)[3:len(NUMBER)]
#     station = sh.col_values(14)[3:len(NUMBER)]
#     size = sh.col_values(15)[3:len(NUMBER)]
#     NUMBER = NUMBER[3:]
#     for i in range(len(NUMBER)):
#         try:
#             NUMBER[i] = str(int(NUMBER[i]))
#         except:
#             pass
#     
#     #loading data
# 
#     respointid = [str(i) + str(j) for i,j in zip(NUMBER, station) if j in ['i', 'j']]
# 
#     respointid = list(dict.fromkeys(respointid))
# 
#     res_dict = {}
# 
#     #init main dist
#     for i in respointid:
#         res_dict[i] = RESPOINT(i)
# 
#     #load data to main dist
#     print(len(NUMBER))
#     print(len(station))
#     for i in range(len(NUMBER)):
#         this_id = str(NUMBER[i]) + str(station[i])
#         if this_id in res_dict.keys():
#             this_respoint = res_dict[this_id]
#             this_respoint.frame_number = NUMBER[i]
#             this_respoint.station = station[i]
#             this_respoint.size = size[i]
#             this_respoint.P_list.append(P[i])
#             this_respoint.V2_list.append(V2[i])
#             this_respoint.V3_list.append(V3[i])
#             this_respoint.T_list.append(T[i])
#             this_respoint.M2_list.append(M2[i])
#             this_respoint.M3_list.append(M3[i])
# 
#     myapp.ui.textBrowser_output.setText('>>>> %s res point data loaded from %s <<<<'%(len(res_dict.keys()), os.path.basename(filename)))
# 
#     set_title(info = ' - ' + os.path.basename(filename))


def get_memberlist():
    text = myapp.ui.plainTextEdit_serch.toPlainText()
    memberlist = list(text.split("\n"))
    memberlist = list(dict.fromkeys(memberlist)) # delete duplicates
    while '' in memberlist:
        memberlist.remove('')
    memberlist = ["".join(i.rstrip().lstrip()) for i in memberlist] # delete spaces at start and end
    return memberlist

def get_force_table(filterlist=['1i', '1j']):
    rep_dict={}
    for key in res_dict:
        rep_dict[res_dict[key].number+'i'] = res_dict[key].report_i
        rep_dict[res_dict[key].number+'j'] = res_dict[key].report_j
    #print(rep_dict) 
    
    
    rows = []
    rows.append(['Loc', 'Type', 'LC', 'Node', 'Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'])
    # 
    if filterlist:
        for i in filterlist:
            if i in rep_dict.keys():
                res = rep_dict[i]
                for n in res:
                    rows.append(n)
            else:
                rows.append([i+'(!!)', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
            rows.append(['Loc', 'Type', 'LC', 'Node', 'Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'])
        return tabulate(rows, headers="firstrow", tablefmt="grid")
    else:
        return ''

# def get_force_table_uplift(filterlist=None):#xxxxxxxxxxxxxx
#     rows = []
#     rows.append(['FrameEnd', 'Pmax', 'Pmin', 'V2up', 'V2down', 'V3', 'T', 'M2', 'M3', 'Size'])
# 
#     if filterlist:
#         for i in filterlist:
#             if i in res_dict.keys():
#                 res = res_dict[i]
#                 rows.append([i, res.Pmax_r, res.Pmin_r, res.V2uplift_r, res.V2down_r,  res.V3_r, res.T_r, res.M2_r, res.M3_r, res.size])
#             else:
#                 rows.append([i+'(!!)', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
#         return tabulate(rows, headers="firstrow", tablefmt="grid")
#     else:
#         return ''

# def get_force_table_statica_format_uplift(filterlist=None, factor=1.0):#xxxxxxxxxxxxxx
#     report = ''
#     report += 'N\tVy\tVz\tMx\tMy\tMz\n'
# 
#     if filterlist:
#         for i in filterlist:
#             if i in res_dict.keys():
#                 res = res_dict[i]
#                 if res.Pmax_r != res.Pmin_r:
#                     if res.V2uplift_r != 0:
#                         report += str(round(res.Pmax_r*factor, 1))+'\t'+str(round(res.V3_r*factor, 1))+'\t'+str(round(res.V2uplift_r*factor, 1))+'\t'+str(round(res.T_r*factor, 1))+'\t'+str(round(-res.M3_r*factor, 1))+'\t'+str(round(res.M2_r*factor, 1))+'\n'
#                     if res.V2down_r != 0:
#                         report += str(round(res.Pmax_r*factor, 1))+'\t'+str(round(res.V3_r*factor, 1))+'\t'+str(round(-res.V2down_r*factor, 1))+'\t'+str(round(res.T_r*factor, 1))+'\t'+str(round(res.M3_r*factor, 1))+'\t'+str(round(res.M2_r*factor, 1))+'\n'
#                     if res.V2_r == 0:
#                         report += str(round(res.Pmax_r*factor, 1))+'\t'+str(round(res.V3_r*factor, 1))+'\t'+str(round(res.V2_r*factor, 1))+'\t'+str(round(res.T_r*factor, 1))+'\t'+str(round(-res.M3_r*factor, 1))+'\t'+str(round(res.M2_r*factor, 1))+'\n'
#                         
#                     if res.V2uplift_r != 0:
#                         report += str(round(res.Pmin_r*factor, 1))+'\t'+str(round(res.V3_r*factor, 1))+'\t'+str(round(res.V2uplift_r*factor, 1))+'\t'+str(round(res.T_r*factor, 1))+'\t'+str(round(-res.M3_r*factor, 1))+'\t'+str(round(res.M2_r*factor, 1))+'\n'
#                     if res.V2down_r != 0:
#                         report += str(round(res.Pmin_r*factor, 1))+'\t'+str(round(res.V3_r*factor, 1))+'\t'+str(round(-res.V2down_r*factor, 1))+'\t'+str(round(res.T_r*factor, 1))+'\t'+str(round(res.M3_r*factor, 1))+'\t'+str(round(res.M2_r*factor, 1))+'\n'
#                     if res.V2_r == 0:
#                         report += str(round(res.Pmin_r*factor, 1))+'\t'+str(round(res.V3_r*factor, 1))+'\t'+str(round(res.V2_r*factor, 1))+'\t'+str(round(res.T_r*factor, 1))+'\t'+str(round(-res.M3_r*factor, 1))+'\t'+str(round(res.M2_r*factor, 1))+'\n'
#                 else:
#                     if res.V2uplift_r != 0:
#                         report += str(round(res.Pmax_r*factor, 1))+'\t'+str(round(res.V3_r*factor, 1))+'\t'+str(round(res.V2uplift_r*factor, 1))+'\t'+str(round(res.T_r*factor, 1))+'\t'+str(round(-res.M3_r*factor, 1))+'\t'+str(round(res.M2_r*factor, 1))+'\n'
#                     if res.V2down_r != 0:
#                         report += str(round(res.Pmax_r*factor, 1))+'\t'+str(round(res.V3_r*factor, 1))+'\t'+str(round(-res.V2down_r*factor, 1))+'\t'+str(round(res.T_r*factor, 1))+'\t'+str(round(res.M3_r*factor, 1))+'\t'+str(round(res.M2_r*factor, 1))+'\n'
#                     if res.V2_r == 0:
#                         report += str(round(res.Pmax_r*factor, 1))+'\t'+str(round(res.V3_r*factor, 1))+'\t'+str(round(res.V2_r*factor, 1))+'\t'+str(round(res.T_r*factor, 1))+'\t'+str(round(-res.M3_r*factor, 1))+'\t'+str(round(res.M2_r*factor, 1))+'\n'                    
#             else:
#                 report += 'NoData/n'
#         return report
#     else:
#         return ''

def get_force_table_statica_format(filterlist=None, factor=1.0):
    report = ''
    report += 'N\tVy\tVz\tMx\tMy\tMz\n'

    if filterlist:
        for i in filterlist:
            if i in res_dict.keys():
                res = res_dict[i]
                if res.Pmax_r != res.Pmin_r:
                    report += str(round(res.Pmax_r*factor, 1))+'\t'+str(round(res.V3_r*factor, 1))+'\t'+str(round(-res.V2_r*factor, 1))+'\t'+str(round(res.T_r*factor, 1))+'\t'+str(round(res.M3_r*factor, 1))+'\t'+str(round(res.M2_r*factor, 1))+'\n'
                    report += str(round(res.Pmin_r*factor, 1))+'\t'+str(round(res.V3_r*factor, 1))+'\t'+str(round(-res.V2_r*factor, 1))+'\t'+str(round(res.T_r*factor, 1))+'\t'+str(round(res.M3_r*factor, 1))+'\t'+str(round(res.M2_r*factor, 1))+'\n'
                else:
                    report += str(round(res.Pmax_r*factor, 1))+'\t'+str(round(res.V3_r*factor, 1))+'\t'+str(round(-res.V2_r*factor, 1))+'\t'+str(round(res.T_r*factor, 1))+'\t'+str(round(res.M3_r*factor, 1))+'\t'+str(round(res.M2_r*factor, 1))+'\n'                    
            else:
                report += 'NoData/n'
        return report
    else:
        return ''

    





def has_Fxmax(where):
    tmp_dict={}
    for key in res_dict:
        tmp_dict[res_dict[key].number+'i'] = res_dict[key].Fximax[0]
        tmp_dict[res_dict[key].number+'j'] = res_dict[key].Fxjmax[0]
    data = {i : tmp_dict[i] for i in where}
    loc = max(data, key=data.get)
    return loc

def has_Fxmin(where):
    tmp_dict={}
    for key in res_dict:
        tmp_dict[res_dict[key].number+'i'] = res_dict[key].Fximin[0]
        tmp_dict[res_dict[key].number+'j'] = res_dict[key].Fxjmin[0]
    data = {i : tmp_dict[i] for i in where}
    loc = max(data, key=data.get)
    return loc

def has_Fymax(where):
    tmp_dict={}
    for key in res_dict:
        tmp_dict[res_dict[key].number+'i'] = res_dict[key].Fyimax[0]
        tmp_dict[res_dict[key].number+'j'] = res_dict[key].Fyjmax[0]
    data = {i : tmp_dict[i] for i in where}
    loc = max(data, key=data.get)
    return loc

def has_Fzmax(where):
    tmp_dict={}
    for key in res_dict:
        tmp_dict[res_dict[key].number+'i'] = res_dict[key].Fzimax[0]
        tmp_dict[res_dict[key].number+'j'] = res_dict[key].Fzjmax[0]
    data = {i : tmp_dict[i] for i in where}
    loc = max(data, key=data.get)
    return loc

def has_Mxmax(where):
    tmp_dict={}
    for key in res_dict:
        tmp_dict[res_dict[key].number+'i'] = res_dict[key].Mximax[0]
        tmp_dict[res_dict[key].number+'j'] = res_dict[key].Mxjmax[0]
    data = {i : tmp_dict[i] for i in where}
    loc = max(data, key=data.get)
    return loc

def has_Mymax(where):
    tmp_dict={}
    for key in res_dict:
        tmp_dict[res_dict[key].number+'i'] = res_dict[key].Myimax[0]
        tmp_dict[res_dict[key].number+'j'] = res_dict[key].Myjmax[0]
    data = {i : tmp_dict[i] for i in where}
    loc = max(data, key=data.get)
    return loc, tmp_dict[loc]

def has_Mtotmax(where):
    tmp_dict={}
    for key in res_dict:
        tmp_dict[res_dict[key].number+'i'] = res_dict[key].Mtotimax[0]
        tmp_dict[res_dict[key].number+'j'] = res_dict[key].Mtotjmax[0]
    data = {i : tmp_dict[i] for i in where}
    loc = max(data, key=data.get)
    return loc

def has_Vtotmax(where):
    tmp_dict={}
    for key in res_dict:
        tmp_dict[res_dict[key].number+'i'] = res_dict[key].Vtotimax[0]
        tmp_dict[res_dict[key].number+'j'] = res_dict[key].Vtotjmax[0]
    data = {i : tmp_dict[i] for i in where}
    loc = max(data, key=data.get)
    return loc

def has_Bolttensionmax(where):
    tmp_dict={}
    for key in res_dict:
        tmp_dict[res_dict[key].number+'i'] = res_dict[key].Bolttensionimax[0]
        tmp_dict[res_dict[key].number+'j'] = res_dict[key].Bolttensionjmax[0]
    data = {i : tmp_dict[i] for i in where}
    loc = max(data, key=data.get)
    return loc

def has_Boltcompressionmax(where):
    tmp_dict={}
    for key in res_dict:
        tmp_dict[res_dict[key].number+'i'] = res_dict[key].Boltcompressionimax[0]
        tmp_dict[res_dict[key].number+'j'] = res_dict[key].Boltcompressionjmax[0]
    data = {i : tmp_dict[i] for i in where}
    loc = max(data, key=data.get)
    return loc

def has_Boltshearmax(where):
    tmp_dict={}
    for key in res_dict:
        tmp_dict[res_dict[key].number+'i'] = res_dict[key].Boltshearimax[0]
        tmp_dict[res_dict[key].number+'j'] = res_dict[key].Boltshearjmax[0]
    data = {i : tmp_dict[i] for i in where}
    loc = max(data, key=data.get)
    return loc


def summary():
    # if is_data_empty():
    #     check()
    #     return None
    # if not is_data_ok():
    #     check()
    #     return None
    #------
    mlist = get_memberlist()
    report = 'Data source - ' + '...' + '\n'
    report += 'Results for  - ' + str(mlist)
    report += '\n\n'
    report += 'Force unit - [kN], Moment unit - [kNm]'
    report += '\n\n'

    report += 'SAP format general table:\n'
    
    report += get_force_table(mlist) + '\n'
    report += '\n'

    report += 'Extreme cases list:\n'
    report += '.........\n'
    

    if myapp.ui.checkBox_idea.isChecked():
        # factor = float(myapp.ui.lineEdit_ideafactor.text())
        report += '\nIdea Statica format extreme cases table (with factor %s):\n'%factor
        report += '.........\n'
        # if myapp.ui.checkBox_upliftV2.isChecked():
        #     report += get_force_table_statica_format_uplift(local_reslist, factor) + '\n'
        # else:
        #     report += get_force_table_statica_format(local_reslist, factor) + '\n'
    # 
    # #print(report)
    myapp.ui.textBrowser_output.setText(report)

def plot_P_M3():
    if is_data_empty():
        check()
        return None
    if not is_data_ok():
        check()
        return None
    #------
    mlist = get_memberlist()
    #-
    X=[res_dict[i].Pmin for i in mlist]
    Y=[res_dict[i].M3 for i in mlist]
    annotations=mlist

    X+=[res_dict[i].Pmax for i in mlist]
    Y+=[res_dict[i].M3 for i in mlist]
    annotations+=mlist

    #-
    plt.figure(figsize=(8,6))
    plt.scatter(X,Y,s=50,color="blue")
    #-
    for i, label in enumerate(annotations):
        plt.text(X[i], Y[i],'   '+label, fontsize=7)
    plt.grid()
    #-
    plt.title("P-M3", fontsize=15)
    plt.xlabel("P [kN]")
    plt.ylabel("M3 [kNm]")
    #-
    plt.show()

def plot_P_M2():
    if is_data_empty():
        check()
        return None
    if not is_data_ok():
        check()
        return None
    #------
    mlist = get_memberlist()
    #-
    X=[res_dict[i].Pmin for i in mlist]
    Y=[res_dict[i].M2 for i in mlist]
    annotations=mlist

    X+=[res_dict[i].Pmax for i in mlist]
    Y+=[res_dict[i].M2 for i in mlist]
    annotations+=mlist

    #-
    plt.figure(figsize=(8,6))
    plt.scatter(X,Y,s=50,color="blue")
    #-
    for i, label in enumerate(annotations):
        plt.text(X[i], Y[i],'   '+label, fontsize=7)
    plt.grid()
    #-
    plt.title("P-M2", fontsize=15)
    plt.xlabel("P [kN]")
    plt.ylabel("M2 [kNm]")
    #-
    plt.show()

def plot_M3_M2():
    if is_data_empty():
        check()
        return None
    if not is_data_ok():
        check()
        return None
    #------
    mlist = get_memberlist()
    #-
    X=[res_dict[i].M3 for i in mlist]
    Y=[res_dict[i].M2 for i in mlist]
    annotations=mlist
    #-
    plt.figure(figsize=(8,6))
    plt.scatter(X,Y,s=50,color="blue")
    #-
    for i, label in enumerate(annotations):
        plt.text(X[i], Y[i], '   '+label, fontsize=7)
    plt.grid()
    #-
    plt.title("M3-M2", fontsize=15)
    plt.xlabel("M3 [kNm]")
    plt.ylabel("M2 [kNm]")
    #-
    plt.show()

def plot_V3_V2():
    if is_data_empty():
        check()
        return None
    if not is_data_ok():
        check()
        return None
    #------
    mlist = get_memberlist()
    #-
    X=[res_dict[i].V3 for i in mlist]
    Y=[res_dict[i].V2 for i in mlist]
    annotations=mlist
    #-
    plt.figure(figsize=(8,6))
    plt.scatter(X,Y,s=50,color="blue")
    #-
    for i, label in enumerate(annotations):
        plt.text(X[i], Y[i],'   '+label, fontsize=7)
    plt.grid()
    #-
    plt.title("V3-V2", fontsize=15)
    plt.xlabel("V3 [kN]")
    plt.ylabel("V2[kN]")
    #-
    plt.show()

def plot_T_Vtot():
    if is_data_empty():
        check()
        return None
    if not is_data_ok():
        check()
        return None
    #------
    mlist = get_memberlist()
    #-
    X=[res_dict[i].Vtot for i in mlist]
    Y=[res_dict[i].T for i in mlist]
    annotations=mlist
    #-
    plt.figure(figsize=(8,6))
    plt.scatter(X,Y,s=50,color="blue")
    #-
    for i, label in enumerate(annotations):
        plt.text(X[i], Y[i],'   '+label, fontsize=7)
    plt.grid()
    #-
    plt.title("Vtot-T", fontsize=15)
    plt.xlabel("Vtot [kN]")
    plt.ylabel("T [kN]")
    #-
    plt.show()

def print_report():
    if print_dialog.exec_() == QtWidgets.QDialog.Accepted:
        myapp.ui.textBrowser_output.document().print_(print_dialog.printer())

def check():
    report = ''
    if is_data_empty():
        report += '!!! Search list is empty -add some items !!!'
        myapp.ui.textBrowser_output.setText(report)
        return None

    if is_data_ok():
        report += 'All data found' + '\n'
    else:
        report += '!!! PROBLEM !!!! some data not found - please correct the list'
    report += '---------------------------------------------------------------------' + '\n'

    for i in get_memberlist():
        if i in res_dict.keys():
            report += str(i) + ' - ok\n'
        else:
            report += str(i) + ' - !!!!!!NO DATA FOUND!!!!!!!<<<<<<<<<<<<<<<<<<<<<<\n'
    myapp.ui.textBrowser_output.setText(report)

def is_data_ok():
    if list(set(get_memberlist())-set(res_dict.keys())):
        return False
    else:
        return True

def is_data_empty():
    if get_memberlist():
        return False
    else:
        return True

def set_title(info=''):
    myapp.setWindowTitle(version + info)



def info():
    about = '''
-------------Licence-------------
Gismo is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

Gismo is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Gismo; if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA.

Copyright (C) 2021 Lukasz Laba (e-mail : lukaszlaba@gmail.com)
'''
    myapp.ui.textBrowser_output.setText(about)



def find():#xxxxxxxxxxxxxx

    if not res_dict:
        myapp.ui.textBrowser_output.setText('!!! No data loaded!!!')
        return None
    
    myapp.ui.plainTextEdit_serch.clear()
    
    section = myapp.ui.lineEdit_section.text()
    
    rM2 = myapp.ui.comboBox_M2.currentIndex()
    rM3 = myapp.ui.comboBox_M3.currentIndex()
    rT = myapp.ui.comboBox_T.currentIndex()
    rP = myapp.ui.comboBox_P.currentIndex()
    rV2 = myapp.ui.comboBox_V2.currentIndex()
    rV3 = myapp.ui.comboBox_V3.currentIndex()
    
    print(section, rM2, rM3, rT, rP, rV2, rV3)
    
    if section :
        s_list = [i for i in res_dict.keys() if res_dict[i].size==section]
    else:
        s_list = res_dict.keys() 
        

    if rM2 != 1:
        if rM2 == 2:
            s_list = list(set(s_list) & set(    [i for i in res_dict.keys() if res_dict[i].M2<0.001]  )  )
        if rM2 == 0:
            s_list = list(set(s_list) & set(    [i for i in res_dict.keys() if res_dict[i].M2>0.001]  )  )

    if rM3 != 1:
        if rM3 == 2:
            s_list = list(set(s_list) & set(    [i for i in res_dict.keys() if res_dict[i].M3<0.001]  )  )
        if rM3 == 0:
            s_list = list(set(s_list) & set(    [i for i in res_dict.keys() if res_dict[i].M3>0.001]  )  )

    if rT != 1:
        if rT == 2:
            s_list = list(set(s_list) & set(    [i for i in res_dict.keys() if res_dict[i].T<0.001]  )  )
        if rT == 0:
            s_list = list(set(s_list) & set(    [i for i in res_dict.keys() if res_dict[i].T>0.001]  )  )

    if rP != 1:       
        if rP == 2:
            s_list = list(    set(s_list)         & set(      [        i for i in res_dict.keys() if max(    abs(res_dict[i].Pmax), abs(res_dict[i].Pmin)    )<0.001     ]      )          )
        if rP == 0:
            s_list = list(    set(s_list)         & set(      [        i for i in res_dict.keys() if max(    abs(res_dict[i].Pmax), abs(res_dict[i].Pmin)    )>0.001     ]      )          )

    if rV2 != 1:
        if rV2 == 2:
            s_list = list(set(s_list) & set(    [i for i in res_dict.keys() if res_dict[i].V2<0.001]  )  )
        if rV2 == 0:
            s_list = list(set(s_list) & set(    [i for i in res_dict.keys() if res_dict[i].V2>0.001]  )  )

    if rV3 != 1:
        if rV3 == 2:
            s_list = list(set(s_list) & set(    [i for i in res_dict.keys() if res_dict[i].V3<0.001]  )  )
        if rV3 == 0:
            s_list = list(set(s_list) & set(    [i for i in res_dict.keys() if res_dict[i].V3>0.001]  )  )






    out_text = ''
    for i in s_list:
        out_text += i + '\n'

    myapp.ui.plainTextEdit_serch.clear()
    myapp.ui.plainTextEdit_serch.insertPlainText(out_text)
    myapp.ui.textBrowser_output.setText('')
    if not out_text:
        myapp.ui.textBrowser_output.setText('!!! Nothing found !!!')



def sort_serch_list():
    mlist = get_memberlist()
    mlist.sort()
    out_text = ''
    for i in mlist:
        out_text += i + '\n'
    myapp.ui.plainTextEdit_serch.clear()
    myapp.ui.plainTextEdit_serch.insertPlainText(out_text)
    



if __name__ == '__main__':
    load_clipboard_data()
    m1 = res_dict['1']  
    app = QtWidgets.QApplication(sys.argv)
    myapp = MAINWINDOW()
    print_dialog = QPrintDialog()
    set_title()
    myapp.ui.textBrowser_output.setText('Welcome in gismo SAP tool! Load data and fill input list to get report.')
    myapp.ui.plainTextEdit_serch.clear()
    myapp.setWindowIcon(QtGui.QIcon('app.ico'))
    myapp.show()
    sys.exit(app.exec_())


'''
command used to frozening with pyinstaller
pyinstaller --onefile --noconsole --icon=app.ico ..\gismo.py
'''