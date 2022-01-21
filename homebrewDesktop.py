import Ingredient
import Instruction
from Recipe import Recipe
from homebrewGUI import Ui_HomebrewController
from newRecipe import Ui_newRecipe
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import json

# pyuic5 -x homebrewGUI.ui -o homebrewGUI.py
class homebrewDesktop():
    def __init__(self):
        self.recipes = {};
        self.workingDir =  os.getcwd()

        self.app = QtWidgets.QApplication(sys.argv)
        self.HomebrewController = QtWidgets.QMainWindow()
        self.ui = Ui_HomebrewController()

        self.ui.setupUi(self.HomebrewController)

        self.ui.listWidget.itemSelectionChanged.connect(self.previewRecipe)

        self.ui.newRecipeButton.clicked.connect(self.openNewRecipe)

        pass

    def setWorkingDir(self):
        self.workingDir = QtWidgets.QFileDialog.getExistingDirectory(testHomebrewDesktop.HomebrewController, 'Hey! Select a File')
        pass

    def addRecipe(self, recipe:dict):
        recipe_num = 1
        original_name = recipe.name
        while recipe.name in self.recipes.keys(): # Make sure there are no repeated recipe names
            recipe.name = original_name + str(recipe_num)
            recipe_num+=1

        self.ui.listWidget.addItem(recipe.name)
        self.recipes[recipe.name] = recipe

        print(self.recipes)

    def previewRecipe(self):
        selectedRecipe = self.recipes[self.ui.listWidget.selectedItems()[0].text()]
        self.ui.recipePreview.setPlainText(selectedRecipe.displayRecipe())

    def openNewRecipe(self):
        self.newRecipeDialog = QtWidgets.QDialog()
        ui = Ui_newRecipe()
        ui.setupUi(self.newRecipeDialog)

        ui.doneButton.clicked.connect(lambda: self.saveNewRecipe(ui))
        ui.addIngredientButton.clicked.connect(lambda: self.setIngredientRows(ui))
        ui.addInstructionButton.clicked.connect(lambda: self.setInstructionRows(ui))

        self.ingreRows = 1
        self.instrRows = 1
        self.newRecipeDialog.show()
        
    def getRecipeName(self, ui):
        try:
            return ui.recipeName.text()

        except:
            return "untitled"

    def saveNewRecipe(self, ui):
        name = self.getRecipeName(ui)
        newRec = Recipe(name, {}, {})

        #get all ingredients
        try:
            for i in range(self.ingreRows):
                ingre = ui.tableWidget.item(i,0).text()
                try:
                    amnt = float(ui.tableWidget.item(i, 1).text())
                except:
                    amnt = 0
                    print("error adding amount")
                
                try:
                    stage = ui.tableWidget.item(i,3).text()
                except:
                    stage = "none"
                    print("error adding stage")
                newRec.addIngredient(ingre,amnt,stage)

        except:
            print("an error occured when reading ingredients")

        #get all ingredients
        step = 1
        print("instruction rows" + str(self.instrRows))
        for i in range(self.instrRows):
            try:
                time = ui.tableWidget_2.item(i,0).text()
                
            except:
                time = "0 min"
                print("error getting time")

            try:
                temp = float(ui.tableWidget_2.item(i, 1).text())
            except:
                temp = 0
                print("error adding amount")
            
            try:
                stage = ui.tableWidget_2.item(i,2).text()
            except:
                stage = "none"
                print("error adding stage")

            try: 
                note = ui.tableWidget_2.item(i,3).text()
            except:
                note = None
                print("error adding Note")
            
            newRec.addInstruction(step, time, temp, stage, note)
            step+=1

        newRec.toJson(name)
        self.addRecipe(newRec)

    def saveRecipe(self, recipe):
        recipe.toJson(recipe.name)

    def setIngredientRows(self, ui):
        self.ingreRows+=1
        ui.tableWidget.setRowCount(self.ingreRows)

    def setInstructionRows(self, ui):
        self.instrRows+=1
        ui.tableWidget_2.setRowCount(self.instrRows)

    def showSavedRecipes(self):
        print("loading recipes...")
        # TODO Change Beer Recipes to selected directory
        direct = os.getcwd()+"\\BeerRecipes\\"  # Get recipes from Directory. 

        for filename in os.listdir(direct):
            i = os.path.join(direct, filename)
            if os.path.isfile(i) == False:
                print("error")

            with open(i, "r") as fo:
                recipeDict = json.load(fo) # load json file into a dictionary

            recipeName = recipeDict['name']
            recipeIngredients = recipeDict['ingredients']
            recipeInstructions = recipeDict['instructions']

            loadedRecipe = Recipe(recipeName, recipeIngredients, recipeInstructions)
            self.addRecipe(loadedRecipe)
            print(str(recipeDict))
        return recipeDict

    def sendData():
        pass

    def receiveData():
        pass
        
if __name__ == "__main__":
    testHomebrewDesktop = homebrewDesktop()
    testHomebrewDesktop.showSavedRecipes()
    print(testHomebrewDesktop.workingDir)

    testHomebrewDesktop.HomebrewController.show()

    sys.exit(testHomebrewDesktop.app.exec_())
