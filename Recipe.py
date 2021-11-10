from Ingredient import Ingredient
from Instruction import Instruction

class Recipe:
    def __init__(self, name: str, ingredients: dict, instructions: list):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    def __str__(self) -> str:
        ingredientStr = ""
        instructionStr = ""
        for i in self.ingredients.values():
            ingredientStr += f"\tName: {i.name}\tAmount: {i.amount}\tStage: {i.stage}\n"

        j = 0
        for i in self.instructions:
            j+=1
            instructionStr += f"\tStep {j}\n\t{i.direction}\n"
        return f"Recipe name: {self.name} \nIngredients:\n {ingredientStr}\nInstructions: \n{instructionStr}"
    
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

    def addInstruction(self, step: int, time, temp, type, direction):
        newInstruction = Instruction(time, temp, type, direction)
        if step >= len(self.instructions):
            self.instructions.append(newInstruction)
        else:
            self.instructions[step] = newInstruction

    def displayRecipe():
        pass

    def saveRecipe():
        pass

    def deleteRecipe():
        pass

