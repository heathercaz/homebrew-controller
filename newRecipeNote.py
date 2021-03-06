# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\CME495\desktop-app\homebrew-controller\newRecipeNote.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_newRecipeNote(object):
    def setupUi(self, newRecipeNote):
        newRecipeNote.setObjectName("newRecipeNote")
        newRecipeNote.resize(640, 480)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("h:\\CME495\\desktop-app\\homebrew-controller\\../../beerIcone.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        newRecipeNote.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(newRecipeNote)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.dateLabel = QtWidgets.QLabel(newRecipeNote)
        self.dateLabel.setEnabled(True)
        self.dateLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.dateLabel.setFont(font)
        self.dateLabel.setObjectName("dateLabel")
        self.horizontalLayout_1.addWidget(self.dateLabel)
        self.dateText = QtWidgets.QLineEdit(newRecipeNote)
        self.dateText.setMaximumSize(QtCore.QSize(500, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.dateText.setFont(font)
        self.dateText.setObjectName("dateText")
        self.horizontalLayout_1.addWidget(self.dateText)
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.batchLabel = QtWidgets.QLabel(newRecipeNote)
        self.batchLabel.setEnabled(True)
        self.batchLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.batchLabel.setFont(font)
        self.batchLabel.setObjectName("batchLabel")
        self.horizontalLayout_2.addWidget(self.batchLabel)
        self.batchText = QtWidgets.QLineEdit(newRecipeNote)
        self.batchText.setMaximumSize(QtCore.QSize(500, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.batchText.setFont(font)
        self.batchText.setObjectName("batchText")
        self.horizontalLayout_2.addWidget(self.batchText)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.sgLabel = QtWidgets.QLabel(newRecipeNote)
        self.sgLabel.setEnabled(True)
        self.sgLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.sgLabel.setFont(font)
        self.sgLabel.setObjectName("sgLabel")
        self.horizontalLayout_3.addWidget(self.sgLabel)
        self.sgText = QtWidgets.QLineEdit(newRecipeNote)
        self.sgText.setMaximumSize(QtCore.QSize(500, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.sgText.setFont(font)
        self.sgText.setObjectName("sgText")
        self.horizontalLayout_3.addWidget(self.sgText)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.ibuLabel = QtWidgets.QLabel(newRecipeNote)
        self.ibuLabel.setEnabled(True)
        self.ibuLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ibuLabel.setFont(font)
        self.ibuLabel.setObjectName("ibuLabel")
        self.horizontalLayout_4.addWidget(self.ibuLabel)
        self.ibuText = QtWidgets.QLineEdit(newRecipeNote)
        self.ibuText.setMaximumSize(QtCore.QSize(500, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ibuText.setFont(font)
        self.ibuText.setObjectName("ibuText")
        self.horizontalLayout_4.addWidget(self.ibuText)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.abvLabel = QtWidgets.QLabel(newRecipeNote)
        self.abvLabel.setEnabled(True)
        self.abvLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.abvLabel.setFont(font)
        self.abvLabel.setObjectName("abvLabel")
        self.horizontalLayout_6.addWidget(self.abvLabel)
        self.abvText = QtWidgets.QLineEdit(newRecipeNote)
        self.abvText.setMaximumSize(QtCore.QSize(500, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.abvText.setFont(font)
        self.abvText.setObjectName("abvText")
        self.horizontalLayout_6.addWidget(self.abvText)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.noteSection = QtWidgets.QTextEdit(newRecipeNote)
        self.noteSection.setObjectName("noteSection")
        self.verticalLayout.addWidget(self.noteSection)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.doneButton = QtWidgets.QPushButton(newRecipeNote)
        self.doneButton.setObjectName("doneButton")
        self.horizontalLayout.addWidget(self.doneButton)
        self.cancelButton = QtWidgets.QPushButton(newRecipeNote)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(newRecipeNote)
        QtCore.QMetaObject.connectSlotsByName(newRecipeNote)

    def retranslateUi(self, newRecipeNote):
        _translate = QtCore.QCoreApplication.translate
        newRecipeNote.setWindowTitle(_translate("newRecipeNote", "Recipe Notes"))
        self.dateLabel.setText(_translate("newRecipeNote", "Date Brewed:"))
        self.batchLabel.setText(_translate("newRecipeNote", "Batch Size:"))
        self.sgLabel.setText(_translate("newRecipeNote", "SG:"))
        self.ibuLabel.setText(_translate("newRecipeNote", "IBUs:"))
        self.abvLabel.setText(_translate("newRecipeNote", "ABV:"))
        self.noteSection.setPlaceholderText(_translate("newRecipeNote", "Notes"))
        self.doneButton.setText(_translate("newRecipeNote", "Done"))
        self.cancelButton.setText(_translate("newRecipeNote", "Cancel"))
