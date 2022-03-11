from Ingredient import Ingredient
from Instruction import Instruction
import json

class Recipe:
    def __init__(self, name: str, ingredients: dict, instructions: dict):
        self.name = name

        self.ingredients = {}
        # check ingredient type
        for i in ingredients.values(): 
            if isinstance(i, list):
                newIngred = Ingredient(i[0], i[1], i[2], i[3])
                self.ingredients[i[0]] = newIngred
            elif isinstance(i, Ingredient):
                self.ingredients[i.name] = i
            else:
                print("error adding ingredients")

        self.instructions = {}
        # check instruction type
        instrNum = 1

        if type(instructions) is not dict:
            return 0

        for i in instructions.values(): 
            # print("instructions type " + str(type(i)) + "instructions: " + str(i))
            if isinstance(i, list):
                try:
                    newInstr = Instruction(i[0], i[1], i[2], i[3])
                except:
                    newInstr = Instruction(None, None, None, None)
                    print("Error adding instructions of: " +  str(self.name))

                self.instructions[instrNum] = newInstr
            elif isinstance(i, Instruction):
                self.instructions[instrNum] = i
            else:
                print("error adding instruction " + str(instrNum))
            instrNum+=1
        

    def __str__(self) -> str:

        ingredientStr = ""
        instructionStr= ""
        for i in self.ingredients.values():
            ingredientStr += f"Name:{i.name} Amount:{i.amount} Stage:{i.stage}, "
        j = 0
        for i in self.instructions.values():
            j+=1
            instructionStr += f"Step {j}: {i.direction},"

        return f"Recipe name: {self.name}\nIngredients:[{ingredientStr}]\nInstructions:\n[{instructionStr}]"

    
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
                
    def addIngredient(self, name, amount, unit, stage):
        newIngredient = Ingredient(name, amount, unit, stage);
        self.ingredients[name] = newIngredient

    def removeIngredient(self, name):
        if name not in self.ingredients:
            return

        del(self.ingredients[name])

    def editIngredient(self, name, newName, newAmount, newUnit, newStage):
        if name in self.ingredients:
            self.ingredients[name].name = newName
            self.ingredients[name].amount = newAmount
            self.ingredients[name].stage = newStage
            self.ingredients[name].unit = newUnit

    def addInstruction(self, step: int, time, temp, type, direction):
        newInstruction = Instruction(time, temp, type, direction)
        # if step >= len(self.instructions):
        #     self.instructions.append(newInstruction)
        # else:
        self.instructions[step] = newInstruction

    def displayRecipe(self):
        ingredientStr = ""
        instructionStr = ""

        print("values " + str(self.ingredients))
        for i in self.ingredients.values():
            print(i)
            ingredientStr += f"\t{i.amount} {i.unit}\t{i.name}\n"

        j = 0
        for i in self.instructions.values():
            j+=1
            instructionStr += f"Step {j}\t{i.direction}\n"
        return f"Recipe name: {self.name} \nIngredients:\n {ingredientStr}\nInstructions: \n{instructionStr}"

    def toJson(self, filename):
        recipeDict = {}
        ingredientDict = {}
        instructionDict= {}

        for i in self.ingredients.values():
            ingredientDict[i.name] = [i.name, i.amount, i.unit, i.step]
        j = 0
        for i in self.instructions.values():
            j+=1
            instructionDict[j] = [i.time, i.temp, i.type, i.direction]

        recipeDict["name"] = self.name
        recipeDict["ingredients"] = ingredientDict
        recipeDict["instructions"] = instructionDict

        with open(filename + ".json", "w") as outfile:
            json.dump(recipeDict, outfile)

    def toSerial(self):
        pass

if __name__ == "__main__":
    testRecipe = Recipe("YUM BEER", {}, [0])
    testRecipe2 = Recipe("YUMMIER BEER", {}, [])

    testRecipe.addIngredient("hops", 4, "fermenter")
    testRecipe.addIngredient("sugar", 2, "boiling")

    testRecipe.addInstruction(0, "5 min", 100, "boil", "Add the sugar to the water. Let boil for 5 min")
    testRecipe.addInstruction(1, "45 min", 27, "ferment", "Time to ferment those hops for 45 mins")
    print(str(testRecipe))