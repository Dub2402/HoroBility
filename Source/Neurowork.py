from g4f.client import Client
from dublib.TelebotUtils import UserData
from datetime import datetime, date
from dublib.Polyglot import Markdown

class Neurwork:

    def __init__(self) -> None:
            self.__Client = Client()
        
    def GetResponce(self, User: UserData) -> str:

        Symbols = ["♈",
                   "♉", 
                   "♊",
                   "♋",
                   "♌",
                   "♍",
                   "♎",
                   "♏",
                   "♐",
                   "♑",
                   "♒",
                   "♓"]
        
        first_zodiak = User.get_property("first_zodiak")
        second_zodiak = User.get_property("second_zodiak")
        for symbol in Symbols:
            if symbol in first_zodiak or symbol in second_zodiak:
                first_zodiak = first_zodiak.replace(symbol, "")
                second_zodiak = second_zodiak.replace(symbol, "")

        Title = f"*💞 {first_zodiak} & {second_zodiak} 💞*"
        Today = datetime.today().date().strftime("%d.%m.%Y")
        Today = Markdown(Today).escaped_text 

        Request1 = f"Сгенерируй {first_zodiak} и {second_zodiak} совместимость только на сегодня."
        Response1 = self.__Client.chat.completions.create(model = "gpt-4", messages = [{"role": "user", "content": Request1}])
        Request2 = f"Оцени процент совместимости {first_zodiak} и {second_zodiak} для текста {Response1.choices[0].message.content}. Выведи результат в виде одной цифры и знака процента!!! Цифра не может быть больше 100."
        Response2 = self.__Client.chat.completions.create(model = "gpt-4", messages = [{"role": "user", "content": Request2}])
        MainText = Markdown(Response1.choices[0].message.content).escaped_text 
        Percent = Markdown(Response2.choices[0].message.content).escaped_text 
        
        Text = Title + "\n" + f"*Совместимость на {Today}*" + "\n\n" + MainText + "\n\n" + f"*💠 Совместимость на сегодня __\\- {Percent}__*"
        return Text
