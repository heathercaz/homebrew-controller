class Ingredient:
    def __init__(self, name, amount, unit, stage):
        self.name = name 
        self.amount = amount
        self.unit = unit
        self.stage = stage

    def __str__(self) -> str:
        return f"NAME: {self.name}  AMOUNT: {self.amount}  STAGE {self.stage}"

    def getName(self):
        return self.name

    def getAmount(self):
        return self.amount

    def getStage(self):
        return self.stage

    def setName(self, newName):
        self.name = newName

    def setAmount(self, newAmount):
        self.amount = newAmount

    def setStage(self, newStage):
        self.stage = newStage
