from dublib.Methods.JSON import ReadJSON

class Updater:

    def __init__(self) -> None:
        self.__Sequence = (
            "Овен",
            "Телец", 
            "Близнецы", 
            "Рак", 
            "Лев", 
            "Дева", 
            "Весы", 
            "Скорпион", 
            "Стрелец", 
            "Козерог", 
            "Водолей", 
            "Рыбы"
            )
        
    def CreateKey(self, first_zodiak, second_zodiak) -> str:

        index1 = self.__Sequence.index(first_zodiak)
        index2 = self.__Sequence.index(second_zodiak)

        if index1 < index2:
            Key = f"{first_zodiak}_{second_zodiak}"
        else:
            Key = f"{second_zodiak}_{first_zodiak}"

        return Key

    def GetText(self, Key) -> str:

        Text = ReadJSON("Response.json")[Key]["text"]

        return Text
    
    def AddText(self, Text):
        pass