from dublib.TelebotUtils import UsersManager

from Source.Updater import Updater

from telebot import TeleBot

import logging


class Mailer:

	def __init__(self, bot: TeleBot, usermanager: UsersManager, updater: Updater):
		self.__Bot = bot
		self.__usermanager = usermanager
		self.__updater = updater

	def StartMailing(self):
		
		for User in self.__usermanager.users:
			logging.info(f"Начата рассылка: {User.id} ")
			try: 
				Text = self.__updater.GetValue(User.get_property("notification_key"), "text")
				self.__Bot.send_message(
					User.id, 
					Text,
					parse_mode = "MarkdownV2"
				)
				Text = None
				logging.info(f"Совместимость {User.get_property("notification_key")} отправлена {User.id} ")
				User.set_chat_forbidden(False)

			except KeyError: logging.info(f"Рассылка выключена {User.id}")
			except Exception as E: 
				logging.info(f"{E}, {User.id}")
				User.set_chat_forbidden(True)
						