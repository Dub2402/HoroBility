from dublib.Methods.JSON import ReadJSON
from dublib.TelebotUtils import UsersManager
from telebot import types
from Source.ReplyKeyboards import ReplyKeyboards
from dublib.Methods.Filesystem import MakeRootDirectories
from dublib.Methods.System import Clear
from Source.Neurowork import Neurwork
from Source.Updater import Updater
from Source.Functions import DeleteSymbols, GetTodayDate

import telebot
import logging


Clear()

Settings = ReadJSON("Settings.json")
MakeRootDirectories(["Data/Users"])

logging.basicConfig(level=logging.INFO, encoding="utf-8", filename="LOGING.log", filemode="w",
	format='%(asctime)s - %(levelname)s - %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S')

Bot = telebot.TeleBot(Settings["token"])
usermanager = UsersManager("Data/Users")
ReplyKeyboardBox = ReplyKeyboards()
neurowork = Neurwork()
updater = Updater()


@Bot.message_handler(commands=["start"])
def ProcessCommandStart(Message: types.Message):
	User = usermanager.auth(Message.from_user)
	Bot.send_message(
		Message.chat.id, 
		"Добро пожаловать в мир тайн вашей совместимости! Приоткройте их завесу и узнайте, что же вам подсказывают звезды! 💫", 
		reply_markup = ReplyKeyboardBox.AddMainMenu()
		)
	Bot.delete_message(Message.chat.id, Message.id)

@Bot.message_handler(content_types = ["text"], regexp = "Общая совместимость")
def ProcessShareWithFriends(Message: types.Message):
	User = usermanager.auth(Message.from_user)

	Bot.send_message(
		Message.chat.id, 
		text = "Выберите, пожалуйста, свой знак зодиака:",
		reply_markup = ReplyKeyboardBox.ZodiacMenu()
		)
	User.set_property("type", "General")
	User.set_expected_type("first_zodiak")
	Bot.delete_message(Message.chat.id, Message.id)
	  
@Bot.message_handler(content_types = ["text"], regexp = "Совместимость на сегодня")
def ProcessShareWithFriends(Message: types.Message):
	User = usermanager.auth(Message.from_user)

	Bot.send_message(
		Message.chat.id, 
		text = "Выберите, пожалуйста, свой знак зодиака:",
		reply_markup = ReplyKeyboardBox.ZodiacMenu()
		)
	User.set_property("type", "Today")
	User.set_expected_type("first_zodiak")
	Bot.delete_message(Message.chat.id, Message.id)
	
@Bot.message_handler(content_types = ["text"], regexp = "Поделиться с друзьями")
def ProcessShareWithFriends(Message: types.Message):
	User = usermanager.auth(Message.from_user)


@Bot.message_handler(content_types = ["text"])
def ProcessShareWithFriends(Message: types.Message):
	User = usermanager.auth(Message.from_user)

	if User.expected_type == "first_zodiak":
		User.set_property("first_zodiak", DeleteSymbols(Message.text))
		Bot.send_message(
			Message.chat.id, 
			text = "А теперь выберите знак зодиака человека, на которого хотите посмотреть:",
			reply_markup = ReplyKeyboardBox.ZodiacMenu()
			)
		User.set_expected_type("second_zodiak")
		return
	
	if User.expected_type == "second_zodiak":
		User.set_property("second_zodiak", DeleteSymbols(Message.text))
		if User.get_property("type") == "General":
			Bot.send_message(
				Message.chat.id, 
				text = "Тестовый текст на общую совместимость.",
				reply_markup = ReplyKeyboardBox.AddMainMenu()
				)
		else:
			Today = GetTodayDate()
			Key = updater.CreateKey(User.get_property("first_zodiak"), User.get_property("second_zodiak"))
			print(Key)
			if updater.GetText(Key):
				Text = updater.GetText(Key)
			else:
				Text = neurowork.GetResponce(User)
				updater.AddText(Text, Key, Today)
			print(Text)
			Bot.send_message(
				Message.chat.id, 
				text = Text,
				reply_markup = ReplyKeyboardBox.AddMainMenu(), 
				parse_mode = "MarkdownV2" 
				)
		User.set_expected_type(None)
		return
	
	Bot.delete_message(Message.chat.id, Message.id)
	
Bot.infinity_polling()
