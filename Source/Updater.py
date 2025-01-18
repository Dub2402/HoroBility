from dublib.Methods.Filesystem import ReadJSON, WriteJSON
from Source.Neurowork import Neurwork
from Source.Functions import GetTodayDate
import telebot

class Updater:

    def __Save(self):
        WriteJSON("Response.json", self.__Data)

    def __init__(self, neurowork: Neurwork, Bot: telebot.TeleBot, chat_id: int) -> None:
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
        self.__Data = ReadJSON("Response.json")
        self.__neurowork = neurowork
        self.__Bot = Bot
        self.__chat_id = chat_id

    def isReversed(self,  first_zodiak, second_zodiak) -> bool:
        isReverse = False

        index1 = self.__Sequence.index(first_zodiak)
        index2 = self.__Sequence.index(second_zodiak)
        if index1 <= index2:
            isReverse = False
        else:
            isReverse = True

        return isReverse
        
    def CreateKey(self, first_zodiak, second_zodiak) -> str:
        index1 = self.__Sequence.index(first_zodiak)
        index2 = self.__Sequence.index(second_zodiak)

        if index1 < index2:
            Key = f"{first_zodiak}_{second_zodiak}"
        else:
            Key = f"{second_zodiak}_{first_zodiak}"

        return Key

    def GetValue(self, Zodiak_Key, Key_attribute) -> str:

        Value = ReadJSON("Response.json")[Zodiak_Key][Key_attribute]

        return Value
    
    def AddText(self, Text, Zodiak_Key, Today):
        self.__Data[Zodiak_Key] = {
            "date": Today,
            "text": Text
            }
        self.__Save()

    def UpdateJson(self):
        self.__Bot.send_message(
                    self.__chat_id,
                    "Начало обновления данных в json."
                )
        Today = GetTodayDate()
        for Zodiak_Key in self.__Data:
            if self.GetValue(Zodiak_Key, "date") != Today:
                first_zodiak = Zodiak_Key.split("_")[0]
                second_zodiak = Zodiak_Key.split("_")[1]
                print(99)
                Text = self.__neurowork.GetResponce(first_zodiak, second_zodiak)
                print(Text)
                self.AddText(Text, Zodiak_Key, Today)
                self.__Bot.send_message(
                    self.__chat_id,
                    Text,
                    parse_mode = "MarkdownV2" 
                )
