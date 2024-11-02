from dublib.Methods.JSON import ReadJSON
from dublib.TelebotUtils import UsersManager
from dublib.TelebotUtils.Cache import TeleCache
from dublib.Methods.Filesystem import MakeRootDirectories
from dublib.Methods.System import Clear
from Source.Neurowork import Neurwork
from Source.Updater import Updater
from Source.Functions import DeleteSymbols, GetTodayDate
from Source.ReplyKeyboards import ReplyKeyboards
from Source.InlineKeyboards import InlineKeyboards
from apscheduler.schedulers.background import BackgroundScheduler

import telebot
import logging
from telebot import types

Clear()

Settings = ReadJSON("Settings.json")
MakeRootDirectories(["Data/Users"])

logging.basicConfig(level=logging.INFO, encoding="utf-8", filename="LOGING.log", filemode="w",
	format='%(asctime)s - %(levelname)s - %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S')

Bot = telebot.TeleBot(Settings["token"])
usermanager = UsersManager("Data/Users")
ReplyKeyboardBox = ReplyKeyboards()
InlineKeyboardsBox = InlineKeyboards()
neurowork = Neurwork()
updater = Updater(neurowork)
scheduler = BackgroundScheduler()

scheduler.add_job(updater.UpdateJson, 'cron', hour = Settings["updating_time"].split(":")[0], minute = Settings["updating_time"].split(":")[1])
scheduler.start()

# Инициализация менеджера кэша.
Cacher = TeleCache()
# Установка данных для выгрузки медиафайлов.
Cacher.set_options(Settings["token"], Settings["chat_id"])

# Получение структуры данных кэшированного файла.
try:
	File = Cacher.get_cached_file(Settings["path_to_image"], type = types.InputMediaPhoto)
	# Получение ID кэшированного файла.
	FileID = Cacher[Settings["path_to_image"]]
except KeyError:
	pass

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
	try:
		Bot.send_photo(
			Message.chat.id, 
			photo = FileID,
			caption="@Sowmes\\_bot\n@Sowmes\\_bot\n@Sowmes\\_bot\n\n*Совместимость по гороскопу*\nВсе знаки зодиака и все главные сферы жизни 😏🤞", 
			reply_markup=InlineKeyboardsBox.AddShare(), 
			parse_mode= "MarkdownV2"
			)
	except NameError:
		Bot.send_message(
			Message.chat.id, 
			text="@Sowmes\\_bot\n@Sowmes\\_bot\n@Sowmes\\_bot\n\n*Совместимость по гороскопу*\nВсе знаки зодиака и все главные сферы жизни 😏🤞", 
			reply_markup=InlineKeyboardsBox.AddShare(), 
			parse_mode= "MarkdownV2"
			)




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
			Zodiak_Key = updater.CreateKey(User.get_property("first_zodiak"), User.get_property("second_zodiak"))
			if updater.GetValue(Zodiak_Key, "text") and updater.GetValue(Zodiak_Key, "date") == GetTodayDate():
				Text = updater.GetValue(Zodiak_Key, "text")
			else:
				Text = neurowork.GetResponce(User.get_property("first_zodiak"), User.get_property("second_zodiak"))
				updater.AddText(Text, Zodiak_Key, Today)
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
