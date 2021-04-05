import re

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import *
from flask import Flask, jsonify, request


app = Flask(__name__)

bot = telebot.TeleBot(TOKEN)

groupChatId = '@H_reug0'
keyFormat = {
	'type': 'callback',
	'texts': [''],
	'callbacks': [''],
	'urls': [],
}


@app.route('/'+TOKEN, methods=['POST'])
def getMessage():
	# bot.enable_save_next_step_handlers(delay=2)
	# bot.load_next_step_handlers()
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200

@app.route('/<userId>', methods=['GET'])
def sendForm(userId):
	bot.send_message(userId, tree.form.text)
	return "Good!", 200

@app.route('/')
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url=URL + TOKEN)
	return '!', 200


def create_keyboard(arr, vals):
	keyboard = InlineKeyboardMarkup()
	i = 0
	print(vals)
	for lst in arr:
		buttons = []
		for button in lst:
			if vals[i]['type'] == 'callback':
				inlineValue = InlineKeyboardButton(button.text.format(*vals[i]['texts']),
												   callback_data=button.callback.format(*vals[i]['callbacks']))
			elif vals[i]['type'] == 'url':
				inlineValue = InlineKeyboardButton(button.text.format(*vals[i]['texts']),
												   url=button.url.format(*vals[i]['urls']))
			buttons.append(inlineValue)
			i = i + 1
		keyboard.row(*buttons)
	return keyboard


@bot.message_handler(commands=['start'])
def menu(message):
	userId = message.chat.id
	currentInlineState = [keyFormat, keyFormat, keyFormat, keyFormat]
	keyboard = create_keyboard(tree.menu.buttons, currentInlineState)
	bot.send_message(userId, tree.menu.text, reply_markup=keyboard)



## <======================== LIST GAMES ==================================>
def list_games(message, value):
	userId = message.chat.id
	value = int(value[0])

	currentInlineState = [{'type':'callback', 'texts':[''], 'callbacks':[max(value - 1, 0)]}, 
						  {'type':'url', 'texts':[''], 'urls':[tree.list_games.messages[value].url.format(userId)]}, 
						  {'type':'callback', 'texts':[''], 'callbacks':[min(value + 1, len(tree.list_games.messages) - 1)]},
						  keyFormat]
	keyboard = create_keyboard(tree.list_games.buttons, currentInlineState)
	bot.send_photo(chat_id=userId, 
				   photo=tree.list_games.messages[value].image, 
				   caption=tree.list_games.messages[value].text, 
				   reply_markup=keyboard)
## <======================================================================>



## <========================== GET CHECK =================================>
def get_check(message):
	userId = message.chat.id
	msg = bot.send_message(userId, tree.get_check.text[0])
	bot.register_next_step_handler(msg, recieved_check)
def recieved_check(message):
	userId = message.chat.id

	# check if its a photo
	if message.content_type != 'photo':
		msg = bot.send_message(userId, tree.get_check.text[1])
		bot.register_next_step_handler(msg, recieved_check)
		return
	currentInlineState = [keyFormat]
	keyboard = create_keyboard(tree.get_check.buttons, currentInlineState)
	bot.send_message(userId, tree.get_check.text[2], reply_markup=keyboard)

	bot.forward_message(groupChatId, userId, message.message_id)

	currentInlineState = [{'type': 'callback', 'texts':[''], 'callbacks':[userId]},
						  {'type': 'callback', 'texts':[''], 'callbacks':[userId]}]
	keyboard = create_keyboard(tree.confirmation.buttons, currentInlineState)
	# bot.edit_message_text(groupChatId, message.message_id, tree.confirmation.text.format(message.chat.username), reply_markup=keyboard )

	bot.send_message(groupChatId, tree.confirmation.text.format(message.chat.username), reply_markup=keyboard)
## <======================================================================>



## <====================== CONFIRMATION ==================================>
def confirm(message, values):
	userId = message.chat.id
	print(message)
	print(message.message_id)
	if values[0] == 'no':
		text = 'Отвергнут'
		bot.send_message(int(values[1]), tree.confirm.text[0])
	elif values[0] == 'yes':
		text = 'Одобрит'
		bot.send_message(int(values[1]), tree.confirm.text[1])

	bot.send_message(groupChatId, tree.confirm.text[2].format(text))
## <======================================================================>



## <======================== CONDITIONS ==================================>
def сonditions(message):
	userId = message.chat.id
	currentInlineState = [keyFormat]
	keyboard = create_keyboard(tree.сonditions.buttons, currentInlineState)
	bot.send_message(userId, tree.сonditions.text, reply_markup=keyboard)
## <======================================================================>



## <=========================== FAQ ======================================> 
def ask_question(message):
	userId = message.chat.id
	currentInlineState = [keyFormat, keyFormat]
	keyboard = create_keyboard(tree.ask_question.buttons, currentInlineState)
	bot.send_message(userId, tree.ask_question.text, reply_markup=keyboard)
def question(message):
	userId = message.chat.id
	currentInlineState = [keyFormat]
	keyboard = create_keyboard(tree.question.buttons, currentInlineState)
	bot.send_message(userId, tree.question.text, reply_markup=keyboard)
## <======================================================================>

def calc(query):
	value = -1
	if '?' in query:
		value = re.search(r'\?.+', query)[0][1:].split(',')
		query = re.search(r'^[^\?]+', query)[0]
	return [query, value]

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
	bot.delete_message(call.message.chat.id, call.message.message_id)

	userId = call.message.chat.id
	[query, value] = calc(call.data)

	possibles = globals().copy()
	possibles.update(locals())
	method = possibles.get(query)
	if value == -1:
		method(call.message)
	else:
		method(call.message, value)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))