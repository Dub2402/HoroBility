from dublib.TelebotUtils import UsersManager
from dublib.TelebotUtils.Cache import TeleCache

from Source.Updater import Updater
from Source.Functions import MirrorText, ChangeMorphology

from telebot import TeleBot
from telebot import types

import logging


class Mailer:

	def __init__(self, bot: TeleBot, usermanager: UsersManager, updater: Updater, Cacher: TeleCache):
		self.__Bot = bot
		self.__usermanager = usermanager
		self.__updater = updater
		self.__Cacher = Cacher

	def StartMailing(self):
		
		for User in self.__usermanager.users:
			logging.info(f"Начата рассылка: {User.id} ")
			FirstZodiak = None
			SecondZodiak = None
			Text = None
			FileID = None

			try:
				FirstZodiak = User.get_property("notification_key")[0]
				SecondZodiak = User.get_property("notification_key")[1]
				File = self.__Cacher.get_cached_file(path = f"Materials/{FirstZodiak}/{SecondZodiak}.jpg", type = types.InputMediaPhoto)
				FileID = self.__Cacher[f"Materials/{FirstZodiak}/{SecondZodiak}.jpg"]
				Key = self.__updater.CreateKey(FirstZodiak, SecondZodiak)
				Text = self.__updater.GetValue(Key, "text")
				if self.__updater.isReversed(FirstZodiak, SecondZodiak):
					Text = MirrorText(Text, FirstZodiak, SecondZodiak)
					Text = ChangeMorphology(Text, FirstZodiak, SecondZodiak)
				self.__Bot.send_photo(
				chat_id = User.id, 
				photo = FileID,
				caption = Text,
				parse_mode= "MarkdownV2"
				)
					
				logging.info(f"Совместимость {Key} отправлена {User.id} ")
				User.set_chat_forbidden(False)
				
			except TypeError:
				logging.info(f"Рассылка выключена {User.id}")
			except KeyError:
				logging.info(f"Рассылкой пользователь {User.id} не пользовался.")

			except Exception as E: 
				logging.info(f"{E}, {User.id}")
				User.set_chat_forbidden(True)
		
			
			

			
						