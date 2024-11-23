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

	def notifications_confirm(self) -> types.InlineKeyboardMarkup:

		Menu = types.InlineKeyboardMarkup()
		No = types.InlineKeyboardButton("Нет", callback_data = "notifications_answer_no")
		Yes = types.InlineKeyboardButton("Да", callback_data = "notifications_answer_yes")
		Menu.add(No, Yes, row_width = 2)
		
		return Menu
	
	def notifications_disable(self) -> types.InlineKeyboardMarkup:

		Menu = types.InlineKeyboardMarkup()
		No = types.InlineKeyboardButton("Нет", callback_data = "notifications_disable_no")
		Yes = types.InlineKeyboardButton("Да", callback_data = "notifications_disable_yes")
		Menu.add(No, Yes, row_width = 2)
		
		return Menu

