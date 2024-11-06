from g4f.client import Client
from dublib.Polyglot import Markdown
from Source.Functions import GetTodayDate

import random

class Neurwork:

	def __match_rus(self, character, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
		
		return character.lower() in alphabet
	
	def __IsTextRussian(self, text):
		IsRussian = True 

		for Character in text:
			if Character.isalpha() and not self.__match_rus(Character):
				IsRussian = False
				break

		return IsRussian
		

	def __init__(self) -> None:
			self.__Client = Client()
		
	def GetResponce(self, first_zodiak: str, second_zodiak: str) -> str:
		Result = False
		Percent = random.randint(1, 100)
		
		Title = f"*💞 {first_zodiak} & {second_zodiak} 💞*"
		Today = Markdown(GetTodayDate()).escaped_text

		while not Result:
			Request = f"Представь себя гадалкой. Составь совместимость {first_zodiak} и {second_zodiak} на сегодняшний день, если известно, что их совместимость {Percent}%. Не добавляй в текст процент совместимости!!!"
			Response = self.__Client.chat.completions.create(model = "gpt-4", messages = [{"role": "user", "content": Request}])
			MainText = Markdown(Response.choices[0].message.content).escaped_text
			print(Result)

			if self.__IsTextRussian(MainText) and "терапевт" not in MainText and "психолог" not in MainText: Result = True

		Text = Title + "\n" + f"*Совместимость на {Today}*" + "\n\n" + MainText + "\n\n" + f"*💠 Совместимость на сегодня __\\- {Percent}%__*"
		print(Text)
		
		return Text





