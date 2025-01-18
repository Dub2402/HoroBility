from dublib.Methods.Filesystem import ReadJSON
from dublib.TelebotUtils import UsersManager
from dublib.TelebotUtils.Cache import TeleCache
from dublib.Methods.Filesystem import MakeRootDirectories
from dublib.Methods.System import Clear

from Source.Neurowork import Neurwork
from Source.Updater import Updater
from Source.Functions import DeleteSymbols, GetTodayDate, MirrorText, ChangeMorphology
from Source.ReplyKeyboards import ReplyKeyboards
from Source.InlineKeyboards import InlineKeyboards
from Source.Mailer import Mailer

from apscheduler.schedulers.background import BackgroundScheduler

import telebot
import logging
from telebot import types

Clear()

Settings = ReadJSON("Settings.json")
GeneralTexts = ReadJSON("Совместимость.json")
MakeRootDirectories(["Data/Users"])

logging.basicConfig(level=logging.INFO, encoding="utf-8", filename="LOGING.log", filemode="w", force=True,
	format='%(asctime)s - %(levelname)s - %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S')

logging.getLogger("pyTelegramBotAPI").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)

Bot = telebot.TeleBot(Settings["token"])
usermanager = UsersManager("Data/Users")
ReplyKeyboardBox = ReplyKeyboards()
InlineKeyboardsBox = InlineKeyboards()
neurowork = Neurwork()
updater = Updater(neurowork, Bot, Settings["chat_id"])
scheduler = BackgroundScheduler()

# Инициализация менеджера кэша.
Cacher = TeleCache()
mailer = Mailer(Bot, usermanager, updater, Cacher)

scheduler.add_job(updater.UpdateJson, 'cron', hour = Settings["updating_time"].split(":")[0], minute = Settings["updating_time"].split(":")[1])
scheduler.add_job(mailer.StartMailing, 'cron', hour = Settings["mailing_time"].split(":")[0], minute = Settings["mailing_time"].split(":")[1])
scheduler.start()

# Установка данных для выгрузки медиафайлов.
Cacher.set_options(Settings["token"], Settings["chat_id"])

# Получение структуры данных кэшированного файла.
try:
	File = Cacher.get_cached_file(Settings["share_image_path"], type = types.InputMediaPhoto)
	# Получение ID кэшированного файла.
	FileID = Cacher[Settings["share_image_path"]]
except KeyError:
	pass

@Bot.message_handler(commands = ["start"])
def ProcessCommandStart(Message: types.Message):
	User = usermanager.auth(Message.from_user)
	User.set_property("notification_key", None, force = False)
	Bot.send_message(
		Message.chat.id, 
		"Добро пожаловать в мир тайн вашей совместимости! Приоткройте их завесу и узнайте, что же вам предсказывают звезды! 💫", 
		reply_markup = ReplyKeyboardBox.AddMainMenu()
		)
	
@Bot.message_handler(commands = ["mailset"])
def ProcessCommandMailset(Message: types.Message):
	User = usermanager.auth(Message.from_user)
	Bot.send_message(Message.chat.id, ("Желаете включить утреннюю рассылку <b>Совместимости по гороскопу</b>?"), parse_mode = "HTML", reply_markup = InlineKeyboardsBox.notifications())

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("notifications"))
def InlineButton(Call: types.CallbackQuery):
	User = usermanager.auth(Call.from_user)
	Command = Call.data.split("_")[-1]

	if Command == "yes":
		Bot.send_message(
			chat_id = User.id, 
			text = "Выберите, пожалуйста, свой знак зодиака:",
			reply_markup = ReplyKeyboardBox.ZodiacMenu()
			)
		User.set_expected_type("first_zodiak")

	else:
		User.set_property("notification_key", None)
		Bot.edit_message_text(
			text = "Хорошо! Вы в любой момент сможете посмотреть предсказания, выбрав в меню ниже ваши знаки зодиака 💫",
			chat_id = User.id,
			message_id = Call.message.id,
			parse_mode = "HTML",
			reply_markup = None
		)

@Bot.message_handler(content_types = ["text"], regexp = "Общая совместимость")
def ProcessShareWithFriends(Message: types.Message):
	User = usermanager.auth(Message.from_user)

	Bot.send_message(
		chat_id = Message.chat.id, 
		text = "Выберите, пожалуйста, свой знак зодиака:",
		reply_markup = ReplyKeyboardBox.ZodiacMenu()
		)
	User.set_property("type", "General")
	User.set_expected_type("first_zodiak")
	  
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
	
@Bot.message_handler(content_types = ["text"], regexp = "Поделиться с друзьями")
def ProcessShareWithFriends(Message: types.Message):
	User = usermanager.auth(Message.from_user)
	try:
		Bot.send_photo(
			Message.chat.id, 
			photo = FileID,
			caption="@Sowmes\\_bot\n@Sowmes\\_bot\n@Sowmes\\_bot\n\n*Совместимость по гороскопу*\nВсе знаки зодиака и самые главные сферы жизни 🤞☺️🤞", 
			reply_markup=InlineKeyboardsBox.AddShare(), 
			parse_mode= "MarkdownV2"
			)
	except NameError:
		Bot.send_message(
			Message.chat.id, 
			text="@Sowmes\\_bot\n@Sowmes\\_bot\n@Sowmes\\_bot\n\n*Совместимость по гороскопу*\nВсе знаки зодиака и самые главные сферы жизни 🤞☺️🤞", 
			reply_markup=InlineKeyboardsBox.AddShare(), 
			parse_mode= "MarkdownV2"
			)

@Bot.message_handler(content_types = ["text"])
def ProcessShareWithFriends(Message: types.Message):
	User = usermanager.auth(Message.from_user)

	if User.expected_type == "first_zodiak":
		if Message.text not in (
			"♈ Овен",
			"♉ Телец",
			"♊ Близнецы",
			"♋ Рак",
			"♌ Лев",
			"♍ Дева",
			"♎ Весы",
			"♏ Скорпион",
			"♐ Стрелец",
			"♑ Козерог",
			"♒ Водолей",
			"♓ Рыбы"
			): Bot.send_message(
					text = "Пожалуйста, используйте кнопки ниже, для выбора своего знака зодиака",
					chat_id = User.id,
					reply_markup = ReplyKeyboardBox.ZodiacMenu()
				)
		else:
			User.set_property("first_zodiak", DeleteSymbols(Message.text))
			Bot.send_message(
				Message.chat.id, 
				text = "А теперь выберите знак зодиака человека, на которого хотите посмотреть:",
				reply_markup = ReplyKeyboardBox.ZodiacMenu()
				)
			User.set_expected_type("second_zodiak")
		return
	
	if User.expected_type == "second_zodiak":
		if Message.text not in (
			"♈ Овен",
			"♉ Телец",
			"♊ Близнецы",
			"♋ Рак",
			"♌ Лев",
			"♍ Дева",
			"♎ Весы",
			"♏ Скорпион",
			"♐ Стрелец",
			"♑ Козерог",
			"♒ Водолей",
			"♓ Рыбы"
			): Bot.send_message(
					text = "Пожалуйста, используйте кнопки ниже, для выбора своего знака зодиака",
					chat_id = User.id,
					reply_markup = ReplyKeyboardBox.ZodiacMenu()
				)
		else:
			FirstZodiak = User.get_property("first_zodiak")
			User.set_property("second_zodiak", DeleteSymbols(Message.text))
			SecondZodiak = User.get_property("second_zodiak")
			File = Cacher.get_cached_file(path = f"Materials/{FirstZodiak}/{SecondZodiak}.jpg", type = types.InputMediaPhoto)
			File = Cacher.get_cached_file(path = f"Materials/{SecondZodiak}/{FirstZodiak}.jpg", type = types.InputMediaPhoto)
			Photo_Original = Cacher[f"Materials/{FirstZodiak}/{SecondZodiak}.jpg"]
			Photo_Mirror = Cacher[f"Materials/{SecondZodiak}/{FirstZodiak}.jpg"]
			match User.get_property("type"):
				case "General":
					Text = GeneralTexts[f"{FirstZodiak}_{SecondZodiak}"].split("🏠")
					Bot.send_photo(
						chat_id = Message.chat.id, 
						photo = Photo_Original,
						caption = Text[0],
						reply_markup = ReplyKeyboardBox.AddMainMenu(),
						parse_mode= "HTML"
						)
					Bot.send_photo(
						chat_id = Message.chat.id, 
						photo = Photo_Mirror,
						caption = Text[-1],
						reply_markup = ReplyKeyboardBox.AddMainMenu(),
						parse_mode= "HTML", 
						show_caption_above_media = True
						)
					
				case "Today":
					Today = GetTodayDate()
					Zodiak_Key = updater.CreateKey(FirstZodiak, SecondZodiak)
					if updater.GetValue(Zodiak_Key, "text") and updater.GetValue(Zodiak_Key, "date") == GetTodayDate():
						Text = updater.GetValue(Zodiak_Key, "text")
					else:
						Text = neurowork.GetResponce(FirstZodiak, SecondZodiak)
						updater.AddText(Text, Zodiak_Key, Today)
					if updater.isReversed(FirstZodiak, SecondZodiak):
						Text = MirrorText(Text, FirstZodiak, SecondZodiak)
						Text = ChangeMorphology(Text, FirstZodiak, SecondZodiak)
						Bot.send_photo(
							Message.chat.id, 
							photo = Photo_Original,
							caption = Text,
							reply_markup = ReplyKeyboardBox.AddMainMenu(), 
							parse_mode = "MarkdownV2" 
							)
					else:
						Bot.send_photo(
							Message.chat.id, 
							photo = Photo_Original,
							caption = Text,
							reply_markup = ReplyKeyboardBox.AddMainMenu(), 
							parse_mode = "MarkdownV2" 
							)
				case None:
					User.set_property("notification_key", [FirstZodiak, SecondZodiak])
					Bot.send_message(
					text = "Спасибо! Теперь вы будете просыпаться вместе со звездами! ✨️",
					chat_id = User.id,
					reply_markup = ReplyKeyboardBox.AddMainMenu()
				)

			User.set_expected_type(None)
			User.set_property("type", None)
			return
	
Bot.infinity_polling()

