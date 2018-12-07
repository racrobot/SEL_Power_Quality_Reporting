# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'statusbar.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_statusBarDialog(object):
    def setupUi(self, statusBarDialog):
        statusBarDialog.setObjectName("statusBarDialog")
        statusBarDialog.resize(400, 209)
        self.statusUpdateLabel = QtWidgets.QLabel(statusBarDialog)
        self.statusUpdateLabel.setGeometry(QtCore.QRect(30, 90, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.statusUpdateLabel.setFont(font)
        self.statusUpdateLabel.setObjectName("statusUpdateLabel")
        self.progressBar = QtWidgets.QProgressBar(statusBarDialog)
        self.progressBar.setGeometry(QtCore.QRect(27, 40, 361, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.statusUpdateValueLabel = QtWidgets.QLabel(statusBarDialog)
        self.statusUpdateValueLabel.setGeometry(QtCore.QRect(30, 120, 341, 71))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(208, 208, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(208, 208, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(208, 208, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(208, 208, 208))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.statusUpdateValueLabel.setPalette(palette)
        self.statusUpdateValueLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.statusUpdateValueLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.statusUpdateValueLabel.setLineWidth(2)
        self.statusUpdateValueLabel.setText("")
        self.statusUpdateValueLabel.setObjectName("statusUpdateValueLabel")

        self.retranslateUi(statusBarDialog)
        QtCore.QMetaObject.connectSlotsByName(statusBarDialog)

    def retranslateUi(self, statusBarDialog):
        _translate = QtCore.QCoreApplication.translate
        statusBarDialog.setWindowTitle(_translate("statusBarDialog", "Progress Bar"))
        self.statusUpdateLabel.setText(_translate("statusBarDialog", "Status Updates:"))

