#import classes
from Recipe import Recipe
from brewHistory import BrewHistory

#Import GUI fils
from homebrewGUI import Ui_HomebrewController
from newRecipe import Ui_newRecipe
from newRecipeNote import Ui_newRecipeNote
from brewConfirmation import Ui_brewConfirmationDialog
from deleteConfirmation import Ui_DeleteConfirmationDialog
from recipeNotes import Ui_recipeNotes
from fileConfirmation import Ui_OverwriteDialog

#import necessary PyQt libraries
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

#import other libraries
import sys
import os
import json
import time
import serial
import time

class homebrewDesktop():
    def __init__(self):
        self.recipes = {}
        self.workingDir = os.getcwd()
        self.selectedRecipe = None

        self.app = QtWidgets.QApplication(sys.argv)
        self.HomebrewController = QtWidgets.QMainWindow()
        self.ui = Ui_HomebrewController()

        self.ui.setupUi(self.HomebrewController)

        self.showSavedRecipes()

        try:
            self.selectedRecipe = self.recipes[self.ui.listWidget.selectedItems()[
                0].text()]
        except:
            if len(self.recipes) > 0:
                self.selectedRecipe = self.recipes[list(self.recipes.keys())[0]]
            else:
                self.selectedRecipe = Recipe("None Selected", {}, {}, [])
            

        self.ui.listWidget.itemSelectionChanged.connect(self.previewRecipe)

        self.ui.newRecipeButton.clicked.connect(self.openNewRecipe)
        self.ui.deleteRecipeButton.clicked.connect(self.openDeleteConfirmation)
        self.ui.editRecipeButton.clicked.connect(self.editRecipe)
        self.ui.pushButton.clicked.connect(self.openBrewConfirmation)

        self.ui.notesButton.clicked.connect(self.openRecipeNotes)
        self.currNote = 0
        self.maxCurrNote = 0

        self.ui.toolButton.clicked.connect(self.setWorkingDir)
        self.ui.plainTextEdit.setPlainText(self.workingDir)

    def setWorkingDir(self):
        self.workingDir = QtWidgets.QFileDialog.getExistingDirectory(
            testHomebrewDesktop.HomebrewController, 'Select Working Directory')
        self.ui.plainTextEdit.setPlainText(self.workingDir)
        self.recipes = {}
        self.ui.listWidget.clear()
        self.showSavedRecipes()

    def addRecipe(self, recipe: dict):
        recipe_num = 1
        original_name = recipe.name
        while recipe.name in self.recipes.keys():  # Make sure there are no repeated recipe names
            recipe.name = original_name + str(recipe_num)
            recipe_num += 1

        listItem = QListWidgetItem(recipe.name)
        self.ui.listWidget.addItem(listItem)
        self.recipes[recipe.name] = recipe

        return recipe.name

    def previewRecipe(self):
        try:
            self.selectedRecipe = self.recipes[self.ui.listWidget.selectedItems()[
                0].text()]
        except:
            if len(self.recipes) > 0:
                self.selectedRecipe = self.recipes[list(self.recipes.keys())[0]]
            else:
                self.selectedRecipe = Recipe("None Selected", {}, {}, [])
            
        self.ui.recipePreview.setPlainText(self.selectedRecipe.displayRecipe())

    def openNewRecipe(self):
        self.newRecipeDialog = QtWidgets.QDialog()
        ui = Ui_newRecipe()
        ui.setupUi(self.newRecipeDialog)

        ui.doneButton.clicked.connect(lambda: self.openFileConfirmation(ui))
        ui.addInstructionButton.clicked.connect(
            lambda: self.increaseInstructionRows(ui))
        ui.removeInstructionButton.clicked.connect(
            lambda: self.decreaseInstructionRows(ui))
        ui.cancelButton.clicked.connect(self.newRecipeDialog.close)

        self.instrRows = 1
        self.newRecipeDialog.show()

    def openDeleteConfirmation(self):
        self.deleteConfirmationDialog = QtWidgets.QDialog()
        ui = Ui_DeleteConfirmationDialog()
        ui.setupUi(self.deleteConfirmationDialog)

        filename = self.selectedRecipe.getName()
        # print(filename)
        ui.label.setText("Are you sure you want to delete " + filename + "?")

        ui.yesButton.clicked.connect(lambda: self.deleteRecipe(filename))
        ui.yesButton.clicked.connect(self.deleteConfirmationDialog.close)
        ui.noButton.clicked.connect(self.deleteConfirmationDialog.close)
        self.deleteConfirmationDialog.show()

    def openBrewConfirmation(self):
        self.brewConfirmationDialog = QtWidgets.QDialog()
        ui = Ui_brewConfirmationDialog()
        ui.setupUi(self.brewConfirmationDialog)

        ui.yesButton.clicked.connect(self.brewConfirmationDialog.close)
        ui.sendButton.clicked.connect(lambda: self.sendData(ui))

        self.brewConfirmationDialog.show()

    def openFileConfirmation(self, editorUi):
        self.fileConfirmationDialog = QtWidgets.QDialog()
        ui = Ui_OverwriteDialog()
        ui.setupUi(self.fileConfirmationDialog)
        filename = self.getRecipeName(editorUi)

        if filename in self.recipes.keys():
            ui.setMsgText(filename + " already exists. Would you like to overwrite?",
                          "(Clicking \"No\" will create a numbered copy of the file)")
        else:
            ui.setMsgText("Save file as " + filename + ".json?", " ")

        ui.yesButton.clicked.connect(self.fileConfirmationDialog.close)
        ui.yesButton.clicked.connect(
            lambda: self.overwriteRecipe(filename, editorUi))

        ui.noButton.clicked.connect(lambda: self.saveNewRecipe(editorUi))
        ui.noButton.clicked.connect(self.fileConfirmationDialog.close)

        ui.cancelButton.clicked.connect(self.fileConfirmationDialog.close)
        self.fileConfirmationDialog.show()

    def prevNote(self, ui):
        if self.currNote > 0:
            self.currNote-=1
        self.updateNoteDisplay(ui)

    def nextNote(self,ui):
        print(str(self.currNote) + " : " + str(self.maxCurrNote))
        if self.currNote < self.maxCurrNote - 1:
            self.currNote+=1
        self.updateNoteDisplay(ui)
        
    def updateNoteDisplay(self, ui):

        try:
            recipeNote = self.selectedRecipe.brewHistory[self.currNote]
        except:
            recipeNote = None

        try:
            date = recipeNote.date
        except:
            date = None

        try:
            batchSize = recipeNote.batchSize
        except:
            batchSize = 0

        try:
            sg = recipeNote.sg
        except:
            sg = None

        try:
            ibu = recipeNote.ibu
        except:
            ibu = None

        try:
            abv = recipeNote.abv
        except:
            abv = None

        try:
            notes = recipeNote.notes
        except:
            notes = None

        ui.dateText.setText(str(date))
        ui.batchText.setText(str(batchSize))
        ui.sgText.setText(str(sg))
        ui.ibuText.setText(str(ibu))
        ui.abvText.setText(str(abv))
        ui.noteSection_2.setText(str(notes))

    def openRecipeNotes(self):
        self.recipeNotesDialog = QtWidgets.QDialog()
        ui = Ui_recipeNotes()
        ui.setupUi(self.recipeNotesDialog)
        self.currNote = 0
        self.maxCurrNote = len(self.selectedRecipe.brewHistory)

        self.updateNoteDisplay(ui)

        ui.cancelButton.clicked.connect(self.recipeNotesDialog.close)
        ui.newButton.clicked.connect(self.openNewRecipeNote)

        ui.prevButton.clicked.connect(lambda:self.prevNote(ui))
        ui.nextButton.clicked.connect(lambda:self.nextNote(ui))

        self.recipeNotesDialog.show()


    def openNewRecipeNote(self):
        self.newRecipeNotesDialog = QtWidgets.QDialog()
        ui = Ui_newRecipeNote()
        ui.setupUi(self.newRecipeNotesDialog)

        ui.cancelButton.clicked.connect(self.newRecipeNotesDialog.close)
        ui.doneButton.clicked.connect(lambda: self.addNewRecipeNote(ui))
        ui.doneButton.clicked.connect(self.newRecipeNotesDialog.close)
        self.newRecipeNotesDialog.show()

    def addNewRecipeNote(self, ui):
        # TODO finish this
        try:
            selectedRecipe = self.recipes[self.ui.listWidget.selectedItems()[
                0].text()]
        except:
            selectedRecipe = self.recipes[list(self.recipes.keys())[0]]

        try:
            date = ui.dateText.text()
        except:
            date = None

        try:
            batchSize = ui.batchText.text()
        except:
            batchSize = None

        try:
            sg = ui.sgText.text()
        except:
            sg = None

        try:
            ibu = ui.ibuText.text()
        except:
            ibu = None

        try:
            abv = ui.abvText.text()
        except:
            abv = None

        try:
            notes = ui.noteSection.toPlainText()
        except:
            notes = None

        newBrewHistory = BrewHistory(date, batchSize, sg, ibu, abv, notes)
        selectedRecipe.addBrewHistory(newBrewHistory)
        self.overwriteRecipe(selectedRecipe.name, None)
        newName = self.workingDir+"/"+self.addRecipe(selectedRecipe)
        selectedRecipe.toJson(newName )
        print(str(selectedRecipe.brewHistory))

    # Get's the recipe Name

    def getRecipeName(self, ui):
        try:
            if ui.recipeName.text() == "":
                return "untitled"
            else:
                return ui.recipeName.text()

        except:
            return "untitled"

    def saveNewRecipe(self, ui):
        name = self.getRecipeName(ui)
        newRec = Recipe(name, {}, {}, [])

        # get all instructions from the table

        step = 1
        for i in range(self.instrRows):
            try:
                ingre = ui.tableWidget.item(i, 0).text()
            except:
                ingre = None

            try:
                amnt = float(ui.tableWidget.item(i, 1).text())
            except:
                amnt = None

            try:
                unit = ui.tableWidget.item(i, 2).text()

            except:
                unit = None

            try:
                temp = float(ui.tableWidget.item(i, 3).text())
            except:
                temp = None

            try:
                time = ui.tableWidget.item(i, 4).text()

            except:
                time = None

            try:
                stage = ui.tableWidget.item(i, 5).text()
            except:
                stage = None

            try:
                note = ui.tableWidget.item(i, 6).text()
            except:
                note = None

            if ingre:
                newRec.addIngredient(ingre, amnt, unit, step)
            newRec.addInstruction(step, time, temp, stage, note)
            step += 1
        newName = self.workingDir+self.addRecipe(newRec)
        newRec.toJson(newName)
        self.newRecipeDialog.close()

    def increaseInstructionRows(self, ui):
        self.instrRows += 1
        ui.tableWidget.setRowCount(self.instrRows)

    def decreaseInstructionRows(self, ui):
        if self.instrRows == 0:
            self.instrRows = 0
        else:
            self.instrRows -= 1
        ui.tableWidget.setRowCount(self.instrRows)

    def showSavedRecipes(self):
        print("loading recipes...")
        direct = self.workingDir

        recipeDict = {}

        for filename in os.listdir(direct):
            i = os.path.join(direct, filename)
            if os.path.isfile(i) == False:
                continue

            try:
                with open(i, "r") as fo:
                    # load json file into a dictionary
                    recipeDict = json.load(fo)
            except:
                continue

            recipeName = recipeDict['name']
            recipeIngredients = recipeDict['ingredients']
            recipeInstructions = recipeDict['instructions']
            recipeHistory = recipeDict['history']

            print(recipeHistory)

            loadedRecipe = Recipe(
                recipeName, recipeIngredients, recipeInstructions, recipeHistory)
            self.addRecipe(loadedRecipe)
            print(str(loadedRecipe.brewHistory))
        return recipeDict

    def overwriteRecipe(self, filename, editorUi):
        direct = self.workingDir + "/"
        recipeFile = filename+'.json'
        # print(os.listdir(direct))
        if recipeFile in os.listdir(direct):
            # remove from files
            os.remove(direct + recipeFile)

            # remove from recipe dictionary
            self.recipes.pop(filename)

            # delete from list widget in gui
            ind = self.ui.listWidget.currentIndex().row()
            self.ui.listWidget.takeItem(ind)

        else:
            print("The file: " + recipeFile + " does not exist")
        if editorUi == None:
            return
        else:
            self.saveNewRecipe(editorUi)

    def deleteRecipe(self, selectedRecipe):
        direct = self.workingDir
        recipeFile = selectedRecipe+'.json'

        if not selectedRecipe:
            return

        # print(os.listdir(direct))
        if recipeFile in os.listdir(direct):
            # remove from files
            os.remove(direct + recipeFile)

            # remove from recipe dictionary
            self.recipes.pop(selectedRecipe)

            # delete from list widget in gui
            ind = self.ui.listWidget.currentIndex().row()
            self.ui.listWidget.takeItem(ind)

        else:
            print("The file: " + recipeFile + "does not exist")

    def editRecipe(self):

        self.newRecipeDialog = QtWidgets.QDialog()
        ui = Ui_newRecipe()
        ui.setupUi(self.newRecipeDialog)

        if self.selectedRecipe is None:
            self.selectedRecipe = self.recipes[list(self.recipes.keys())[0]]

        thisRecipe = self.selectedRecipe
        ui.recipeName.setText(self.selectedRecipe.name)

        ui.tableWidget.setRowCount(len(self.selectedRecipe.instructions))
        ingredientsList = list(thisRecipe.ingredients.keys())

        for row in range(ui.tableWidget.rowCount()):

            # get ingredients
            for ingr in ingredientsList:
                if row + 1 == thisRecipe.ingredients[ingr].step:
                    name = QTableWidgetItem(thisRecipe.ingredients[ingr].name)
                    print(thisRecipe.ingredients[ingr].name)
                    amnt = QTableWidgetItem(
                        str(thisRecipe.ingredients[ingr].amount))
                    unit = QTableWidgetItem(thisRecipe.ingredients[ingr].unit)
                    ingredientsList.remove(ingr)

                    ui.tableWidget.setItem(row, 0, name)
                    ui.tableWidget.setItem(row, 1, amnt)
                    ui.tableWidget.setItem(row, 2, unit)
                    break

            if thisRecipe.instructions[row + 1].temp == None:
                temp = QTableWidgetItem("")
            else:
                temp = QTableWidgetItem(str(thisRecipe.instructions[row + 1].temp))

            # get instructions
            dur = QTableWidgetItem(thisRecipe.instructions[row + 1].time)
            
            stage = QTableWidgetItem(thisRecipe.instructions[row + 1].type)
            note = QTableWidgetItem(thisRecipe.instructions[row + 1].direction)

            # populate table

            ui.tableWidget.setItem(row, 3, temp)
            ui.tableWidget.setItem(row, 4, dur)
            ui.tableWidget.setItem(row, 5, stage)
            ui.tableWidget.setItem(row, 6, note)

        ui.doneButton.clicked.connect(lambda: self.openFileConfirmation(ui))
        ui.addInstructionButton.clicked.connect(
            lambda: self.increaseInstructionRows(ui))
        ui.removeInstructionButton.clicked.connect(
            lambda: self.decreaseInstructionRows(ui))
        ui.cancelButton.clicked.connect(self.newRecipeDialog.close)

        self.instrRows = ui.tableWidget.rowCount()
        self.newRecipeDialog.show()

    def sendData(self, ui):
        ui.statusLabel.setText("Sending data. Do not disconnect")
        #TODO Add com port selection in gui
        ser = serial.Serial('COM3', 9600) #Connect to Com3, baud = 9600
        time.sleep(2) # Need this or race condition will happen!!

        serialArr = self.selectedRecipe.toSerial()
        print(serialArr)
        bytesSent = 0
        for b in serialArr:
            ser.write(b)
            print(b)
            bytesSent+=1
            if bytesSent >= 60:
                time.sleep(1) # give the arduino time to empty buffer
                bytesSent = 0

        #TODO add Fermentor info

        ui.statusLabel.setText("Sending Complete")

    def receiveData(self):
        pass


if __name__ == "__main__":
    testHomebrewDesktop = homebrewDesktop()

    testHomebrewDesktop.HomebrewController.show()

    sys.exit(testHomebrewDesktop.app.exec_())
