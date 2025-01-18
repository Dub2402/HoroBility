from dublib.TelebotUtils import UserData
from telebot import types

class InlineKeyboards:

	def __init__(self):
		pass
	
	def AddShare(self) -> types.InlineKeyboardMarkup:
		Menu = types.InlineKeyboardMarkup()

		Share = types.InlineKeyboardButton(
			"Поделиться", 
			switch_inline_query='\n\nСовместимость по гороскопу\nВсе знаки зодиака и самые главные сферы жизни 🤞☺️🤞',
			parse_mode= "MarkdownV2",
			)
		
		Menu.add(Share)

		return Menu

	def notifications(self) -> types.InlineKeyboardMarkup:

		Menu = types.InlineKeyboardMarkup()
		No = types.InlineKeyboardButton("Нет", callback_data = "notifications_no")
		Yes = types.InlineKeyboardButton("Да", callback_data = "notifications_yes")
		Menu.add(No, Yes, row_width = 2)
		
		return Menu
	

