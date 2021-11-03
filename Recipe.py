from Ingredient import Ingredient
from Instruction import Instruction

class Recipe:
    def __init__(self, name: str, ingredients: dict, instructions: list):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    def __str__(self) -> str:
        ingredientStr = ""
        for i in self.ingredients.values():
            ingredientStr += f"Name: {i.name} Amount: {i.amount} Stage: {i.stage}\n"
        return f"Recipe name: {self.name} \nIngredients: {ingredientStr}Instructions: {self.instructions}"
    
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
                
    def addIngredient(self, name, amount, stage):
        newIngredient = Ingredient(name, amount, stage);
        self.ingredients[name] = newIngredient

    def removeIngredient(self, name):
        if name not in self.ingredients:
            return

        del(self.ingredients[name])

    def editIngredient(self, name, newName, newAmount, newStage):
        if name in self.ingredients:
            self.ingredients[name].name = newName
            self.ingredients[name].amount = newAmount
            self.ingredients[name].stage = newStage

    def displayRecipe():
        pass

    def saveRecipe():
        pass

    def deleteRecipe():
        pass

testRecipe = Recipe("YUM BEER", {}, [])

testRecipe.addIngredient("hops", 4, "fermenter")
testRecipe.addIngredient("sugar", 2, "boiling")

print(testRecipe)

