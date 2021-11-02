class Instruction:
    def __init__(self, time, temp, type):
        self.time = time
        self.temp = temp
        self.type = type

    def __str__(self) -> str:
        return f"TIME: {self.time} TEMP: {self.temp}  TYPE: {self.type}"

    def getTime(self):
        return self.time

    def getTemp(self):
        return self.temp

    def getType(self):
        return self.type

    def setTime(self, newTime):
        self.time = newTime
    
    def setTemp(self, newTemp):
        self.temp = newTemp

    def setType(self, newType):
        self.type = newType
        

