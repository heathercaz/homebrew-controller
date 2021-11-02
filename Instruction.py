class Instruction:
    def __init__(self, time, temp, type):
        self.time = time
        self.temp = temp
        self.type = type

    def __str__(self) -> str:
        return f"TIME: {self.time} TEMP: {self.temp}  TYPE: {self.type}"


