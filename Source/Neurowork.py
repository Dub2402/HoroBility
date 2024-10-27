from g4f.client import Client
from dublib.TelebotUtils import UserData
from dublib.Polyglot import Markdown
from Source.Functions import GetTodayDate

import random

class Neurwork:

    def __init__(self) -> None:
            self.__Client = Client()
        
    def GetResponce(self, User: UserData) -> str:

        first_zodiak = User.get_property("first_zodiak")
        second_zodiak = User.get_property("second_zodiak")
        Percent = random.randint(1, 100)
        
        Title = f"*💞 {first_zodiak} & {second_zodiak} 💞*"
        Today = Markdown(GetTodayDate()).escaped_text
    
        Request1 = f"Сгенерируй {first_zodiak} и {second_zodiak} совместимость на {Percent}% только на сегодня. Не добавляй в текст процент совместимости!!!"
        Response1 = self.__Client.chat.completions.create(model = "gpt-4", messages = [{"role": "user", "content": Request1}])
        MainText = Markdown(Response1.choices[0].message.content).escaped_text 
        
        Text = Title + "\n" + f"*Совместимость на {Today}*" + "\n\n" + MainText + "\n\n" + f"*💠 Совместимость на сегодня __\\- {Percent}%__*"
        
        return Text
