import Ingredient
import Instruction
from Recipe import Recipe
from homebrewGUI import Ui_HomebrewController
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

# pyuic5 -x homebrewGUI.ui -o homebrewGUI.py
class homebrewDesktop:
    def __init__(self):
        self.recipes = {};

        self.app = QtWidgets.QApplication(sys.argv)
        self.HomebrewController = QtWidgets.QMainWindow()
        self.ui = Ui_HomebrewController()

        self.ui.setupUi(self.HomebrewController)

        self.ui.listWidget.itemSelectionChanged.connect(self.previewRecipe)

        pass

    def addRecipe(self, recipe):
        self.recipes[recipe.name] = recipe
        self.ui.listWidget.addItem(recipe.name)

    def previewRecipe(self):
        selectedRecipe = self.recipes[self.ui.listWidget.selectedItems()[0].text()]
        self.ui.recipePreview.setPlainText(str(selectedRecipe))

    def sendData():
        pass

    def receiveData():
        pass


if __name__ == "__main__":
    testHomebrewDesktop = homebrewDesktop()



    testRecipe = Recipe("YUM BEER", {}, [])
    testRecipe2 = Recipe("YUMMIER BEER", {}, [])

    testRecipe.addIngredient("hops", 4, "fermenter")
    testRecipe.addIngredient("sugar", 2, "boiling")

    testHomebrewDesktop.addRecipe(testRecipe)
    testHomebrewDesktop.addRecipe(testRecipe2)
    # currentItem = testHomebrewDesktop.ui.listWidget.itemClicked['QListWidgetItem*']
    # testHomebrewDesktop.previewRecipe(currentItem)
    # testHomebrewDesktop.previewRecipe(testRecipe)
    

    print(testRecipe)
    testHomebrewDesktop.HomebrewController.show()

    sys.exit(testHomebrewDesktop.app.exec_())