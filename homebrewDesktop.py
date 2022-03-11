import Ingredient
import Instruction
from Recipe import Recipe
from homebrewGUI import Ui_HomebrewController
from newRecipe import Ui_newRecipe
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys
import os
import json

# pyuic5 -x homebrewGUI.ui -o homebrewGUI.py
class homebrewDesktop():
    def __init__(self):
        self.recipes = {};
        self.workingDir =  os.getcwd()+"/BeerRecipes/"
        self.selectedRecipe = None

        self.app = QtWidgets.QApplication(sys.argv)
        self.HomebrewController = QtWidgets.QMainWindow()
        self.ui = Ui_HomebrewController()

        self.ui.setupUi(self.HomebrewController)

        self.ui.listWidget.itemSelectionChanged.connect(self.previewRecipe)

        self.ui.newRecipeButton.clicked.connect(self.openNewRecipe)
        self.ui.deleteRecipeButton.clicked.connect(self.deleteRecipe)

        self.ui.editRecipeButton.clicked.connect(self.editRecipe)
        self.ui.toolButton.clicked.connect(self.setWorkingDir)
        self.ui.plainTextEdit.setPlainText(self.workingDir)

    def setWorkingDir(self):
        self.workingDir = QtWidgets.QFileDialog.getExistingDirectory(testHomebrewDesktop.HomebrewController, 'Select Working Directory')
        self.ui.plainTextEdit.setPlainText(self.workingDir)
        self.recipes = {}
        self.ui.listWidget.clear()
        self.showSavedRecipes()

    def addRecipe(self, recipe:dict):
        recipe_num = 1
        original_name = recipe.name
        while recipe.name in self.recipes.keys(): # Make sure there are no repeated recipe names
            recipe.name = original_name + str(recipe_num)
            recipe_num+=1

        listItem = QListWidgetItem(recipe.name)
        self.ui.listWidget.addItem(listItem)
        self.recipes[recipe.name] = recipe

        # print(self.recipes)

    def previewRecipe(self):
        try: 
            self.selectedRecipe = self.recipes[self.ui.listWidget.selectedItems()[0].text()]
        except:
            self.selectedRecipe = self.recipes[list(self.recipes.keys())[0]]
        self.ui.recipePreview.setPlainText(self.selectedRecipe.displayRecipe())

    def openNewRecipe(self):
        self.newRecipeDialog = QtWidgets.QDialog()
        ui = Ui_newRecipe()
        ui.setupUi(self.newRecipeDialog)

        ui.doneButton.clicked.connect(lambda: self.saveNewRecipe(ui))
        ui.addInstructionButton.clicked.connect(lambda: self.increaseInstructionRows(ui))
        ui.removeInstructionButton.clicked.connect(lambda: self.decreaseInstructionRows(ui))

        self.instrRows = 1
        # self.instrRows = 1
        self.newRecipeDialog.show()
        
    # Get's the recipe Name
    def getRecipeName(self, ui):
        try:
            return ui.recipeName.text()

        except:
            return "untitled"

    # TODO adjust for new gui layout
    def saveNewRecipe(self, ui):
        name = self.getRecipeName(ui)
        newRec = Recipe(name, {}, {},[])

        #get all instructions from the table

        step = 1
        for i in range(self.instrRows):
            try:
                ingre = ui.tableWidget.item(i,0).text()
            except:
                ingre = None

            try:
                amnt = float(ui.tableWidget.item(i, 1).text())
            except:
                amnt = 0

            try:
                unit = ui.tableWidget.item(i,2).text()
            
            except:
                unit = None

            try:
                temp = float(ui.tableWidget.item(i, 3).text())
            except:
                temp = 0

            try:
                time = ui.tableWidget.item(i,4).text()
                
            except:
                time = "0 min"

            try:
                stage = ui.tableWidget.item(i,5).text()
            except:
                stage = None
                print("error adding stage")

            try: 
                note = ui.tableWidget.item(i,6).text()
            except:
                note = None
                print("error adding Note")

            if ingre:
                newRec.addIngredient(ingre,amnt,unit,stage)
            newRec.addInstruction(step, time, temp, stage, note)
            step+=1

        newRec.toJson(name)
        self.addRecipe(newRec)


    def increaseInstructionRows(self, ui):
        self.instrRows+=1
        ui.tableWidget.setRowCount(self.instrRows)

    def decreaseInstructionRows(self, ui):
        self.instrRows-=1
        ui.tableWidget.setRowCount(self.instrRows)

    def showSavedRecipes(self):
        print("loading recipes...")
        # TODO Change Beer Recipes to selected directory
        direct = self.workingDir
        # direct = os.getcwd()+"\\BeerRecipes\\"  # Get recipes from Directory. 
        recipeDict = {}

        for filename in os.listdir(direct):
            i = os.path.join(direct, filename)
            if os.path.isfile(i) == False:
                print("error")

            with open(i, "r") as fo:
                recipeDict = json.load(fo) # load json file into a dictionary

            recipeName = recipeDict['name']
            recipeIngredients = recipeDict['ingredients']
            recipeInstructions = recipeDict['instructions']
            recipeArray = recipeDict['array']

            loadedRecipe = Recipe(recipeName, recipeIngredients, recipeInstructions, recipeArray)
            self.addRecipe(loadedRecipe)
            # print(str(recipeDict))
        return recipeDict

    def deleteRecipe(self):
        direct = self.workingDir
        selectedRecipe = self.ui.listWidget.selectedItems()[0]
        recipeFile = selectedRecipe.text()+'.json'

        if not selectedRecipe:
            return

        # print(os.listdir(direct))
        if recipeFile in os.listdir(direct):
            # remove from files
            os.remove(direct + recipeFile)
            
            #remove from recipe dictionary
            self.recipes.pop(selectedRecipe.text())

            # delete from list widget in gui
            ind = self.ui.listWidget.currentIndex().row()
            self.ui.listWidget.takeItem(ind)

        else:
            print("The file: " + recipeFile +"does not exist")


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
            
            #get ingredients
            for ingr in ingredientsList:
                if row + 1 == thisRecipe.ingredients[ingr].step:
                    name = QTableWidgetItem(thisRecipe.ingredients[ingr].name)
                    amnt = QTableWidgetItem(thisRecipe.ingredients[ingr].amount)
                    unit = QTableWidgetItem(thisRecipe.ingredients[ingr].unit)
                    ingredientsList.remove(ingr)

                    ui.tableWidget.setItem(row, 0, name)
                    ui.tableWidget.setItem(row, 1, amnt)
                    ui.tableWidget.setItem(row, 2, unit)
                    break
            
            #get instructions
            dur = QTableWidgetItem(thisRecipe.instructions[row + 1].time)
            temp = QTableWidgetItem(thisRecipe.instructions[row + 1].temp)
            stage = QTableWidgetItem(thisRecipe.instructions[row + 1].type)
            note = QTableWidgetItem(thisRecipe.instructions[row + 1].direction)

            #populate table

            ui.tableWidget.setItem(row,3, temp)
            ui.tableWidget.setItem(row,4, dur)
            ui.tableWidget.setItem(row,5, stage)
            ui.tableWidget.setItem(row,6, note)

        ui.doneButton.clicked.connect(lambda: self.saveNewRecipe(ui))
        ui.addInstructionButton.clicked.connect(lambda: self.increaseInstructionRows(ui))
        ui.removeInstructionButton.clicked.connect(lambda: self.decreaseInstructionRows(ui))

        self.instrRows = 1
        self.newRecipeDialog.show()


    def sendData():
        pass

    def receiveData():
        pass
        
if __name__ == "__main__":
    testHomebrewDesktop = homebrewDesktop()
    testHomebrewDesktop.showSavedRecipes()

    testHomebrewDesktop.HomebrewController.show()

    sys.exit(testHomebrewDesktop.app.exec_())
