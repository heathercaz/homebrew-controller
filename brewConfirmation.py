# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\CME495\desktop-app\homebrew-controller\brewConfirmation.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_brewConfirmationDialog(object):
    def setupUi(self, brewConfirmationDialog):
        brewConfirmationDialog.setObjectName("brewConfirmationDialog")
        brewConfirmationDialog.resize(400, 300)
        self.label = QtWidgets.QLabel(brewConfirmationDialog)
        self.label.setGeometry(QtCore.QRect(0, 50, 401, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayoutWidget = QtWidgets.QWidget(brewConfirmationDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(70, 120, 260, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton_3 = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_3.setChecked(True)
        self.radioButton_3.setObjectName("radioButton_3")
        self.horizontalLayout.addWidget(self.radioButton_3)
        self.ferm2 = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.ferm2.setObjectName("ferm2")
        self.horizontalLayout.addWidget(self.ferm2)
        self.ferm3 = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.ferm3.setObjectName("ferm3")
        self.horizontalLayout.addWidget(self.ferm3)
        self.label_2 = QtWidgets.QLabel(brewConfirmationDialog)
        self.label_2.setGeometry(QtCore.QRect(70, 100, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(brewConfirmationDialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(120, 200, 160, 80))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.yesButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.yesButton.setObjectName("yesButton")
        self.horizontalLayout_2.addWidget(self.yesButton)
        self.noButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.noButton.setObjectName("noButton")
        self.horizontalLayout_2.addWidget(self.noButton)

        self.retranslateUi(brewConfirmationDialog)
        QtCore.QMetaObject.connectSlotsByName(brewConfirmationDialog)

    def retranslateUi(self, brewConfirmationDialog):
        _translate = QtCore.QCoreApplication.translate
        brewConfirmationDialog.setWindowTitle(_translate("brewConfirmationDialog", "Ready to brew?"))
        self.label.setText(_translate("brewConfirmationDialog", "Ready to brew?"))
        self.radioButton_3.setText(_translate("brewConfirmationDialog", "Fermentor 1"))
        self.ferm2.setText(_translate("brewConfirmationDialog", "Fermentor 2"))
        self.ferm3.setText(_translate("brewConfirmationDialog", "Fermentor 3"))
        self.label_2.setText(_translate("brewConfirmationDialog", "Select Fermentor:"))
        self.yesButton.setText(_translate("brewConfirmationDialog", "Yes"))
        self.noButton.setText(_translate("brewConfirmationDialog", "No"))
