

class BrewHistory:
    def __init__(self, date: str, batchSize: str, sg: str, ibu: str, abv: str, notes: str):
        self.date = date;
        self.batchSize = batchSize
        self.sg = sg
        self.ibu = ibu
        self.abv = abv
        self.notes = notes

    def __str__(self) -> str:
        return f"Date: {self.date}\nBatch Size: {self.batchSize}\nsg: \n{self.sg}\nibu: {self.ibu}\nabv: {self.abv}\nnotes: {self.notes}"

    def toString(self):
        return f"Date: {self.date}\nBatch Size: {self.batchSize}\nsg: \n{self.sg}\nibu: {self.ibu}\nabv: {self.abv}\nnotes: {self.notes}"
