from Ingredient import Ingredient
from Instruction import Instruction
from brewHistory import BrewHistory
import json

class Recipe:
    def __init__(self, name: str, ingredients: dict, instructions: dict, brewHistroy: list, tempUnit: str):
        self.name = name
        self.ingredients = {}
        self.tempUnit = tempUnit
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
        self.brewHistory = []
        for i in brewHistroy:
            newHist = BrewHistory(i[0], i[1], i[2], i[3], i[4], i[5])
            self.brewHistory.append(newHist)

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
        historyList = []

        for i in self.ingredients.values():
            ingredientDict[i.name] = [i.name, i.amount, i.unit, i.step]
        
        j = 0
        for i in self.instructions.values():
            j+=1
            instructionDict[j] = [i.time, i.temp, i.type, i.direction]

        try:
            for i in self.brewHistory:
                historyList.append([i.date, i.batchSize, i.sg, i.ibu, i.abv, i.notes])
        except:
            pass

        recipeDict["name"] = self.name
        recipeDict["ingredients"] = ingredientDict
        recipeDict["instructions"] = instructionDict
        recipeDict["history"] = historyList
        recipeDict["tempUnit"] = self.tempUnit

        with open(filename + ".json", "w") as outfile:
            json.dump(recipeDict, outfile)

    def toSerial(self, ferm):
        stages = ["none","preheat", "heating", "mashing", "sparging",  "chilling", "fermenting", "fermenter1", "fermenter2", "fermenter3"]
        serialArr = ['!'.encode() , bytes([len(self.instructions)])]
        step = 1;

        for i in self.instructions.values():
            try:
                time = int(i.time[:-1])
                # time = 0
                timeUnit = i.time[-1]
            except:
                time = 0
                timeUnit = 'm'

            try:
                stage = stages.index(i.type.lower())
                if stage == stages.index("fermenting"):
                    if ferm == 1:
                        stage = stages.index("fermenter1")
                    elif ferm == 2:
                        stage = stages.index("fermenter2")
                    elif ferm == 3:
                        stage = stages.index("fermenter3")

            except:
                stage = 0

            
            try:
                temp = int(i.temp)

            except:
                temp = 0

            #convert to celcius
            if self.tempUnit.lower() == "f":
                    contemp = (temp - 32) * (5/9)
            elif self.tempUnit.lower() == "c":
                    contemp = temp
            else:
                contemp = 0

            if contemp < 0:
                contemp = 0

            serialArr+=['#'.encode(), bytes([step]), bytes([time]), timeUnit.encode(), bytes([int(contemp)]), bytes([stage]), '&'.encode()]
            step+= 1
        return serialArr


    def addBrewHistory(self, history):
        self.brewHistory.append(history)

    
    def removeBrewHistory(self, num):
        self.brewHistory.pop(num)


if __name__ == "__main__":
    pass