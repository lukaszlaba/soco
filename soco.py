'''
--------------------------------------------------------------------------
Copyright (C) 2022 Lukasz Laba <lukaszlaba@gmail.com>

This file is part of soco.

Soco is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Soco is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Soco; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------

'''

import os
import sys

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtPrintSupport import QPrintDialog
from tabulate import tabulate
import matplotlib.pyplot as plt

from mainwindow_ui import Ui_MainWindow
from member_respoint import member_respoint

res_dict = {}
unit_force = '[]'
unit_moment = '[]'

version = 'soco 0.0.2'

class MAINWINDOW(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #--
        self.ui.pushButton_Report.clicked.connect(show_report)
        #--
        self.ui.pushButton_Fx_My.clicked.connect(plot_Fx_My)
        self.ui.pushButton_Fx_Mz.clicked.connect(plot_Fx_Mz)
        self.ui.pushButton_Fx_Mtot.clicked.connect(plot_Fx_Mtot)
        self.ui.pushButton_My_Mz.clicked.connect(plot_Mz_My)
        self.ui.pushButton_Fy_Fz.clicked.connect(plot_Fz_Fy)
        self.ui.pushButton_Mx_Vtot.clicked.connect(plot_Mx_Vtot)
        #--
        self.ui.pushButton_Sort.clicked.connect(sort_memberlist)
        self.ui.pushButton_getMembers.clicked.connect(load_memberlist_from_results)
        self.ui.pushButton_makei.clicked.connect(makei)
        self.ui.pushButton_makej.clicked.connect(makej)
        self.ui.pushButton_makeij.clicked.connect(makeij)
        self.ui.pushButton_check.clicked.connect(check_memberlist)
        #--
        self.ui.pushButton_clbResults.clicked.connect(clbResults)
        self.ui.pushButton_clbMembers.clicked.connect(clbMembers)
        self.ui.pushButton_clbNodes.clicked.connect(clbNodes)
        #--
        #--
        self.ui.pushButton_info.clicked.connect(info)
        self.ui.pushButton_print.clicked.connect(print_report)

def clbResults():
    # from tkinter import Tk
    # root = Tk()
    # root.withdraw()
    #data = root.clipboard_get()
    import testdata
    data = testdata.data
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
            record[j] = eval(record[j].replace(',', '.'))

    for i in range(1, len(data)-1):
        record = data[i]
        record[1] = record[1].split()[0]
    #--geting units
    global unit_force
    global unit_moment
    unit_force = '[' + data[0][3].split()[1] + ']'
    unit_moment = '[' + data[0][6].split()[1] + ']'
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
            memb_i = member_respoint()
            memb_j = member_respoint()
            curent_mem_number = record[0]
            memb_i.number = curent_mem_number + 'i'
            memb_j.number = curent_mem_number + 'j'
        #print('zapis')
        if end == -1:
            #memb.i = record[2]
            memb_i.res.append(record)
            memb_i.node = record[2]
        #transform to internal force values instead of end forces
        if end == 1:
            record[3] = -record[3] # Fx sign update at the member end
            record[4] = -record[4] # Fy sign update at the member end
            record[5] = -record[6] # Fz sign update at the member end
            record[6] = -record[6] # Mx sign update at the member end
            record[7] = -record[7] # My sign update at the member end
            record[8] = -record[8] # Mz sign update at the member end
            memb_j.res.append(record)
            memb_j.node = record[2]
        end = end * -1
        res_dict[memb_i.number] = memb_i
        res_dict[memb_j.number] = memb_j
    #--
    for key in res_dict:
        res_dict[key].unit_force = unit_force
        res_dict[key].unit_moment = unit_moment
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
    set_memberlist(mlist)
    
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
    set_memberlist(outlist)

#-----------------------------------------------------------

def makei():
    mlist = get_memberlist()
    mlist = [i.replace('i','') for i in mlist]
    mlist = [i.replace('j','') for i in mlist]
    mlist = list(dict.fromkeys(mlist))
    mlist = [i+'i' for i in mlist]
    set_memberlist(mlist)

def makej():
    mlist = get_memberlist()
    mlist = [i.replace('i','') for i in mlist]
    mlist = [i.replace('j','') for i in mlist]
    mlist = list(dict.fromkeys(mlist))
    mlist = [i+'j' for i in mlist]
    set_memberlist(mlist)
    
def makeij():
    mlist = get_memberlist()
    mlist = [i.replace('i','') for i in mlist]
    mlist = [i.replace('j','') for i in mlist]
    mlist = list(dict.fromkeys(mlist))
    outlist=[]
    for i in mlist:
        outlist.append(i+'i')
        outlist.append(i+'j')
    set_memberlist(outlist)

def get_memberlist():
    text = myapp.ui.plainTextEdit_serch.toPlainText()
    memberlist = list(text.split("\n"))
    memberlist = list(dict.fromkeys(memberlist)) # delete duplicates
    while '' in memberlist:
        memberlist.remove('')
    memberlist = ["".join(i.rstrip().lstrip()) for i in memberlist] # delete spaces at start and end
    return memberlist

def set_memberlist(mlist):
    out_text = ''
    for i in mlist:
        out_text += i + '\n'
    myapp.ui.plainTextEdit_serch.clear()
    myapp.ui.plainTextEdit_serch.insertPlainText(out_text)

def sort_memberlist():
    mlist = get_memberlist()
    mlist.sort()
    set_memberlist(mlist)

def check_memberlist():
    report = ''
    if is_memberlist_empty():
        report += '!!! Search list is empty -add some items !!!'
        myapp.ui.textBrowser_output.setText(report)
        return None

    if data_for_memberlist_exist():
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

def is_memberlist_empty():
    if get_memberlist():
        return False
    else:
        return True

def data_for_memberlist_exist():
    if list(set(get_memberlist())-set(res_dict.keys())):
        return False
    else:
        return True

def load_memberlist_from_results():
    mlist = list(res_dict.keys())
    mlist = [i.replace('i','') for i in mlist]
    mlist = [i.replace('j','') for i in mlist]
    mlist = list(dict.fromkeys(mlist))
    set_memberlist(mlist)

#-----------------------------------------------------------
    
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

#-----------------------------------------------------------

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
                if res.Boltcompressionmax[0] != 0:
                    rows.append([str(res.number), 'Max conn comp'] + res.Boltcompressionmax[1][1:9])
                if res.Bolttensionmax[0] != 0:
                    rows.append([str(res.number), 'Max bolt tens'] + res.Bolttensionmax[1][1:9])
                if res.Boltshearmax[0] != 0:
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
        if res.Boltcompressionmax[0] != 0:
            rows.append([str(res.number), 'Max conn comp'] + res.Boltcompressionmax[1][1:9])
        
        res = res_dict[has_Bolttensionmax(filterlist)]
        if res.Bolttensionmax[0] != 0:
            rows.append([str(res.number), 'Max bolt tens'] + res.Bolttensionmax[1][1:9])
        
        res = res_dict[has_Boltshearmax(filterlist)]
        if res.Boltshearmax[0] != 0:
            rows.append([str(res.number), 'Max bolt shear'] + res.Boltshearmax[1][1:9])
        
        return tabulate(rows, headers="firstrow", tablefmt="grid")
    else:
        return ''

# def get_force_table_statica_format(filterlist=None, factor=1.0):
#     report = ''
#     report += 'N\tVy\tVz\tMx\tMy\tMz\n'
# 
#     if filterlist:
#         for i in filterlist:
#             if i in res_dict.keys():
#                 res = res_dict[i]
#                 if res.Pmax_r != res.Pmin_r:
#                     report += str(round(res.Pmax_r*factor, 1))+'\t'+str(round(res.V3_r*factor, 1))+'\t'+str(round(-res.V2_r*factor, 1))+'\t'+str(round(res.T_r*factor, 1))+'\t'+str(round(res.M3_r*factor, 1))+'\t'+str(round(res.M2_r*factor, 1))+'\n'
#                     report += str(round(res.Pmin_r*factor, 1))+'\t'+str(round(res.V3_r*factor, 1))+'\t'+str(round(-res.V2_r*factor, 1))+'\t'+str(round(res.T_r*factor, 1))+'\t'+str(round(res.M3_r*factor, 1))+'\t'+str(round(res.M2_r*factor, 1))+'\n'
#                 else:
#                     report += str(round(res.Pmax_r*factor, 1))+'\t'+str(round(res.V3_r*factor, 1))+'\t'+str(round(-res.V2_r*factor, 1))+'\t'+str(round(res.T_r*factor, 1))+'\t'+str(round(res.M3_r*factor, 1))+'\t'+str(round(res.M2_r*factor, 1))+'\n'                    
#             else:
#                 report += 'NoData/n'
#         return report
#     else:
#         return ''


def show_report():
    if is_memberlist_empty():
        check_memberlist()
        return None
    if not data_for_memberlist_exist():
        check_memberlist()
        return None
    #------
    mlist = get_memberlist()
    report = ''
    sourcefile = myapp.ui.lineEdit_staadname.text()
    if sourcefile:
        report += 'Data source - ' + sourcefile + '\n'
    report += 'Results for  - ' + str(mlist)
    report += '\n\n'
    report += 'Fx Fy Fz Mx My Mz are Staad format member intenal forces\n'
    report += 'Force unit - %s, Moment unit - %s'%(unit_force, unit_moment)
    report += '\n\n'
    
    if myapp.ui.checkBox_full.isChecked():
        report += 'STAAD format general table:\n'
        report += get_force_table(mlist) + '\n'
        report += '\n'

    report += 'Extreme cases list:\n'
    report += get_extreme_force_table(mlist) + '\n'
    report += '.........\n'
    #--
    # if myapp.ui.checkBox_idea.isChecked():
    #     factor = float(myapp.ui.lineEdit_ideafactor.text())
    #     report += '\nIdea Statica format extreme cases table (with factor %s):\n'%factor
    #     report += '.........\n'
    #--
    myapp.ui.textBrowser_output.setText(report)

#-----------------------------------------------------------

def plot_Fx_My():
    if is_memberlist_empty():
        check_memberlist()
        return None
    if not data_for_memberlist_exist():
        check_memberlist()
        return None
    #------
    mlist = get_memberlist()
    #-
    X=[]
    Y=[]
    annotations=[]
    for i in mlist:
        X += res_dict[i].Fxlist
        Y += res_dict[i].Mylist
        annotations += [res_dict[i].numberlist[j] + ' LC' + res_dict[i].LClist[j] for j in range(0, len(res_dict[i].numberlist))]
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
    plt.xlabel("Fx " + unit_force)
    plt.ylabel("My " + unit_moment)
    #-
    plt.show()

def plot_Fx_Mz():
    if is_memberlist_empty():
        check_memberlist()
        return None
    if not data_for_memberlist_exist():
        check_memberlist()
        return None
    #------
    mlist = get_memberlist()
    #-
    X=[]
    Y=[]
    annotations=[]
    for i in mlist:
        X += res_dict[i].Fxlist
        Y += res_dict[i].Mzlist
        annotations += [res_dict[i].numberlist[j] + ' LC' + res_dict[i].LClist[j] for j in range(0, len(res_dict[i].numberlist))]
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
    plt.xlabel("Fx " + unit_force)
    plt.ylabel("Mz " + unit_moment)
    #-
    plt.show()

def plot_Fx_Mtot():
    if is_memberlist_empty():
        check_memberlist()
        return None
    if not data_for_memberlist_exist():
        check_memberlist()
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
        annotations += [res_dict[i].numberlist[j] + ' LC' + res_dict[i].LClist[j] for j in range(0, len(res_dict[i].numberlist))]
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
    plt.xlabel("Fx " + unit_force)
    plt.ylabel("Mtot " + unit_moment)
    #-
    plt.show()

def plot_Mz_My():
    if is_memberlist_empty():
        check_memberlist()
        return None
    if not data_for_memberlist_exist():
        check_memberlist()
        return None
    #------
    mlist = get_memberlist()
    #-
    X=[]
    Y=[]
    annotations=[]
    for i in mlist:
        X += res_dict[i].Mzlist
        Y += res_dict[i].Mylist
        annotations += [res_dict[i].numberlist[j] + ' LC' + res_dict[i].LClist[j] for j in range(0, len(res_dict[i].numberlist))]
    #-
    plt.figure(figsize=(8,6))
    plt.scatter(X,Y,s=50,color="blue")
    #-
    if myapp.ui.checkBox_pltAnnot.isChecked():
        for i, label in enumerate(annotations):
            plt.text(X[i], Y[i],'   '+label, fontsize=7)
    plt.grid()
    #-
    plt.title("Mz-My", fontsize=15)
    plt.xlabel("Mz " + unit_moment)
    plt.ylabel("My " + unit_moment)
    #-
    plt.show()

def plot_Fz_Fy():
    if is_memberlist_empty():
        check_memberlist()
        return None
    if not data_for_memberlist_exist():
        check_memberlist()
        return None
    #------
    mlist = get_memberlist()
    #-
    X=[]
    Y=[]
    annotations=[]
    for i in mlist:
        X += res_dict[i].Fzlist
        Y += res_dict[i].Fylist
        annotations += [res_dict[i].numberlist[j] + ' LC' + res_dict[i].LClist[j] for j in range(0, len(res_dict[i].numberlist))]
    #-make it abs
    X = [abs(i) for i in X]
    Y = [abs(i) for i in Y]
    #-
    plt.figure(figsize=(8,6))
    plt.scatter(X,Y,s=50,color="blue")
    #-
    if myapp.ui.checkBox_pltAnnot.isChecked():
        for i, label in enumerate(annotations):
            plt.text(X[i], Y[i],'   '+label, fontsize=7)
    plt.grid()
    #-
    plt.title("|Fy|-|Fz|", fontsize=15)
    plt.xlabel("|Fz| " + unit_force)
    plt.ylabel("|Fy| " + unit_force)
    #-
    plt.show()

def plot_Mx_Vtot():
    if is_memberlist_empty():
        check_memberlist()
        return None
    if not data_for_memberlist_exist():
        check_memberlist()
        return None
    #------
    mlist = get_memberlist()
    #-
    X=[]
    Y=[]
    annotations=[]
    for i in mlist:
        X += res_dict[i].Mxlist
        Y += res_dict[i].Vtotlist
        annotations += [res_dict[i].numberlist[j] + ' LC' + res_dict[i].LClist[j] for j in range(0, len(res_dict[i].numberlist))]
    #-make Mx abs
    X = [abs(i) for i in X]
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
    plt.xlabel("Mx " + unit_moment)
    plt.ylabel("Vtot " + unit_force)
    #-
    plt.show()

#-----------------------------------------------------------

def print_report():
    if print_dialog.exec_() == QtWidgets.QDialog.Accepted:
        myapp.ui.textBrowser_output.document().print_(print_dialog.printer())

def set_title(info=''):
    myapp.setWindowTitle(version + info)

def info():
    about = '''
Soco - Staad member force extract tool
Alpha stage software for testing only

-------------Licence-------------
Soco is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

Soco is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Soco; if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA.

Copyright (C) 2022 Lukasz Laba (e-mail : lukaszlaba@gmail.com)
'''
    myapp.ui.textBrowser_output.setText(about)

if __name__ == '__main__': 
    app = QtWidgets.QApplication(sys.argv)
    myapp = MAINWINDOW()
    print_dialog = QPrintDialog()
    set_title()
    myapp.ui.textBrowser_output.setText('Welcome in soco - Staad member force extract tool! Load data and fill input list to get report.')
    myapp.ui.plainTextEdit_serch.clear()
    myapp.setWindowIcon(QtGui.QIcon('app.ico'))
    myapp.show()
    sys.exit(app.exec_())


'''
command used to frozening with pyinstaller
pyinstaller --onefile --noconsole --icon=app.ico ..\gismo.py
'''