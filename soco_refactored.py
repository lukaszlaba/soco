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

#import xlrd
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

res_dict = {}


version = 'soco 0.1'

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
    return abs(maxabsrecord[col]), maxabsrecord


class MEMEB_RES():

    def __init__(self, id=None):
        self.number = None
        self.node = None
        #--
        self.res = []
        #--
        self.colLC = 1
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
        for record in self.res:
            My = record[self.colMy]
            Mz = record[self.colMz]
            record.append(round((My**2 + Mz**2)**0.5, 2))

    def calc_Vtot(self):
        for record in self.res:
            Fy = record[self.colFy]
            Fz = record[self.colFz]
            record.append(round((Fy**2 + Fz**2)**0.5, 2))

    def calc_bolt_maxtension(self):
        for record in self.res:
            My = abs(record[self.colMy])
            Mz = abs(record[self.colMz])
            Fx = record[self.colFx]
            fp = Fx / 4
            fm = -My / 0.2 / 2 - My / 0.2 / 2
            f = fp + fm
            record.append(round(f, 2))

    def calc_bolt_maxcompression(self):
        for record in self.res:
            My = abs(record[self.colMy])
            Mz = abs(record[self.colMz])
            Fx = record[self.colFx]
            fp = Fx / 4
            fm = My / 0.2 / 2 + My / 0.2 / 2
            f = fp + fm
            record.append(round(f, 2))

    def calc_bolt_maxshear(self):
        for record in self.res:
            Vtot = abs(record[self.colVtot])
            Mx = abs(record[self.colMx])
            fv = Vtot / 4
            fm = Mx / 2 / (0.1**2 + 0.2**2)**0.5
            f = fv + fm
            record.append(round(f, 2))

    #---
    @property
    def Fxmax(self):
        return find_max(self.res, self.colFx)
    @property
    def Fxmin(self):
        return find_min(self.res, self.colFx)


    @property
    def Fymax(self):
        return find_maxabs(self.res, self.colFy)
        
    @property
    def Fzmax(self):
        return find_maxabs(self.res, self.colFz)

    @property
    def Mxmax(self):
        return find_maxabs(self.res, self.colMx)

    @property
    def Mymax(self):
        return find_maxabs(self.res, self.colMy)

    @property
    def Mzmax(self):
        return find_maxabs(self.res, self.colMz)

    @property
    def Mzmax(self):
        return find_maxabs(self.res, self.colMz)
        
    @property
    def Mtotmax(self):
        return find_maxabs(self.res, self.colMtot)

    @property
    def Vtotmax(self):
        return find_maxabs(self.res, self.colVtot)

    @property
    def Bolttensionmax(self):
        return find_maxabs(self.res, self.colboltmaxtension)
        
    @property
    def Boltcompressionmax(self):
        return find_maxabs(self.res, self.colmaxboltcompression)

    @property
    def Boltshearmax(self):
        return find_maxabs(self.res, self.colmaxboltshear)     
        
    @property
    def Fxmax(self):
        return find_max(self.res, self.colFx)
    @property
    def Fxmin(self):
        return find_min(self.res, self.colFx)

    #---
    @property
    def Fxlist(self):
        return [i[self.colFx] for i in self.res]
    @property
    def Fylist(self):
        return [i[self.colFy] for i in self.res]
    @property
    def Fzlist(self):
        return [i[self.colFz] for i in self.res]
    @property
    def Mxlist(self):
        return [i[self.colMx] for i in self.res]
    @property
    def Mylist(self):
        return [i[self.colMy] for i in self.res]
    @property
    def Mzlist(self):
        return [i[self.colMz] for i in self.res]
    @property
    def Mtotlist(self):
        return [i[self.colMtot] for i in self.res]
    @property
    def Vtotlist(self):
        return [i[self.colVtot] for i in self.res]  
    @property
    def LClist(self):
        return [i[self.colLC] for i in self.res]
    @property
    def numberlist(self):
        return [self.number]*len(self.res)

class MAINWINDOW(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #--
        self.ui.pushButton_Report.clicked.connect(summary)
        #--
        self.ui.pushButton_Fx_My.clicked.connect(plot_Fx_My)
        self.ui.pushButton_Fx_Mz.clicked.connect(plot_Fx_Mz)
        self.ui.pushButton_Fx_Mtot.clicked.connect(plot_Fx_Mtot)
        self.ui.pushButton_My_Mz.clicked.connect(plot_My_Mz)
        self.ui.pushButton_Fy_Fz.clicked.connect(plot_Fy_Fz)
        self.ui.pushButton_Mx_Vtot.clicked.connect(plot_Mx_Vtot)
        #--
        self.ui.pushButton_Sort.clicked.connect(sort_serch_list)
        self.ui.pushButton_getMembers.clicked.connect(getMembers)
        self.ui.pushButton_makei.clicked.connect(makei)
        self.ui.pushButton_makej.clicked.connect(makej)
        self.ui.pushButton_makeij.clicked.connect(makeij)
        self.ui.pushButton_check.clicked.connect(check)
        #--
        self.ui.pushButton_clbResults.clicked.connect(clbResults)
        self.ui.pushButton_clbMembers.clicked.connect(clbMembers)
        self.ui.pushButton_clbNodes.clicked.connect(clbNodes)
        #--
        #--
        self.ui.pushButton_info.clicked.connect(info)
        self.ui.pushButton_print.clicked.connect(print_report)

def getMembers():
    mlist = list(res_dict.keys())
    mlist = [i.replace('i','') for i in mlist]
    mlist = [i.replace('j','') for i in mlist]
    
    mlist = list(dict.fromkeys(mlist))
    set_list(mlist)
    

def sort_serch_list():
    mlist = get_memberlist()
    mlist.sort()
    set_list(mlist)

def set_list(mlist):
    out_text = ''
    for i in mlist:
        out_text += i + '\n'
    myapp.ui.plainTextEdit_serch.clear()
    myapp.ui.plainTextEdit_serch.insertPlainText(out_text)
    
    
def makei():
    mlist = get_memberlist()
    mlist = [i.replace('i','') for i in mlist]
    mlist = [i.replace('j','') for i in mlist]
    mlist = list(dict.fromkeys(mlist))
    mlist = [i+'i' for i in mlist]
    set_list(mlist)

def makej():
    mlist = get_memberlist()
    mlist = [i.replace('i','') for i in mlist]
    mlist = [i.replace('j','') for i in mlist]
    mlist = list(dict.fromkeys(mlist))
    mlist = [i+'j' for i in mlist]
    set_list(mlist)
    
def makeij():
    mlist = get_memberlist()
    mlist = [i.replace('i','') for i in mlist]
    mlist = [i.replace('j','') for i in mlist]
    mlist = list(dict.fromkeys(mlist))
    outlist=[]
    for i in mlist:
        outlist.append(i+'i')
        outlist.append(i+'j')
    set_list(outlist)
    
    
def clbResults():
    from tkinter import Tk
    root = Tk()
    root.withdraw()
    #global data
    data = root.clipboard_get()
    # import testdata
    # data = testdata.data
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
        record = data[i]
        for j in range(3, 9): 
            record[j] = eval(record[j])

    for i in range(1, len(data)-1):
        record = data[i]
        record[1] = record[1].split()[0]
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
            memb_i = MEMEB_RES()
            memb_j = MEMEB_RES()
            curent_mem_number = record[0]
            memb_i.number = curent_mem_number + 'i'
            memb_j.number = curent_mem_number + 'j'
        #print('zapis')
        if end == -1:
            #memb.i = record[2]
            memb_i.res.append(record)
            memb_i.node = record[2]
        if end == 1:
            #memb.j = record[2]
            memb_j.res.append(record)
            memb_j.node = record[2]
        end = end * -1
        res_dict[memb_i.number] = memb_i
        res_dict[memb_j.number] = memb_j
    #--
    for key in res_dict:
        res_dict[key].calc_additional_forces()
    #---
    myapp.ui.textBrowser_output.setText('>>>> %s res point data loaded from %s <<<<'%(len(res_dict.keys()), ' model name '))
    set_title(info = ' model name ')

def clbMembers():
    from tkinter import Tk
    root = Tk()
    root.withdraw()
    data = root.clipboard_get()
    data = data.replace("\r", '')
    data =  data.split('\n')
    for i in range(len(data)):#--each parameter
        tmp = data[i].split('\t')
        data[i] = tmp
    mlist = [str(int(i[0])) for i in data]
    print(mlist)
    set_list(mlist)
    
def clbNodes():
    from tkinter import Tk
    root = Tk()
    root.withdraw()
    data = root.clipboard_get()
    data = data.replace("\r", '')
    data =  data.split('\n')
    for i in range(len(data)):#--each parameter
        tmp = data[i].split('\t')
        data[i] = tmp
    nlist = [str(int(i[0])) for i in data]
    print(nlist)
    mlist = get_memberlist()
    mlist = [i.replace('i','') for i in mlist]
    mlist = [i.replace('j','') for i in mlist]
    mlist = list(dict.fromkeys(mlist))
    outlist=[]
    for i in mlist:
        if i+'i' in res_dict.keys():
            if res_dict[i+'i'].node in nlist:
                outlist.append(i+'i')
        if i+'j' in res_dict.keys():
            if res_dict[i+'j'].node in nlist:
                outlist.append(i+'j')
    set_list(outlist)

def get_memberlist():
    text = myapp.ui.plainTextEdit_serch.toPlainText()
    memberlist = list(text.split("\n"))
    memberlist = list(dict.fromkeys(memberlist)) # delete duplicates
    while '' in memberlist:
        memberlist.remove('')
    memberlist = ["".join(i.rstrip().lstrip()) for i in memberlist] # delete spaces at start and end
    return memberlist

def get_force_table(filterlist=['1i', '1j']):
    rows = []
    rows.append(['Loc', 'Type', 'LC', 'Node', 'Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'])
    # 
    if filterlist:
        for i in filterlist:
            if i in res_dict.keys():
                res = res_dict[i]
                rows.append([str(res.number), 'Fxmax = '+str(res.Fxmax[0])] + res.Fxmax[1][1:9])
                rows.append([str(res.number), 'Fxmin = '+str(res.Fxmin[0])] + res.Fxmin[1][1:9])
                rows.append([str(res.number), 'Fymax = '+str(res.Fymax[0])] + res.Fymax[1][1:9])        
                rows.append([str(res.number), 'Fzmax = '+str(res.Fzmax[0])] + res.Fzmax[1][1:9]) 
                rows.append([str(res.number), 'Mxmax = '+str(res.Mxmax[0])] + res.Mxmax[1][1:9])    
                rows.append([str(res.number), 'Mymax = '+str(res.Mymax[0])] + res.Mymax[1][1:9])        
                rows.append([str(res.number), 'Mzmax = '+str(res.Mzmax[0])] + res.Mzmax[1][1:9])
                rows.append([str(res.number), 'Mtoimax = '+str(res.Mtotmax[0])] + res.Mtotmax[1][1:9])
                rows.append([str(res.number), 'Vtotmax = '+str(res.Vtotmax[0])] + res.Vtotmax[1][1:9])
                rows.append([str(res.number), 'Max bolt comp'] + res.Boltcompressionmax[1][1:9])
                rows.append([str(res.number), 'Max bolt tens'] + res.Bolttensionmax[1][1:9])
                rows.append([str(res.number), 'Max bolt shear'] + res.Boltshearmax[1][1:9])

            else:
                rows.append([i+'(!!)', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
            rows.append(['Loc', 'Type', 'LC', 'Node', 'Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'])
        rows = rows[:-1]
        return tabulate(rows, headers="firstrow", tablefmt="grid")
    else:
        return ''

def get_extreme_force_table(filterlist=['1i', '1j']):
    rows = []
    rows.append(['Loc', 'Type', 'LC', 'Node', 'Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'])
    # 
    if filterlist:
        res = res_dict[has_Fxmax(filterlist)]
        rows.append([str(res.number), 'Fxmax = '+str(res.Fxmax[0])] + res.Fxmax[1][1:9])
        
        res = res_dict[has_Fxmin(filterlist)]
        rows.append([str(res.number), 'Fxmin = '+str(res.Fxmin[0])] + res.Fxmin[1][1:9])
        
        res = res_dict[has_Fymax(filterlist)]
        rows.append([str(res.number), 'Fymax = '+str(res.Fymax[0])] + res.Fymax[1][1:9]) 
          
        res = res_dict[has_Fzmax(filterlist)]     
        rows.append([str(res.number), 'Fzmax = '+str(res.Fzmax[0])] + res.Fzmax[1][1:9]) 

        res = res_dict[has_Mxmax(filterlist)] 
        rows.append([str(res.number), 'Mxmax = '+str(res.Mxmax[0])] + res.Mxmax[1][1:9])
         
        res = res_dict[has_Mymax(filterlist)] 
        rows.append([str(res.number), 'Mymax = '+str(res.Mymax[0])] + res.Mymax[1][1:9])
        
        res = res_dict[has_Mzmax(filterlist)]        
        rows.append([str(res.number), 'Mzmax = '+str(res.Mzmax[0])] + res.Mzmax[1][1:9])
        
        res = res_dict[has_Mtotmax(filterlist)]
        rows.append([str(res.number), 'Mtotmax = '+str(res.Mtotmax[0])] + res.Mtotmax[1][1:9])
        
        res = res_dict[has_Vtotmax(filterlist)]
        rows.append([str(res.number), 'Vtotmax = '+str(res.Vtotmax[0])] + res.Vtotmax[1][1:9])
        
        res = res_dict[has_Boltcompressionmax(filterlist)]
        rows.append([str(res.number), 'Max bolt comp'] + res.Boltcompressionmax[1][1:9])
        
        res = res_dict[has_Bolttensionmax(filterlist)]
        rows.append([str(res.number), 'Max bolt tens'] + res.Bolttensionmax[1][1:9])
        
        res = res_dict[has_Boltshearmax(filterlist)]
        rows.append([str(res.number), 'Max bolt shear'] + res.Boltshearmax[1][1:9])
        
        return tabulate(rows, headers="firstrow", tablefmt="grid")
    else:
        return ''

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
    data = {i : res_dict[i].Fxmax[0] for i in where}
    return max(data, key=data.get)

def has_Fxmin(where):
    data = {i : res_dict[i].Fxmin[0] for i in where}
    return min(data, key=data.get)

def has_Fymax(where):
    data = {i : res_dict[i].Fymax[0] for i in where}
    return max(data, key=data.get)

def has_Fzmax(where):
    data = {i : res_dict[i].Fzmax[0] for i in where}
    return max(data, key=data.get)

def has_Mxmax(where):
    data = {i : res_dict[i].Mxmax[0] for i in where}
    return max(data, key=data.get)

def has_Mymax(where):
    data = {i : res_dict[i].Mymax[0] for i in where}
    return max(data, key=data.get)

def has_Mzmax(where):
    data = {i : res_dict[i].Mzmax[0] for i in where}
    return max(data, key=data.get)

def has_Mtotmax(where):
    data = {i : res_dict[i].Mtotmax[0] for i in where}
    return max(data, key=data.get)

def has_Vtotmax(where):
    data = {i : res_dict[i].Vtotmax[0] for i in where}
    return max(data, key=data.get)

def has_Bolttensionmax(where):
    data = {i : res_dict[i].Bolttensionmax[0] for i in where}
    return max(data, key=data.get)

def has_Boltcompressionmax(where):
    data = {i : res_dict[i].Boltcompressionmax[0] for i in where}
    return max(data, key=data.get)

def has_Boltshearmax(where):
    data = {i : res_dict[i].Boltshearmax[0] for i in where}
    return max(data, key=data.get)


def summary():
    if is_data_empty():
        check()
        return None
    if not is_data_ok():
        check()
        return None
    #------
    mlist = get_memberlist()
    report = 'Data source - ' + '...' + '\n'
    report += 'Results for  - ' + str(mlist)
    report += '\n\n'
    report += 'Force unit - [kN], Moment unit - [kNm]'
    report += '\n\n'
    
    if myapp.ui.checkBox_full.isChecked():
        report += 'STAAD format general table:\n'
        report += get_force_table(mlist) + '\n'
        report += '\n'

    report += 'Extreme cases list:\n'
    report += get_extreme_force_table(mlist) + '\n'
    report += '.........\n'
    

    if myapp.ui.checkBox_idea.isChecked():
        factor = float(myapp.ui.lineEdit_ideafactor.text())
        report += '\nIdea Statica format extreme cases table (with factor %s):\n'%factor
        report += '.........\n'
        # if myapp.ui.checkBox_upliftV2.isChecked():
        #     report += get_force_table_statica_format_uplift(local_reslist, factor) + '\n'
        # else:
        #     report += get_force_table_statica_format(local_reslist, factor) + '\n'
    # 
    # #print(report)
    myapp.ui.textBrowser_output.setText(report)

def plot_Fx_My():
    if is_data_empty():
        check()
        return None
    if not is_data_ok():
        check()
        return None
    #------
    mlist = get_memberlist()
    #-
    X=[]
    Y=[]
    annotations=[]
    for i in mlist:
        X += res_dict[i].Fxlist
        Y += [abs(j) for j in res_dict[i].Mylist]
        annotations += res_dict[i].numberlist
    #-
    plt.figure(figsize=(8,6))
    plt.scatter(X,Y,s=50,color="blue")
    #-
    if myapp.ui.checkBox_pltAnnot.isChecked():
        for i, label in enumerate(annotations):
            plt.text(X[i], Y[i],'   '+label, fontsize=7)
    plt.grid()
    #-
    plt.title("Fx-My", fontsize=15)
    plt.xlabel("Fx [kip]")
    plt.ylabel("My [kip-ft]")
    #-
    plt.show()

def plot_Fx_Mz():
    if is_data_empty():
        check()
        return None
    if not is_data_ok():
        check()
        return None
    #------
    mlist = get_memberlist()
    #-
    X=[]
    Y=[]
    annotations=[]
    for i in mlist:
        X += res_dict[i].Fxlist
        Y += [abs(j) for j in res_dict[i].Mzlist]
        annotations += res_dict[i].numberlist
    #-
    plt.figure(figsize=(8,6))
    plt.scatter(X,Y,s=50,color="blue")
    #-
    if myapp.ui.checkBox_pltAnnot.isChecked():
        for i, label in enumerate(annotations):
            plt.text(X[i], Y[i],'   '+label, fontsize=7)
    plt.grid()
    #-
    plt.title("Fx-Mz", fontsize=15)
    plt.xlabel("Fx [kip]")
    plt.ylabel("Mz [kip-ft]")
    #-
    plt.show()

def plot_Fx_Mtot():
    if is_data_empty():
        check()
        return None
    if not is_data_ok():
        check()
        return None
    #------
    mlist = get_memberlist()
    #-
    X=[]
    Y=[]
    annotations=[]
    for i in mlist:
        X += res_dict[i].Fxlist
        Y += res_dict[i].Mtotlist
        annotations += res_dict[i].numberlist
    #-
    plt.figure(figsize=(8,6))
    plt.scatter(X,Y,s=50,color="blue")
    #-
    if myapp.ui.checkBox_pltAnnot.isChecked():
        for i, label in enumerate(annotations):
            plt.text(X[i], Y[i],'   '+label, fontsize=7)
    plt.grid()
    #-
    plt.title("Fx-Mtot", fontsize=15)
    plt.xlabel("Fx [kip]")
    plt.ylabel("Mtot [kip-ft]")
    #-
    plt.show()

def plot_My_Mz():
    if is_data_empty():
        check()
        return None
    if not is_data_ok():
        check()
        return None
    #------
    mlist = get_memberlist()
    #-
    X=[]
    Y=[]
    annotations=[]
    for i in mlist:
        X += [abs(j) for j in res_dict[i].Mylist]
        Y += [abs(j) for j in res_dict[i].Mzlist]
        annotations += res_dict[i].numberlist
    #-
    plt.figure(figsize=(8,6))
    plt.scatter(X,Y,s=50,color="blue")
    #-
    if myapp.ui.checkBox_pltAnnot.isChecked():
        for i, label in enumerate(annotations):
            plt.text(X[i], Y[i],'   '+label, fontsize=7)
    plt.grid()
    #-
    plt.title("My-Mz", fontsize=15)
    plt.xlabel("My [kip-ft]")
    plt.ylabel("Mz [kip-ft]")
    #-
    plt.show()

def plot_Fy_Fz():
    if is_data_empty():
        check()
        return None
    if not is_data_ok():
        check()
        return None
    #------
    mlist = get_memberlist()
    #-
    X=[]
    Y=[]
    annotations=[]
    for i in mlist:
        X += [abs(j) for j in res_dict[i].Fylist]
        Y += [abs(j) for j in res_dict[i].Fzlist]
        annotations += res_dict[i].numberlist
    #-
    plt.figure(figsize=(8,6))
    plt.scatter(X,Y,s=50,color="blue")
    #-
    if myapp.ui.checkBox_pltAnnot.isChecked():
        for i, label in enumerate(annotations):
            plt.text(X[i], Y[i],'   '+label, fontsize=7)
    plt.grid()
    #-
    plt.title("Fy-Fz", fontsize=15)
    plt.xlabel("Fy [kip]")
    plt.ylabel("Fz [kip]")
    #-
    plt.show()

def plot_Mx_Vtot():
    if is_data_empty():
        check()
        return None
    if not is_data_ok():
        check()
        return None
    #------
    mlist = get_memberlist()
    #-
    X=[]
    Y=[]
    annotations=[]
    for i in mlist:
        X += [abs(j) for j in res_dict[i].Mxlist]
        Y += res_dict[i].Vtotlist
        annotations += res_dict[i].numberlist
    #-
    plt.figure(figsize=(8,6))
    plt.scatter(X,Y,s=50,color="blue")
    #-
    if myapp.ui.checkBox_pltAnnot.isChecked():
        for i, label in enumerate(annotations):
            plt.text(X[i], Y[i],'   '+label, fontsize=7)
    plt.grid()
    #-
    plt.title("Mx-Vtot", fontsize=15)
    plt.xlabel("Mx [kip]")
    plt.ylabel("Vtot [kip]")
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
        report += '!!! PROBLEM !!!! some data not found - please correct the list\n'
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

if __name__ == '__main__':
    # load_clipboard_data()
    # m1 = res_dict['1i']  
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