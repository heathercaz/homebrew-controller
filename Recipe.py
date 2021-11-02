class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    def getName(self):
        return self.name

    def getIngredients(self):
        return self.ingredients

    def getInstructions(self):
        return self.instructions

    def setName(self, newName):
        self.name = newName

    def setIngredients(self, newIngredients):
        self.ingredients = newIngredients

    def setInstructions(self, newInstructions):
        self.instructions = newInstructions
                
    def addIngredient():
        pass

    def removeIngredient():
        pass

    def editIngredient():
        pass

    def displayRecipe():
        pass

    def saveRecipe():
        pass

    def deleteRecipe():
        pass