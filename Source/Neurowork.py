from g4f.client import Client
from dublib.Polyglot import Markdown
from Source.Functions import GetTodayDate

import g4f
import random

class Neurwork:

	def __match_rus(self, character, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
		
		return character.lower() in alphabet
	
	def __IsTextRussian(self, text):
		IsRussian = True 
		if not text:
			IsRussian = False
		else:
			for Character in text:
				if Character.isalpha() and not self.__match_rus(Character):
					IsRussian = False
					break

		return IsRussian

	def __GetGoodResult(self, text):
		Result = False
		if self.__IsTextRussian(text) and len(text) < 500: Result = True

		return Result

	def __init__(self) -> None:
			self.__Client = Client()

	def GetResponce(self, first_zodiak: str, second_zodiak: str) -> str:
		Result = False
		Percent = random.randint(1, 100)
		
		Title = f"*💞 {first_zodiak} & {second_zodiak} 💞*"
		Today = Markdown(GetTodayDate()).escaped_text

		while not Result:
			
			Request = f"Сгенерируй 1 абзац (не более 400 символов) гороскопа совместимости для знаков зодиака {first_zodiak} и {second_zodiak} на сегодня, если известно, что их степень совместимости {Percent}%. "
			Request += "Первый абзац описывает совместимость этих знаков на сегодняшний день, интересные детали сегодняшнего взаимодействия. "
			Request += "Не добавляй в текст ничего лишнего, разметку и сам процент совместимости!!!"
			Response = self.__Client.chat.completions.create(model = "gpt-4", provider = g4f.Provider.Ai4Chat, messages = [{"role": "user", "content": Request}])
			Text_response = Response.choices[0].message.content.strip().replace("\n", "\n\n")
			MainText = Markdown(Text_response).escaped_text

			try:
				Result = self.__GetGoodResult(MainText)
			except: pass

		Text = Title + "\n" + f"*Совместимость на {Today}*" + "\n\n" + MainText + "\n\n" + f"*💠 Совместимость на сегодня __\\- {Percent}%__*"
		
		return Text

