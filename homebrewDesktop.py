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

    def addRecipe(self, recipe):
        recipe_num = 1
        original_name = recipe.name
    
        while recipe.name in self.recipes.keys():
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
        newRec = Recipe(name, {}, [])

        #get all ingredients
        try:
            for i in range(self.ingreRows):
                ingre = ui.tableWidget.item(i,0).text()
                try:
                    amnt = int(ui.tableWidget.item(i, 1).text())
                except:
                    amnt = 0
                
                try:
                    stage = ui.tableWidget.item(i,3).text()
                except:
                    stage = "none"
                newRec.addIngredient(ingre,amnt,stage)

        except:
            print("an error occured when reading ingredients")

        newRec.toJson(name)
        self.addRecipe(newRec)

    def setIngredientRows(self, ui):
        self.ingreRows+=1
        ui.tableWidget.setRowCount(self.ingreRows)

    def setInstructionRows(self, ui):
        self.instrRows+=1
        ui.tableWidget_2.setRowCount(self.instrRows)

    def getRecipeFromFile(self, fn):
        i = os.getcwd()+"\\"+fn+".json"

        with open(i, "r") as fo:
            recipeDict = json.load(fo)

        print(str(recipeDict))
        return recipeDict

    def sendData():
        pass

    def receiveData():
        pass
        
if __name__ == "__main__":
    testHomebrewDesktop = homebrewDesktop()
    # testHomebrewDesktop.getRecipeFromFile("Cool Beer")
    print(testHomebrewDesktop.workingDir)

    # testRecipe = Recipe("YUM BEER", {}, [0])
    # testRecipe2 = Recipe("YUMMIER BEER", {}, [])

    # testRecipe.addIngredient("hops", 4, "fermenter")
    # testRecipe.addIngredient("sugar", 2, "boiling")

    # testRecipe.addInstruction(0, "5 min", 100, "boil", "Add the sugar to the water. Let boil for 5 min")
    # testRecipe.addInstruction(1, "45 min", 27, "ferment", "Time to ferment those hops for 45 mins")

    # testHomebrewDesktop.addRecipe(testRecipe)
    # testHomebrewDesktop.addRecipe(testRecipe2)



    
    testHomebrewDesktop.HomebrewController.show()

    sys.exit(testHomebrewDesktop.app.exec_())