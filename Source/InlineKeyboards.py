from dublib.TelebotUtils import UserData
from telebot import types

class InlineKeyboards:

	def __init__(self):
		pass
	
	def AddShare(self) -> types.InlineKeyboardMarkup:
		Menu = types.InlineKeyboardMarkup()

		Share = types.InlineKeyboardButton(
			"Поделиться", 
			switch_inline_query='\n\nСовместимость по гороскопу\nВсе знаки зодиака и все главные сферы жизни 😏🤞',
			parse_mode= "MarkdownV2",
			)
		
		Menu.add(Share)

		return Menu

