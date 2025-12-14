'''
--------------------------------------------------------------------------
Copyright (C) 2022-2025 Lukasz Laba <lukaszlaba@gmail.com>

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
import win32com.client

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import QMessageBox
from tabulate import tabulate
import matplotlib.pyplot as plt

from mainwindow_ui import Ui_MainWindow
from member_respoint import member_respoint
from preset_content import preset_dict

res_dict = {}
unit_force = '[]'
unit_moment = '[]'

version = 'soco 0.2.1'

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
        self.ui.pushButton_normFy_Fz.clicked.connect(plot_norm_Fz_Fy)
        self.ui.pushButton_Mx_Vtot.clicked.connect(plot_Mx_Vtot)
        
        #--
        self.ui.pushButton_Sort.clicked.connect(sort_memberlist)
        self.ui.pushButton_getMembers.clicked.connect(load_memberlist_from_results)
        self.ui.pushButton_makei.clicked.connect(makei)
        self.ui.pushButton_makej.clicked.connect(makej)
        self.ui.pushButton_makeij.clicked.connect(makeij)
        self.ui.pushButton_staad_show.clicked.connect(show_in_staad)
        self.ui.pushButton_check.clicked.connect(check_memberlist)
        #--
        self.ui.pushButton_clbResults.clicked.connect(clbResults)
        self.ui.pushButton_clbMembers.clicked.connect(clbMembers)
        self.ui.pushButton_clbNodes.clicked.connect(clbNodes)
        #--
        self.ui.comboBox_preset.currentIndexChanged.connect(set_preset_content)
        #--
        self.ui.pushButton_info.clicked.connect(info)
        self.ui.pushButton_print.clicked.connect(print_report)

def clbResults():
    from tkinter import Tk
    root = Tk()
    root.withdraw()
    data = root.clipboard_get()
    #import testdata
    #data = testdata.data
    data = data.replace("\r", '')
    data =  data.split('\n')
    for i in range(len(data)):#--each parameter
        tmp = data[i].split('\t')
        data[i] = tmp
    # - cheking if clipboard data is corect
    try:
        if not 'Fx' in data[0][3]:
            QMessageBox.about(myapp, "Warning", 'It looks, the cipboard has no Staad result data.')
            return None
    except:
        QMessageBox.about(myapp, "Warning", 'It looks, the cipboard has no Staad result data.')
        return None        
    #--
    for i in range(1, len(data)-1):
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
        record = data[i]
        if record[0] != '':
            memb_i = member_respoint()
            memb_j = member_respoint()
            curent_mem_number = record[0]
            memb_i.number = curent_mem_number + 'i'
            memb_j.number = curent_mem_number + 'j'
        if end == -1:
            memb_i.res.append(record)
            memb_i.node = record[2]
        #transform to internal force values instead of end forces
        if end == 1:
            record[3] = -record[3] # Fx sign update at the member end
            record[4] = -record[4] # Fy sign update at the member end
            record[5] = -record[5] # Fz sign update at the member end
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
    # - cheking if clipboard data is corect
    try:
        if not len(data[0])==7 :
            QMessageBox.about(myapp, "Warning", 'It looks, the cipboard have no Staad member data.')
            return None
    except:
        QMessageBox.about(myapp, "Warning", 'It looks, the cipboard have no Staad member data.')
        return None
    #--
    if data[-1] ==['']: data.pop()
    #--
    mlist = [str(int(i[0])) for i in data]
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
    # - cheking if clipboard data is corect
    try:
        if not len(data[0])==4 :
            QMessageBox.about(myapp, "Warning", 'It looks, the cipboard have no Staad node data.')
            return None
    except:
        QMessageBox.about(myapp, "Warning", 'It looks, the cipboard have no Staad node data.')
        return None
    #--
    if data[-1] ==['']: data.pop()
    #--
    nlist = [str(int(i[0])) for i in data]
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

def show_in_staad():
    check_memberlist()
    try:
        os = win32com.client.GetActiveObject("StaadPro.OpenSTAAD")
        geometry = os.Geometry
        geometry._FlagAsMethod("SelectBeam")
        geometry._FlagAsMethod("SelectNode")
    except:
        QMessageBox.about(myapp, "Warning", 'Staad not detected.')
        return None
    #---
    member_numbers = get_memberlist()
    member_numbers = [int(''.join(filter(str.isdigit, i))) for i in member_numbers]
    #-
    node_numbers = []
    for i in get_memberlist():
        try:
            node_numbers.append(int(res_dict[i].node))
        except:
            pass
    #-showing in staad
    for i in member_numbers:
        geometry.SelectBeam(i)
    for i in node_numbers:
        geometry.SelectNode(i)

def load_memberlist_from_results():
    mlist = list(res_dict.keys())
    mlist = [i.replace('i','') for i in mlist]
    mlist = [i.replace('j','') for i in mlist]
    mlist = list(dict.fromkeys(mlist))
    set_memberlist(mlist)

#-----------------------------------------------------------
     
def has_Fxmaxabs(where):
    data = {i : res_dict[i].Fxmaxabs[0] for i in where}
    return max(data, key=data.get)
def has_Fxmax(where):
    data = {i : res_dict[i].Fxmax[0] for i in where}
    return max(data, key=data.get)
def has_Fxmin(where):
    data = {i : res_dict[i].Fxmin[0] for i in where}
    return min(data, key=data.get)

def has_Fymaxabs(where):
    data = {i : res_dict[i].Fymaxabs[0] for i in where}
    return max(data, key=data.get)

def has_Fzmaxabs(where):
    data = {i : res_dict[i].Fzmaxabs[0] for i in where}
    return max(data, key=data.get)

def has_Mxmaxabs(where):
    data = {i : res_dict[i].Mxmaxabs[0] for i in where}
    return max(data, key=data.get)     
    
def has_Mymaxabs(where):
    data = {i : res_dict[i].Mymaxabs[0] for i in where}
    return max(data, key=data.get)
def has_Mymax(where):
    data = {i : res_dict[i].Mymax[0] for i in where}
    return max(data, key=data.get)
def has_Mymin(where):
    data = {i : res_dict[i].Mymin[0] for i in where}
    return min(data, key=data.get)

def has_Mzmaxabs(where):
    data = {i : res_dict[i].Mzmaxabs[0] for i in where}
    return max(data, key=data.get)
def has_Mzmax(where):
    data = {i : res_dict[i].Mzmax[0] for i in where}
    return max(data, key=data.get)
def has_Mzmin(where):
    data = {i : res_dict[i].Mzmin[0] for i in where}
    return min(data, key=data.get)    
    
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

def has_Boltshearmax(where):
    data = {i : res_dict[i].Boltshearmax[0] for i in where}
    return max(data, key=data.get)

def has_Fynormmax(where):
    data = {i : res_dict[i].Fynormmax[0] for i in where}
    return max(data, key=data.get)
def has_Fynormmin(where):
    data = {i : res_dict[i].Fynormmin[0] for i in where}
    return min(data, key=data.get)

def has_Fznormmax(where):
    data = {i : res_dict[i].Fznormmax[0] for i in where}
    return max(data, key=data.get)
def has_Fznormmin(where):
    data = {i : res_dict[i].Fznormmin[0] for i in where}
    return min(data, key=data.get)

def has_Fxymaxabs(where):#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    data = {i : res_dict[i].Fxymaxabs[0] for i in where}
    return max(data, key=data.get)
def has_Fxzmaxabs(where):
    data = {i : res_dict[i].Fxzmaxabs[0] for i in where}
    return max(data, key=data.get)    
def has_Fxyzmaxabs(where):
    data = {i : res_dict[i].Fxyzmaxabs[0] for i in where}
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

                if myapp.ui.checkBox_maxabsFx.isChecked():
                    if res.Fxmax[0] != 0:
                        rows.append([str(res.number), 'max |Fx| = '+str(res.Fxmaxabs[0])] + res.Fxmaxabs[1][1:9])
                    else:
                        rows.append(['-', 'max Fx = '+str(res.Fxmax[0])] + 8*['-'])

                if myapp.ui.checkBox_maxFx.isChecked():
                    if res.Fxmax[0] != 0:
                        rows.append([str(res.number), 'max Fx = '+str(res.Fxmax[0])] + res.Fxmax[1][1:9])
                    else:
                        rows.append(['-', 'max Fx = '+str(res.Fxmax[0])] + 8*['-'])

                if myapp.ui.checkBox_minFx.isChecked():
                    if res.Fxmin[0] != 0:
                        rows.append([str(res.number), 'min Fx = '+str(res.Fxmin[0])] + res.Fxmin[1][1:9])
                    else:
                        rows.append(['-', 'min Fx = '+str(res.Fxmin[0])] + 8*['-'])

                if myapp.ui.checkBox_maxabsFy.isChecked():
                    if res.Fymaxabs[0] != 0:
                        rows.append([str(res.number), 'max |Fy| = '+str(res.Fymaxabs[0])] + res.Fymaxabs[1][1:9])
                    else:
                        rows.append(['-', 'max |Fy| = '+str(res.Fymaxabs[0])] + 8*['-'])

                if myapp.ui.checkBox_maxFynorm.isChecked():
                    if res.Fynormmax[0] != 0:
                        rows.append([str(res.number), 'max Fynorm = '+str(res.Fynormmax[0])] + res.Fynormmax[1][1:9])
                    else:
                        rows.append(['-', 'max Fynorm = '+str(res.Fynormmax[0])] + 8*['-'])

                if myapp.ui.checkBox_minFynorm.isChecked():
                    if res.Fynormmin[0] != 0:
                        rows.append([str(res.number), 'min Fynorm = '+str(res.Fynormmin[0])] + res.Fynormmin[1][1:9])
                    else:
                        rows.append(['-', 'min Fynorm = '+str(res.Fynormmin[0])] + 8*['-'])

                if myapp.ui.checkBox_maxabsFz.isChecked():
                    if res.Fzmaxabs[0] != 0:
                        rows.append([str(res.number), 'max |Fz| = '+str(res.Fzmaxabs[0])] + res.Fzmaxabs[1][1:9])
                    else:
                        rows.append(['-', 'max |Fz| = '+str(res.Fzmaxabs[0])] + 8*['-'])

                if myapp.ui.checkBox_maxFznorm.isChecked():
                    if res.Fznormmax[0] != 0:
                        rows.append([str(res.number), 'max Fznorm = '+str(res.Fznormmax[0])] + res.Fznormmax[1][1:9])
                    else:
                        rows.append(['-', 'max Fznorm = '+str(res.Fznormmax[0])] + 8*['-'])

                if myapp.ui.checkBox_minFznorm.isChecked():
                    if res.Fznormmin[0] != 0:
                        rows.append([str(res.number), 'min Fznorm = '+str(res.Fznormmin[0])] + res.Fznormmin[1][1:9])
                    else:
                        rows.append(['-', 'min Fznorm = '+str(res.Fznormmin[0])] + 8*['-'])

                if myapp.ui.checkBox_maxabsFxy.isChecked(): #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                    if res.Fxymaxabs[0] != 0:
                        rows.append([str(res.number), 'max |Fxy| = '+str(res.Fxymaxabs[0])] + res.Fxymaxabs[1][1:9])
                    else:
                        rows.append(['-', 'max |Fxymax| = '+str(res.Fxymaxabs[0])] + 8*['-'])

                if myapp.ui.checkBox_maxabsFxz.isChecked():
                    if res.Fxzmaxabs[0] != 0:
                        rows.append([str(res.number), 'max |Fxz| = '+str(res.Fxzmaxabs[0])] + res.Fxzmaxabs[1][1:9])
                    else:
                        rows.append(['-', 'max |Fxzmax| = '+str(res.Fxzmaxabs[0])] + 8*['-'])

                if myapp.ui.checkBox_maxabsFxyz.isChecked():
                    if res.Fxyzmaxabs[0] != 0:
                        rows.append([str(res.number), 'max |Fxyz| = '+str(res.Fxyzmaxabs[0])] + res.Fxyzmaxabs[1][1:9])
                    else:
                        rows.append(['-', 'max |Fxyzmax| = '+str(res.Fxyzmaxabs[0])] + 8*['-'])

                if myapp.ui.checkBox_maxVtot.isChecked():
                    if res.Vtotmax[0] != 0:
                        rows.append([str(res.number), 'max |Vtot| = '+str(res.Vtotmax[0])] + res.Vtotmax[1][1:9])
                    else:
                        rows.append(['-', 'max |Vtot| = '+str(res.Vtotmax[0])] + 8*['-'])

                if myapp.ui.checkBox_maxabsMx.isChecked():
                    if res.Mxmaxabs[0] != 0:
                        rows.append([str(res.number), 'max |Mx| = '+str(res.Mxmaxabs[0])] + res.Mxmaxabs[1][1:9])
                    else:
                        rows.append(['-', 'max |Mx| = '+str(res.Mxmaxabs[0])] + 8*['-'])

                if myapp.ui.checkBox_maxabsMy.isChecked():
                    if res.Mymaxabs[0] != 0:
                        rows.append([str(res.number), 'max |My| = '+str(res.Mymaxabs[0])] + res.Mymaxabs[1][1:9])
                    else:
                        rows.append(['-', 'max |My| = '+str(res.Mymaxabs[0])] + 8*['-'])

                if myapp.ui.checkBox_maxMy.isChecked():
                    if res.Mymax[0] != 0:
                        rows.append([str(res.number), 'max My = '+str(res.Mymax[0])] + res.Mymax[1][1:9])
                    else:
                        rows.append(['-', 'max My = '+str(res.Mymax[0])] + 8*['-'])

                if myapp.ui.checkBox_minMy.isChecked():
                    if res.Mymin[0] != 0:
                        rows.append([str(res.number), 'min My = '+str(res.Mymin[0])] + res.Mymin[1][1:9])
                    else:
                        rows.append(['-', 'min My = '+str(res.Mymin[0])] + 8*['-'])

                if myapp.ui.checkBox_maxabsMz.isChecked():
                    if res.Mzmaxabs[0] != 0:
                        rows.append([str(res.number), 'max |Mz| = '+str(res.Mzmaxabs[0])] + res.Mzmaxabs[1][1:9])
                    else:
                        rows.append(['-', 'max |Mz| = '+str(res.Mzmaxabs[0])] + 8*['-'])

                if myapp.ui.checkBox_maxMz.isChecked():
                    if res.Mzmax[0] != 0:
                        rows.append([str(res.number), 'max Mz = '+str(res.Mzmax[0])] + res.Mzmax[1][1:9])
                    else:
                        rows.append(['-', 'max Mz = '+str(res.Mzmax[0])] + 8*['-'])

                if myapp.ui.checkBox_minMz.isChecked():
                    if res.Mzmin[0] != 0:
                        rows.append([str(res.number), 'min Mz = '+str(res.Mzmin[0])] + res.Mzmin[1][1:9])
                    else:
                        rows.append(['-', 'min Mz = '+str(res.Mzmin[0])] + 8*['-'])

                if myapp.ui.checkBox_maxMtot.isChecked():
                    if res.Mtotmax[0] != 0:
                        rows.append([str(res.number), 'max |Mtot| = '+str(res.Mtotmax[0])] + res.Mtotmax[1][1:9])
                    else:
                        rows.append(['-', 'max |Mtot| = '+str(res.Mtotmax[0])] + 8*['-'])

                if myapp.ui.checkBox_maxconncomp.isChecked():
                    if res.Boltcompressionmax[0] != 0:
                        rows.append([str(res.number), 'max conn comp (N-M)'] + res.Boltcompressionmax[1][1:9])
                    else:
                        rows.append(['-', 'max conn comp (N-M)'] + 8*['-'])

                if myapp.ui.checkBox_maxbolttens.isChecked():
                    if res.Bolttensionmax[0] != 0:
                        rows.append([str(res.number), 'max bolt tens (N-M)'] + res.Bolttensionmax[1][1:9])
                    else:
                        rows.append(['-', 'max bolt tens (N-M)'] + 8*['-'])

                if myapp.ui.checkBox_maxboltshear.isChecked():
                    if res.Boltshearmax[0] != 0:
                        rows.append([str(res.number), 'max bolt shear (V-T)'] + res.Boltshearmax[1][1:9])
                    else:
                        rows.append(['-', 'max bolt shear (V-T)'] + 8*['-'])
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

        if myapp.ui.checkBox_maxabsFx.isChecked():
            res = res_dict[has_Fxmaxabs(filterlist)]
            if res.Fxmax[0] != 0:
                rows.append([str(res.number), 'max |Fx| = '+str(res.Fxmaxabs[0])] + res.Fxmaxabs[1][1:9])
            else:
                rows.append(['-', 'max Fx = '+str(res.Fxmax[0])] + 8*['-'])

        if myapp.ui.checkBox_maxFx.isChecked():
            res = res_dict[has_Fxmax(filterlist)]
            if res.Fxmax[0] != 0:
                rows.append([str(res.number), 'max Fx = '+str(res.Fxmax[0])] + res.Fxmax[1][1:9])
            else:
                rows.append(['-', 'max Fx = '+str(res.Fxmax[0])] + 8*['-'])

        if myapp.ui.checkBox_minFx.isChecked():
            res = res_dict[has_Fxmin(filterlist)]
            if res.Fxmin[0] != 0:
                rows.append([str(res.number), 'min Fx = '+str(res.Fxmin[0])] + res.Fxmin[1][1:9])
            else:
                rows.append(['-', 'min Fx = '+str(res.Fxmin[0])] + 8*['-'])

        if myapp.ui.checkBox_maxabsFy.isChecked():
            res = res_dict[has_Fymaxabs(filterlist)]
            if res.Fymaxabs[0] != 0:
                rows.append([str(res.number), 'max |Fy| = '+str(res.Fymaxabs[0])] + res.Fymaxabs[1][1:9])
            else:
                rows.append(['-', 'max |Fy| = '+str(res.Fymaxabs[0])] + 8*['-'])

        if myapp.ui.checkBox_maxFynorm.isChecked():
            res = res_dict[has_Fynormmax(filterlist)]
            if res.Fynormmax[0] != 0:
                rows.append([str(res.number), 'max Fynorm = '+str(res.Fynormmax[0])] + res.Fynormmax[1][1:9])
            else:
                rows.append(['-', 'max Fynorm = '+str(res.Fynormmax[0])] + 8*['-'])

        if myapp.ui.checkBox_minFynorm.isChecked():
            res = res_dict[has_Fynormmin(filterlist)]
            if res.Fynormmin[0] != 0:
                rows.append([str(res.number), 'min Fynorm = '+str(res.Fynormmin[0])] + res.Fynormmin[1][1:9])
            else:
                rows.append(['-', 'min Fynorm = '+str(res.Fynormmin[0])] + 8*['-'])

        if myapp.ui.checkBox_maxabsFz.isChecked():
            res = res_dict[has_Fzmaxabs(filterlist)]
            if res.Fzmaxabs[0] != 0:
                rows.append([str(res.number), 'max |Fz| = '+str(res.Fzmaxabs[0])] + res.Fzmaxabs[1][1:9])
            else:
                rows.append(['-', 'max |Fz| = '+str(res.Fzmaxabs[0])] + 8*['-'])

        if myapp.ui.checkBox_maxFznorm.isChecked():
            res = res_dict[has_Fznormmax(filterlist)]
            if res.Fznormmax[0] != 0:
                rows.append([str(res.number), 'max Fznorm = '+str(res.Fznormmax[0])] + res.Fznormmax[1][1:9])
            else:
                rows.append(['-', 'max Fznorm = '+str(res.Fznormmax[0])] + 8*['-'])

        if myapp.ui.checkBox_minFznorm.isChecked():
            res = res_dict[has_Fznormmin(filterlist)]
            if res.Fznormmin[0] != 0:
                rows.append([str(res.number), 'min Fznorm = '+str(res.Fznormmin[0])] + res.Fznormmin[1][1:9])
            else:
                rows.append(['-', 'min Fznorm = '+str(res.Fznormmin[0])] + 8*['-'])

        if myapp.ui.checkBox_maxVtot.isChecked():
            res = res_dict[has_Vtotmax(filterlist)]
            if res.Vtotmax[0] != 0:
                rows.append([str(res.number), 'max |Vtot| = '+str(res.Vtotmax[0])] + res.Vtotmax[1][1:9])
            else:
                rows.append(['-', 'max |Vtot| = '+str(res.Vtotmax[0])] + 8*['-'])

        if myapp.ui.checkBox_maxabsFxy.isChecked():#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            res = res_dict[has_Fxymaxabs(filterlist)]
            if res.Fxymaxabs[0] != 0:
                rows.append([str(res.number), 'max |Fxy| = '+str(res.Fxymaxabs[0])] + res.Fxymaxabs[1][1:9])
            else:
                rows.append(['-', 'max |Vtot| = '+str(res.Fxymaxabs[0])] + 8*['-'])

        if myapp.ui.checkBox_maxabsFxz.isChecked():
            res = res_dict[has_Fxzmaxabs(filterlist)]
            if res.Fxzmaxabs[0] != 0:
                rows.append([str(res.number), 'max |Fxz| = '+str(res.Fxzmaxabs[0])] + res.Fxzmaxabs[1][1:9])
            else:
                rows.append(['-', 'max |Fxz| = '+str(res.Fxzmaxabs[0])] + 8*['-'])

        if myapp.ui.checkBox_maxabsFxyz.isChecked():
            res = res_dict[has_Fxyzmaxabs(filterlist)]
            if res.Fxyzmaxabs[0] != 0:
                rows.append([str(res.number), 'max |Fxyz| = '+str(res.Fxyzmaxabs[0])] + res.Fxyzmaxabs[1][1:9])
            else:
                rows.append(['-', 'max |Fxyz| = '+str(res.Fxyzmaxabs[0])] + 8*['-'])

        if myapp.ui.checkBox_maxabsMx.isChecked():
            res = res_dict[has_Mxmaxabs(filterlist)]
            if res.Mxmaxabs[0] != 0:
                rows.append([str(res.number), 'max |Mx| = '+str(res.Mxmaxabs[0])] + res.Mxmaxabs[1][1:9])
            else:
                rows.append(['-', 'max |Mx| = '+str(res.Mxmaxabs[0])] + 8*['-'])

        if myapp.ui.checkBox_maxabsMy.isChecked():
            res = res_dict[has_Mymaxabs(filterlist)]
            if res.Mymaxabs[0] != 0:
                rows.append([str(res.number), 'max |My| = '+str(res.Mymaxabs[0])] + res.Mymaxabs[1][1:9])
            else:
                rows.append(['-', 'max |My| = '+str(res.Mymaxabs[0])] + 8*['-'])

        if myapp.ui.checkBox_maxMy.isChecked():
            res = res_dict[has_Mymax(filterlist)]
            if res.Mymax[0] != 0:
                rows.append([str(res.number), 'max My = '+str(res.Mymax[0])] + res.Mymax[1][1:9])
            else:
                rows.append(['-', 'max My = '+str(res.Mymax[0])] + 8*['-'])

        if myapp.ui.checkBox_minMy.isChecked():
            res = res_dict[has_Mymin(filterlist)]
            if res.Mymin[0] != 0:
                rows.append([str(res.number), 'min My = '+str(res.Mymin[0])] + res.Mymin[1][1:9])
            else:
                rows.append(['-', 'min My = '+str(res.Mymin[0])] + 8*['-'])

        if myapp.ui.checkBox_maxabsMz.isChecked():
            res = res_dict[has_Mzmaxabs(filterlist)]
            if res.Mzmaxabs[0] != 0:
                rows.append([str(res.number), 'max |Mz| = '+str(res.Mzmaxabs[0])] + res.Mzmaxabs[1][1:9])
            else:
                rows.append(['-', 'max |Mz| = '+str(res.Mzmaxabs[0])] + 8*['-'])

        if myapp.ui.checkBox_maxMz.isChecked():
            res = res_dict[has_Mzmax(filterlist)]
            if res.Mzmax[0] != 0:
                rows.append([str(res.number), 'max Mz = '+str(res.Mzmax[0])] + res.Mzmax[1][1:9])
            else:
                rows.append(['-', 'max Mz = '+str(res.Mzmax[0])] + 8*['-'])

        if myapp.ui.checkBox_minMz.isChecked():
            res = res_dict[has_Mzmin(filterlist)]
            if res.Mzmin[0] != 0:
                rows.append([str(res.number), 'min Mz = '+str(res.Mzmin[0])] + res.Mzmin[1][1:9])
            else:
                rows.append(['-', 'min Mz = '+str(res.Mzmin[0])] + 8*['-'])

        if myapp.ui.checkBox_maxMtot.isChecked():
            res = res_dict[has_Mtotmax(filterlist)]
            if res.Mtotmax[0] != 0:
                rows.append([str(res.number), 'max |Mtot| = '+str(res.Mtotmax[0])] + res.Mtotmax[1][1:9])
            else:
                rows.append(['-', 'max |Mtot| = '+str(res.Mtotmax[0])] + 8*['-'])

        if myapp.ui.checkBox_maxconncomp.isChecked():
            res = res_dict[has_Boltcompressionmax(filterlist)]
            if res.Boltcompressionmax[0] != 0:
                rows.append([str(res.number), 'max conn comp (N-M)'] + res.Boltcompressionmax[1][1:9])
            else:
                rows.append(['-', 'max conn comp (N-M)'] + 8*['-'])

        if myapp.ui.checkBox_maxbolttens.isChecked():
            res = res_dict[has_Bolttensionmax(filterlist)]
            if res.Bolttensionmax[0] != 0:
                rows.append([str(res.number), 'max bolt tens (N-M)'] + res.Bolttensionmax[1][1:9])
            else:
                rows.append(['-', 'max bolt tens (N-M)'] + 8*['-'])

        if myapp.ui.checkBox_maxboltshear.isChecked():
            res = res_dict[has_Boltshearmax(filterlist)]
            if res.Boltshearmax[0] != 0:
                rows.append([str(res.number), 'max bolt shear (V-T)'] + res.Boltshearmax[1][1:9])
            else:
                rows.append(['-', 'max bolt shear (V-T)'] + 8*['-'])
        report = tabulate(rows, headers="firstrow", tablefmt="grid")

        #--- adding compressed list
        report += '\n'
        report += '\n'
        report += 'Compressed list of load cases:\n'
        unique = {}
        rows = rows[1:]
        for i in rows:
            i.pop(1)
            if i[0] != '-':
                unique[i[0]+i[1]] = i
        unique = [unique[i] for i in unique.keys()]
        unique = [['Loc', 'LC', 'Node', 'Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']] + unique
        report += tabulate(unique, headers="firstrow", tablefmt="grid")

        #--- adding factord excel format
        if myapp.ui.checkBox_excel.isChecked():
            factor = float(myapp.ui.lineEdit_ideafactor.text())
            report += '\n'
            report += '\nCompressed list of load cases in excel (with factor %s):\n'%factor
            report += '(copy paste to notepad then to excel)\n'
            unique = unique[1:]
            report += 'Loc\tLC\tFx\tFy\tFz\tMx\tMy\tMz\n'
            for i in unique:
                report += '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(i[0],i[1],
                                                        round(i[3]*factor, 3),
                                                        round(i[4]*factor, 3),
                                                        round(i[5]*factor, 3),
                                                        round(i[6]*factor, 3),
                                                        round(i[7]*factor, 3),
                                                        round(i[8]*factor, 3))
        #--- adding factored IdeaStatica format
        if myapp.ui.checkBox_idea.isChecked():
            factor = float(myapp.ui.lineEdit_ideafactor.text())
            report += '\n'
            report += '\nCompressed list of load cases in IdeStatica format (with factor %s):\n'%factor
            report += '(copy paste to IdeaStatica)\n'
            report += 'N\tVy\tVz\tMx\tMy\tMz\n'
            for i in unique:
                if 'i' in i[0]:
                    report += '%s\t%s\t%s\t%s\t%s\t%s\n'%(  round(-i[3]*factor, 2),
                                                            round(i[5]*factor, 2),
                                                            round(-i[4]*factor, 2),
                                                            round(-i[6]*factor, 2),
                                                            round(i[8]*factor, 2),
                                                            round(-i[7]*factor, 2))
                if 'j' in i[0]:
                    report += '%s\t%s\t%s\t%s\t%s\t%s\n'%(  round(-i[3]*factor, 2),
                                                            round(i[5]*factor, 2),
                                                            round(i[4]*factor, 2),
                                                            round(-i[6]*factor, 2),
                                                            round(i[8]*factor, 2),
                                                            round(i[7]*factor, 2))
        return report
    else:
        return ''


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
    limx = 1.1*max(abs(max(X)),abs(min(X)))
    limy = 1.1*max(abs(max(Y)),abs(min(Y)))
    plt.xlim([-limx, limx])
    plt.ylim([-limy, limy])
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
    limx = 1.1*max(abs(max(X)),abs(min(X)))
    limy = 1.1*max(abs(max(Y)),abs(min(Y)))
    plt.xlim([-limx, limx])
    plt.ylim([-limy, limy])
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
    limx = 1.1*max(abs(max(X)),abs(min(X)))
    limy = 1.1*max(abs(max(Y)),abs(min(Y)))
    plt.xlim([-limx, limx])
    plt.ylim([0, limy])
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
    lim = 1.1*max(abs(max(X)),abs(min(X)),abs(max(Y)),abs(min(Y)))
    plt.xlim([-lim, lim])
    plt.ylim([-lim, lim])
    ax = plt.gca()
    ax.set_aspect('equal')
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
    
    lim = 1.1*max(abs(max(X)),abs(min(X)),abs(max(Y)),abs(min(Y)))
    plt.xlim([0, lim])
    plt.ylim([0, lim])
    ax = plt.gca()
    ax.set_aspect('equal')
    #-
    plt.show()

def plot_norm_Fz_Fy():
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
        X += res_dict[i].Fznormlist
        Y += res_dict[i].Fynormlist
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
    plt.title("norm Fy-norm Fz", fontsize=15)
    plt.xlabel("norm Fz " + unit_force)
    plt.ylabel("norm Fy " + unit_force)
    lim = 1.1*max(abs(max(X)),abs(min(X)),abs(max(Y)),abs(min(Y)))
    plt.xlim([-lim, lim])
    plt.ylim([-lim, lim])
    ax = plt.gca()
    ax.set_aspect('equal')
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
    plt.title("|Mx|-Vtot", fontsize=15)
    plt.xlabel("|Mx| " + unit_moment)
    plt.ylabel("Vtot " + unit_force)
    limx = 1.1*max(abs(max(X)),abs(min(X)))
    limy = 1.1*max(abs(max(Y)),abs(min(Y)))
    plt.xlim([0, limx])
    plt.ylim([0, limy])
    #-
    plt.show()

#-----------------------------------------------------------
def set_preset_content():
    selected = myapp.ui.comboBox_preset.currentText()
    states = preset_dict[selected]
    print(states)
    
    myapp.ui.checkBox_maxabsFx.setChecked(states[0])
    myapp.ui.checkBox_maxFx.setChecked(states[1])
    myapp.ui.checkBox_minFx.setChecked(states[2])
    
    myapp.ui.checkBox_maxabsFy.setChecked(states[3])
    myapp.ui.checkBox_maxFynorm.setChecked(states[4])
    myapp.ui.checkBox_minFynorm.setChecked(states[5])
    
    myapp.ui.checkBox_maxabsFz.setChecked(states[6])
    myapp.ui.checkBox_maxFznorm.setChecked(states[7])
    myapp.ui.checkBox_minFznorm.setChecked(states[8])

    myapp.ui.checkBox_maxVtot.setChecked(states[9])
    
    myapp.ui.checkBox_maxabsFxy.setChecked(states[10]) #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    myapp.ui.checkBox_maxabsFxz.setChecked(states[11])
    
    myapp.ui.checkBox_maxabsFxyz.setChecked(states[12])
    
    myapp.ui.checkBox_maxabsMx.setChecked(states[13])
    
    myapp.ui.checkBox_maxabsMy.setChecked(states[14])
    myapp.ui.checkBox_maxMy.setChecked(states[15])
    myapp.ui.checkBox_minMy.setChecked(states[16])
    
    myapp.ui.checkBox_maxabsMz.setChecked(states[17])
    myapp.ui.checkBox_maxMz.setChecked(states[18])
    myapp.ui.checkBox_minMz.setChecked(states[19])
    
    myapp.ui.checkBox_maxMtot.setChecked(states[20])
    
    myapp.ui.checkBox_maxconncomp.setChecked(states[21])
    myapp.ui.checkBox_maxbolttens.setChecked(states[22])
    myapp.ui.checkBox_maxboltshear.setChecked(states[23])

def print_report():
    if print_dialog.exec_() == QtWidgets.QDialog.Accepted:
        myapp.ui.textBrowser_output.document().print_(print_dialog.printer())

def set_title(info=''):
    myapp.setWindowTitle(version + info)

def info():
    about = '''
Soco - Staad member result extract tool.
Beta stage software.

-------------Licence-------------
Soco is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

Soco is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Soco; if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA.

Copyright (C) 2022-2025 Lukasz Laba (e-mail : lukaszlaba@gmail.com)
Project website: https://github.com/lukaszlaba/soco
Check for lataest version: https://github.com/lukaszlaba/soco/releases
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
    myapp.ui.comboBox_preset.addItems(preset_dict.keys())
    myapp.ui.comboBox_preset.setCurrentIndex(3)
    myapp.show()
    sys.exit(app.exec_())


'''
command used to frozening with pyinstaller
pyinstaller --onefile --noconsole --icon=app.ico ..\soco.py

command used to get updated mainwindow_ui.py
pyuic5 ...\mainwindow.ui > ...\mainwindow_ui.py
'''