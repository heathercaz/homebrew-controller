class Ingredient:
    def __init__(self, amount, name, stage):
        self.amount = amount
        self.name = name 
        self.stage = stage

    def __str__(self) -> str:
        return f"NAME: {self.name}  AMOUNT: {self.name}  STAGE {self.stage}"