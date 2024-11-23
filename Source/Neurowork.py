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
	
	def __isСontainsWord(self, text):
		black_list = ["терапевт", "психолог", "клинический", "гадалки", "здравствуй", "давай", "совет", "звезды", "сочетание"]

		IsnotСontains = True

		split_segments = text.split(" ")
		for split_segment in split_segments:
			if split_segment.lower().replace(",", "").replace("**", "") in black_list:
				IsnotСontains = False
				break

		return IsnotСontains

	def __GetGoodResult(self, text):
		Result = False
		if self.__IsTextRussian(text) and self.__isСontainsWord(text): Result = True

		return Result

	def __init__(self) -> None:
			self.__Client = Client()
		
	def GetResponce(self, first_zodiak: str, second_zodiak: str) -> str:
		Result = False
		Percent = random.randint(1, 100)
		
		Title = f"*💞 {first_zodiak} & {second_zodiak} 💞*"
		Today = Markdown(GetTodayDate()).escaped_text

		while not Result:
			
			Request = f"Сгенерируй 2 абзаца совместимости для {first_zodiak} и {second_zodiak} на сегодняшний день, если известно, что их совместимость {Percent}%."
			Request += "Первый абзац совместимость на сегодня."
			Request += "Второй абзац резюмирующая для этих знаков зодиака"
			Request += "Не добавляй в текст знак %, разметку и строчки."
			Response = self.__Client.chat.completions.create(model = "gpt-4", provider = g4f.Provider.Ai4Chat, messages = [{"role": "user", "content": Request}])
			Text_response = Response.choices[0].message.content.strip().replace("\n", "\n\n")
			MainText = Markdown(Text_response).escaped_text

			try:
				Result = self.__GetGoodResult(MainText)
			except: pass

		Text = Title + "\n" + f"*Совместимость на {Today}*" + "\n\n" + MainText + "\n\n" + f"*💠 Совместимость на сегодня __\\- {Percent}%__*"
		
		return Text