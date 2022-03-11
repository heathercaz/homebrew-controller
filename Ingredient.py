class Ingredient:
    def __init__(self, name, amount, unit, step):
        self.name = name 
        self.amount = amount
        self.unit = unit
        self.step = step

    def __str__(self) -> str:
        return f"NAME: {self.name}  AMOUNT: {self.amount}  step {self.step}"

    def getName(self):
        return self.name

    def getAmount(self):
        return self.amount

    def getStage(self):
        return self.step

    def setName(self, newName):
        self.name = newName

    def setAmount(self, newAmount):
        self.amount = newAmount

    def setStage(self, newStage):
        self.step = newStage
