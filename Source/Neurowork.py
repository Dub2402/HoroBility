from g4f.client import Client
from dublib.Polyglot import Markdown
from Source.Functions import GetTodayDate
from langdetect import detect

import json
import random

class Neurwork:

	def __init__(self) -> None:
			self.__Client = Client()
		
	def GetResponce(self, first_zodiak: str, second_zodiak: str) -> str:
		Result = False
		Percent = random.randint(1, 100)
		
		Title = f"*💞 {first_zodiak} & {second_zodiak} 💞*"
		Today = Markdown(GetTodayDate()).escaped_text

		while not Result:
			Request = f"Сгенерируй {first_zodiak} и {second_zodiak} совместимость на {Percent}% только на сегодня. Не добавляй в текст процент совместимости!!!"
			Response = self.__Client.chat.completions.create(model = "gpt-4", messages = [{"role": "user", "content": Request}])
			MainText = Markdown(Response.choices[0].message.content).escaped_text

			if len(MainText) > 10:
				Result = True

			try:
				dictData = json.loads(Response.choices[0].message.content)
				Result = False
			except json.decoder.JSONDecodeError:
				detect_language = detect(MainText)
				if detect_language != "ru": Result = False
				if Response.choices[0].message.content == "No message received" or Response.choices[0].message.content == "Request ended with status code 404": Result = False
			
		Text = Title + "\n" + f"*Совместимость на {Today}*" + "\n\n" + MainText + "\n\n" + f"*💠 Совместимость на сегодня __\\- {Percent}%__*"
		
		return Text
