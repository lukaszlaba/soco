# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1367, 764)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser_output = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_output.setGeometry(QtCore.QRect(180, 40, 1061, 661))
        font = QtGui.QFont()
        font.setFamily("ISOCTEUR")
        font.setPointSize(9)
        self.textBrowser_output.setFont(font)
        self.textBrowser_output.setObjectName("textBrowser_output")
        self.plainTextEdit_serch = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_serch.setGeometry(QtCore.QRect(10, 40, 161, 401))
        font = QtGui.QFont()
        font.setFamily("ISOCPEUR")
        font.setPointSize(8)
        self.plainTextEdit_serch.setFont(font)
        self.plainTextEdit_serch.setObjectName("plainTextEdit_serch")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 47, 13))
        self.label.setObjectName("label")
        self.pushButton_check = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_check.setGeometry(QtCore.QRect(10, 600, 161, 23))
        self.pushButton_check.setObjectName("pushButton_check")
        self.pushButton_clbResults = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clbResults.setGeometry(QtCore.QRect(10, 650, 161, 23))
        self.pushButton_clbResults.setObjectName("pushButton_clbResults")
        self.pushButton_Sort = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Sort.setGeometry(QtCore.QRect(10, 450, 161, 23))
        self.pushButton_Sort.setObjectName("pushButton_Sort")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 630, 91, 16))
        self.label_3.setObjectName("label_3")
        self.pushButton_clbMembers = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clbMembers.setGeometry(QtCore.QRect(10, 680, 161, 23))
        self.pushButton_clbMembers.setObjectName("pushButton_clbMembers")
        self.pushButton_clbNodes = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clbNodes.setGeometry(QtCore.QRect(10, 710, 161, 23))
        self.pushButton_clbNodes.setObjectName("pushButton_clbNodes")
        self.pushButton_getMembers = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_getMembers.setGeometry(QtCore.QRect(10, 480, 161, 23))
        self.pushButton_getMembers.setObjectName("pushButton_getMembers")
        self.pushButton_makei = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_makei.setGeometry(QtCore.QRect(10, 510, 161, 23))
        self.pushButton_makei.setObjectName("pushButton_makei")
        self.pushButton_makej = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_makej.setGeometry(QtCore.QRect(10, 540, 161, 23))
        self.pushButton_makej.setObjectName("pushButton_makej")
        self.pushButton_makeij = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_makeij.setGeometry(QtCore.QRect(10, 570, 161, 23))
        self.pushButton_makeij.setObjectName("pushButton_makeij")
        self.lineEdit_staadname = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_staadname.setGeometry(QtCore.QRect(350, 710, 481, 20))
        self.lineEdit_staadname.setText("")
        self.lineEdit_staadname.setObjectName("lineEdit_staadname")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(200, 710, 151, 16))
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(1250, 620, 100, 13))
        self.label_6.setObjectName("label_6")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setEnabled(False)
        self.comboBox.setGeometry(QtCore.QRect(1250, 640, 101, 22))
        self.comboBox.setObjectName("comboBox")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(1250, 50, 102, 552))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.line_5 = QtWidgets.QFrame(self.widget)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout.addWidget(self.line_5)
        self.checkBox_maxabsFx = QtWidgets.QCheckBox(self.widget)
        self.checkBox_maxabsFx.setEnabled(True)
        self.checkBox_maxabsFx.setChecked(True)
        self.checkBox_maxabsFx.setObjectName("checkBox_maxabsFx")
        self.verticalLayout.addWidget(self.checkBox_maxabsFx)
        self.checkBox_maxFx = QtWidgets.QCheckBox(self.widget)
        self.checkBox_maxFx.setEnabled(True)
        self.checkBox_maxFx.setObjectName("checkBox_maxFx")
        self.verticalLayout.addWidget(self.checkBox_maxFx)
        self.checkBox_minFx = QtWidgets.QCheckBox(self.widget)
        self.checkBox_minFx.setEnabled(True)
        self.checkBox_minFx.setObjectName("checkBox_minFx")
        self.verticalLayout.addWidget(self.checkBox_minFx)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.checkBox_maxabsFy = QtWidgets.QCheckBox(self.widget)
        self.checkBox_maxabsFy.setEnabled(True)
        self.checkBox_maxabsFy.setChecked(True)
        self.checkBox_maxabsFy.setObjectName("checkBox_maxabsFy")
        self.verticalLayout.addWidget(self.checkBox_maxabsFy)
        self.checkBox_maxFynorm = QtWidgets.QCheckBox(self.widget)
        self.checkBox_maxFynorm.setEnabled(True)
        self.checkBox_maxFynorm.setObjectName("checkBox_maxFynorm")
        self.verticalLayout.addWidget(self.checkBox_maxFynorm)
        self.checkBox_minFynorm = QtWidgets.QCheckBox(self.widget)
        self.checkBox_minFynorm.setEnabled(True)
        self.checkBox_minFynorm.setObjectName("checkBox_minFynorm")
        self.verticalLayout.addWidget(self.checkBox_minFynorm)
        self.checkBox_maxabsFz = QtWidgets.QCheckBox(self.widget)
        self.checkBox_maxabsFz.setEnabled(True)
        self.checkBox_maxabsFz.setChecked(True)
        self.checkBox_maxabsFz.setObjectName("checkBox_maxabsFz")
        self.verticalLayout.addWidget(self.checkBox_maxabsFz)
        self.checkBox_maxFznorm = QtWidgets.QCheckBox(self.widget)
        self.checkBox_maxFznorm.setEnabled(True)
        self.checkBox_maxFznorm.setObjectName("checkBox_maxFznorm")
        self.verticalLayout.addWidget(self.checkBox_maxFznorm)
        self.checkBox_minFznorm = QtWidgets.QCheckBox(self.widget)
        self.checkBox_minFznorm.setEnabled(True)
        self.checkBox_minFznorm.setObjectName("checkBox_minFznorm")
        self.verticalLayout.addWidget(self.checkBox_minFznorm)
        self.checkBox_maxVtot = QtWidgets.QCheckBox(self.widget)
        self.checkBox_maxVtot.setEnabled(True)
        self.checkBox_maxVtot.setChecked(True)
        self.checkBox_maxVtot.setObjectName("checkBox_maxVtot")
        self.verticalLayout.addWidget(self.checkBox_maxVtot)
        self.line_2 = QtWidgets.QFrame(self.widget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.checkBox_maxabsMx = QtWidgets.QCheckBox(self.widget)
        self.checkBox_maxabsMx.setEnabled(True)
        self.checkBox_maxabsMx.setChecked(True)
        self.checkBox_maxabsMx.setObjectName("checkBox_maxabsMx")
        self.verticalLayout.addWidget(self.checkBox_maxabsMx)
        self.line_3 = QtWidgets.QFrame(self.widget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.checkBox_maxabsMy = QtWidgets.QCheckBox(self.widget)
        self.checkBox_maxabsMy.setEnabled(True)
        self.checkBox_maxabsMy.setChecked(True)
        self.checkBox_maxabsMy.setObjectName("checkBox_maxabsMy")
        self.verticalLayout.addWidget(self.checkBox_maxabsMy)
        self.checkBox_maxMy = QtWidgets.QCheckBox(self.widget)
        self.checkBox_maxMy.setEnabled(True)
        self.checkBox_maxMy.setObjectName("checkBox_maxMy")
        self.verticalLayout.addWidget(self.checkBox_maxMy)
        self.checkBox_minMy = QtWidgets.QCheckBox(self.widget)
        self.checkBox_minMy.setEnabled(True)
        self.checkBox_minMy.setObjectName("checkBox_minMy")
        self.verticalLayout.addWidget(self.checkBox_minMy)
        self.checkBox_maxabsMz = QtWidgets.QCheckBox(self.widget)
        self.checkBox_maxabsMz.setEnabled(True)
        self.checkBox_maxabsMz.setChecked(True)
        self.checkBox_maxabsMz.setObjectName("checkBox_maxabsMz")
        self.verticalLayout.addWidget(self.checkBox_maxabsMz)
        self.checkBox_maxMz = QtWidgets.QCheckBox(self.widget)
        self.checkBox_maxMz.setEnabled(True)
        self.checkBox_maxMz.setObjectName("checkBox_maxMz")
        self.verticalLayout.addWidget(self.checkBox_maxMz)
        self.checkBox_minMz = QtWidgets.QCheckBox(self.widget)
        self.checkBox_minMz.setEnabled(True)
        self.checkBox_minMz.setObjectName("checkBox_minMz")
        self.verticalLayout.addWidget(self.checkBox_minMz)
        self.checkBox_maxMtot = QtWidgets.QCheckBox(self.widget)
        self.checkBox_maxMtot.setEnabled(True)
        self.checkBox_maxMtot.setChecked(True)
        self.checkBox_maxMtot.setObjectName("checkBox_maxMtot")
        self.verticalLayout.addWidget(self.checkBox_maxMtot)
        self.line_4 = QtWidgets.QFrame(self.widget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout.addWidget(self.line_4)
        self.checkBox_maxconncomp = QtWidgets.QCheckBox(self.widget)
        self.checkBox_maxconncomp.setEnabled(True)
        self.checkBox_maxconncomp.setChecked(True)
        self.checkBox_maxconncomp.setObjectName("checkBox_maxconncomp")
        self.verticalLayout.addWidget(self.checkBox_maxconncomp)
        self.checkBox_maxbolttens = QtWidgets.QCheckBox(self.widget)
        self.checkBox_maxbolttens.setEnabled(True)
        self.checkBox_maxbolttens.setChecked(True)
        self.checkBox_maxbolttens.setObjectName("checkBox_maxbolttens")
        self.verticalLayout.addWidget(self.checkBox_maxbolttens)
        self.checkBox_maxboltshear = QtWidgets.QCheckBox(self.widget)
        self.checkBox_maxboltshear.setEnabled(True)
        self.checkBox_maxboltshear.setChecked(True)
        self.checkBox_maxboltshear.setObjectName("checkBox_maxboltshear")
        self.verticalLayout.addWidget(self.checkBox_maxboltshear)
        self.line_6 = QtWidgets.QFrame(self.widget)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout.addWidget(self.line_6)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(180, 10, 291, 21))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_Report = QtWidgets.QPushButton(self.widget1)
        self.pushButton_Report.setObjectName("pushButton_Report")
        self.horizontalLayout_2.addWidget(self.pushButton_Report)
        self.checkBox_full = QtWidgets.QCheckBox(self.widget1)
        self.checkBox_full.setChecked(False)
        self.checkBox_full.setObjectName("checkBox_full")
        self.horizontalLayout_2.addWidget(self.checkBox_full)
        self.widget2 = QtWidgets.QWidget(self.centralwidget)
        self.widget2.setGeometry(QtCore.QRect(980, 710, 241, 22))
        self.widget2.setObjectName("widget2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_7 = QtWidgets.QLabel(self.widget2)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.checkBox_excel = QtWidgets.QCheckBox(self.widget2)
        self.checkBox_excel.setEnabled(True)
        self.checkBox_excel.setObjectName("checkBox_excel")
        self.horizontalLayout_3.addWidget(self.checkBox_excel)
        self.checkBox_excel_2 = QtWidgets.QCheckBox(self.widget2)
        self.checkBox_excel_2.setEnabled(False)
        self.checkBox_excel_2.setObjectName("checkBox_excel_2")
        self.horizontalLayout_3.addWidget(self.checkBox_excel_2)
        self.lineEdit_ideafactor = QtWidgets.QLineEdit(self.widget2)
        self.lineEdit_ideafactor.setEnabled(True)
        self.lineEdit_ideafactor.setMaximumSize(QtCore.QSize(30, 16777215))
        self.lineEdit_ideafactor.setObjectName("lineEdit_ideafactor")
        self.horizontalLayout_3.addWidget(self.lineEdit_ideafactor)
        self.widget3 = QtWidgets.QWidget(self.centralwidget)
        self.widget3.setGeometry(QtCore.QRect(490, 10, 701, 21))
        self.widget3.setObjectName("widget3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.widget3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.pushButton_Fx_My = QtWidgets.QPushButton(self.widget3)
        self.pushButton_Fx_My.setObjectName("pushButton_Fx_My")
        self.horizontalLayout.addWidget(self.pushButton_Fx_My)
        self.pushButton_Fx_Mz = QtWidgets.QPushButton(self.widget3)
        self.pushButton_Fx_Mz.setObjectName("pushButton_Fx_Mz")
        self.horizontalLayout.addWidget(self.pushButton_Fx_Mz)
        self.pushButton_Fx_Mtot = QtWidgets.QPushButton(self.widget3)
        self.pushButton_Fx_Mtot.setObjectName("pushButton_Fx_Mtot")
        self.horizontalLayout.addWidget(self.pushButton_Fx_Mtot)
        self.pushButton_My_Mz = QtWidgets.QPushButton(self.widget3)
        self.pushButton_My_Mz.setObjectName("pushButton_My_Mz")
        self.horizontalLayout.addWidget(self.pushButton_My_Mz)
        self.pushButton_Fy_Fz = QtWidgets.QPushButton(self.widget3)
        self.pushButton_Fy_Fz.setObjectName("pushButton_Fy_Fz")
        self.horizontalLayout.addWidget(self.pushButton_Fy_Fz)
        self.pushButton_normFy_Fz = QtWidgets.QPushButton(self.widget3)
        self.pushButton_normFy_Fz.setObjectName("pushButton_normFy_Fz")
        self.horizontalLayout.addWidget(self.pushButton_normFy_Fz)
        self.pushButton_Mx_Vtot = QtWidgets.QPushButton(self.widget3)
        self.pushButton_Mx_Vtot.setObjectName("pushButton_Mx_Vtot")
        self.horizontalLayout.addWidget(self.pushButton_Mx_Vtot)
        self.checkBox_pltAnnot = QtWidgets.QCheckBox(self.widget3)
        self.checkBox_pltAnnot.setChecked(True)
        self.checkBox_pltAnnot.setObjectName("checkBox_pltAnnot")
        self.horizontalLayout.addWidget(self.checkBox_pltAnnot)
        self.widget4 = QtWidgets.QWidget(self.centralwidget)
        self.widget4.setGeometry(QtCore.QRect(1200, 10, 158, 21))
        self.widget4.setObjectName("widget4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_print = QtWidgets.QPushButton(self.widget4)
        self.pushButton_print.setObjectName("pushButton_print")
        self.horizontalLayout_4.addWidget(self.pushButton_print)
        self.pushButton_info = QtWidgets.QPushButton(self.widget4)
        self.pushButton_info.setObjectName("pushButton_info")
        self.horizontalLayout_4.addWidget(self.pushButton_info)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1367, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.actionLoadXLS = QtWidgets.QAction(MainWindow)
        self.actionLoadXLS.setEnabled(True)
        self.actionLoadXLS.setObjectName("actionLoadXLS")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "gismo"))
        self.textBrowser_output.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'ISOCTEUR\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8.25pt;\">a---as</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8.25pt;\">0-----</span></p></body></html>"))
        self.plainTextEdit_serch.setPlainText(_translate("MainWindow", "12x25 rectangle - 209j\n"
"12x25 rectangle - 101i\n"
"12x25 rectangle - 1109j\n"
"10 dia bar - 965j\n"
"10 dia bar - 972j\n"
"10 dia bar - 757i"))
        self.label.setText(_translate("MainWindow", "Input list:"))
        self.pushButton_check.setText(_translate("MainWindow", "Check list"))
        self.pushButton_clbResults.setText(_translate("MainWindow", ">> get beam results"))
        self.pushButton_Sort.setText(_translate("MainWindow", "Sort list"))
        self.label_3.setText(_translate("MainWindow", "Clipboard data:"))
        self.pushButton_clbMembers.setText(_translate("MainWindow", ">> get beam numbers"))
        self.pushButton_clbNodes.setText(_translate("MainWindow", ">> get node numbers"))
        self.pushButton_getMembers.setText(_translate("MainWindow", "get all members"))
        self.pushButton_makei.setText(_translate("MainWindow", " make all  i"))
        self.pushButton_makej.setText(_translate("MainWindow", "make all j"))
        self.pushButton_makeij.setText(_translate("MainWindow", "make all i and j"))
        self.label_4.setText(_translate("MainWindow", "Data source staad file name:"))
        self.label_6.setText(_translate("MainWindow", "Set preset:"))
        self.label_5.setText(_translate("MainWindow", "Report content:"))
        self.checkBox_maxabsFx.setText(_translate("MainWindow", "max|Fx|"))
        self.checkBox_maxFx.setText(_translate("MainWindow", "maxFx"))
        self.checkBox_minFx.setText(_translate("MainWindow", "minFx"))
        self.checkBox_maxabsFy.setText(_translate("MainWindow", "max|Fy|"))
        self.checkBox_maxFynorm.setText(_translate("MainWindow", "maxFynorm"))
        self.checkBox_minFynorm.setText(_translate("MainWindow", "minFynorm"))
        self.checkBox_maxabsFz.setText(_translate("MainWindow", "max|Fz|"))
        self.checkBox_maxFznorm.setText(_translate("MainWindow", "maxFznorm"))
        self.checkBox_minFznorm.setText(_translate("MainWindow", "minFznorm"))
        self.checkBox_maxVtot.setText(_translate("MainWindow", "max |Vtot|"))
        self.checkBox_maxabsMx.setText(_translate("MainWindow", "max|Mx|"))
        self.checkBox_maxabsMy.setText(_translate("MainWindow", "max|My|"))
        self.checkBox_maxMy.setText(_translate("MainWindow", "maxMy"))
        self.checkBox_minMy.setText(_translate("MainWindow", "minMy"))
        self.checkBox_maxabsMz.setText(_translate("MainWindow", "max|Mz|"))
        self.checkBox_maxMz.setText(_translate("MainWindow", "maxMz"))
        self.checkBox_minMz.setText(_translate("MainWindow", "minMz"))
        self.checkBox_maxMtot.setText(_translate("MainWindow", "max|Mtot|"))
        self.checkBox_maxconncomp.setText(_translate("MainWindow", "max conn comp "))
        self.checkBox_maxbolttens.setText(_translate("MainWindow", "max bolt tens"))
        self.checkBox_maxboltshear.setText(_translate("MainWindow", "max bolt shear"))
        self.pushButton_Report.setText(_translate("MainWindow", "GET REPORT"))
        self.checkBox_full.setText(_translate("MainWindow", "long report"))
        self.label_7.setText(_translate("MainWindow", "Include"))
        self.checkBox_excel.setText(_translate("MainWindow", "excel /"))
        self.checkBox_excel_2.setText(_translate("MainWindow", "Idea with factor"))
        self.lineEdit_ideafactor.setText(_translate("MainWindow", "1.0"))
        self.label_2.setText(_translate("MainWindow", "Plot:"))
        self.pushButton_Fx_My.setText(_translate("MainWindow", " Fx-My"))
        self.pushButton_Fx_Mz.setText(_translate("MainWindow", " Fx-Mz"))
        self.pushButton_Fx_Mtot.setText(_translate("MainWindow", "Fx-Mtot"))
        self.pushButton_My_Mz.setText(_translate("MainWindow", "Mz-My"))
        self.pushButton_Fy_Fz.setText(_translate("MainWindow", " |Fz|-|Fy|"))
        self.pushButton_normFy_Fz.setText(_translate("MainWindow", "norm Fz-Fy"))
        self.pushButton_Mx_Vtot.setText(_translate("MainWindow", "|Mx|-Vtot"))
        self.checkBox_pltAnnot.setText(_translate("MainWindow", "plot annotation"))
        self.pushButton_print.setText(_translate("MainWindow", "Print report"))
        self.pushButton_info.setText(_translate("MainWindow", "App info"))
        self.actionLoadXLS.setText(_translate("MainWindow", "Load xls data"))
