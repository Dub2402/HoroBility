from telebot import types

class ReplyKeyboards:

	def __init__(self):
		pass

	def Share(self) -> types.ReplyKeyboardMarkup:
		# Кнопочное меню.
		Menu = types.ReplyKeyboardMarkup(resize_keyboard = True)

		# Генерация кнопок.
		Share = types.KeyboardButton("📢 Поделиться с друзьями")
	
		# Добавление кнопок в меню.
		Menu.add(Share, row_width = 1)
		
		return Menu

	def AddMainMenu(self) -> types.ReplyKeyboardMarkup:
		# Кнопочное меню.
		Menu = types.ReplyKeyboardMarkup(resize_keyboard = True)

		# Генерация кнопок.
		GeneralCompatinility = types.KeyboardButton("Общая совместимость")
		TodayCompatinility = types.KeyboardButton("Совместимость на сегодня")
		Share = types.KeyboardButton("Поделиться с друзьями")

		# Добавление кнопок в меню.
		Menu.add(GeneralCompatinility, TodayCompatinility, Share, row_width = 2)
		
		return Menu

	def ZodiacMenu(self) -> types.ReplyKeyboardMarkup:
		"""Строит Reply-интерфейс: панель выбора знака зодиака."""

		Zodiacs = {
			"♈": "Овен",
			"♉": "Телец",
			"♊": "Близнецы",
			"♋": "Рак",
			"♌": "Лев",
			"♍": "Дева",
			"♎": "Весы",
			"♏": "Скорпион",
			"♐": "Стрелец",
			"♑": "Козерог",
			"♒": "Водолей",
			"♓": "Рыбы"
		}
		Menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
		RowButtons = list()

		for Key in Zodiacs.keys(): 
			RowButtons.append(types.KeyboardButton(Key + " " + Zodiacs[Key]))
			
			if len(RowButtons) % 3 == 0:
				Menu.row(*RowButtons)
				RowButtons = list()
		
		return Menu