import re
import os

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

from config import *
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
cluster = PyMongo(app, uri=URI)
users = cluster.db.user

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

@app.route('/gamebot/<userId>', methods=['GET'])
def sendForm(userId):
	print(userId)
	currentInlineState = [keyFormat]
	keyboard = create_keyboard(tree.form.buttons, currentInlineState)
	bot.send_message(userId, tree.form.text, reply_markup=keyboard)
	return "Form started!", 200

@app.route('/')
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url=URL + TOKEN)
	return '!', 200


def create_keyboard(arr, vals):
	keyboard = InlineKeyboardMarkup()
	i = 0
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
	if users.find_one({'_id': userId}) == None:
		users.insert_one({
			'_id': userId,
			'name': "#",
			'toy_choice': 0,
			'photo_check': -1,
			'function_name': '#'
		})

	currentInlineState = [keyFormat, keyFormat, keyFormat, keyFormat]
	keyboard = create_keyboard(tree.menu.buttons, currentInlineState)
	bot.send_message(userId, tree.menu.text, reply_markup=keyboard)

## <============================ FORM ====================================>
def form(message, values):
	userId = message.chat.id
	stageId = int(values[0])
	phase = tree.form.stages[stageId]
	print(phase, message)
	if values[1] == 'photo_check':
		if message.content_type != 'photo':
			bot.send_message(userId, phase[1].text)
			users.update_one({'_id': userId}, {'$set': {'function_name': phase[1].next_step}})
			return
		else:
			users.update_one({'_id': userId}, {'$set': {values[1]: message.message_id}})
	elif values[1] != '#':
		users.update_one({'_id': userId}, {'$set': {values[1]: message.text}})

	print(gifts)
	if 'buttons' in phase[0]:
		if 'prize' in phase[0]:
			index = int(values[2])
			currentInlineState = [
				{'type': 'callback', 'texts':[''], 'callbacks':[max(index - 1, 0)]},
				{'type': 'callback', 'texts':[''], 'callbacks':[min(index + 1, len(gifts) - 1)]},
				{'type': 'callback', 'texts':[''], 'callbacks':[index]},
			]
			keyboard = create_keyboard(phase[0].buttons, currentInlineState)
			bot.send_photo(chat_id=userId,
						   photo=gifts[index],
						   caption=phase[0].text,
						   reply_markup=keyboard)
		else:
			currentInlineState = [keyFormat, keyFormat]
			keyboard = create_keyboard(phase[0].buttons, currentInlineState)
			bot.send_message(userId, phase[0].text, reply_markup=keyboard)
	else:
		bot.send_message(userId, phase[0].text)

	users.update_one({'_id': userId}, {'$set': {'function_name': phase[0].next_step}})
def form_complete(message, values):
	userId = message.chat.id
	stageId = int(values[0])
	phase = tree.form.stages[stageId]
	if values[1] == 'toy_choice':
		users.update_one({'_id': userId}, {'$set': {values[1]: values[2]}})

	user = users.find_one({'_id': userId})

	currentInlineState = [keyFormat]
	keyboard = create_keyboard(phase[0].buttons, currentInlineState)
	bot.send_message(userId, phase[0].text, reply_markup=keyboard)

	# Send to channel for confirmation
	bot.forward_message(groupChatId, userId, user['photo_check'])
	currentInlineState = [{'type':'callback', 'texts':[''], 'callbacks':[userId]},
						  {'type':'callback', 'texts':[''], 'callbacks':[userId]}]
	keyboard = create_keyboard(tree.confirmation.buttons, currentInlineState)
	bot.send_message(groupChatId, tree.confirmation.text.format(message.chat.username), reply_markup=keyboard)
## <======================================================================>


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



## <====================== CONFIRMATION ==================================>
def confirm(message, values):
	userId = message.chat.id
	values[1] = int(values[1])

	if values[0] == 'no':
		text = 'Отвергнут'
		bot.send_message(values[1], tree.confirm.text[0])
	elif values[0] == 'yes':
		text = 'Одобрит'
		bot.send_message(values[1], tree.confirm.text[1])

		user = users.find_one({'_id': values[1]})
		bot.send_photo(chat_id=groupChatId,
					   photo=gifts[user['toy_choice']],
					   caption=tree.confirm.text[3].format(user['name'], user['address'], user['phone']))
	bot.send_message(groupChatId, tree.confirm.text[2].format(text))
## <======================================================================>



## <======================== CONDITIONS ==================================>
def сonditions(message):
	userId = message.chat.id
	currentInlineState = [keyFormat, keyFormat]
	keyboard = create_keyboard(tree.сonditions.buttons, currentInlineState)
	bot.send_message(userId, tree.сonditions.text, reply_markup=keyboard)

def list_partners(message):
	userId = message.chat.id
	currentInlineState = [keyFormat]
	keyboard = create_keyboard(tree.list_partners.buttons, currentInlineState)
	bot.send_message(userId, tree.list_partners.text, reply_markup=keyboard)
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



@bot.message_handler(content_types = ['text', 'photo'])
def receiver(message):
	userId = message.chat.id
	user = users.find_one({'_id': userId})
	if user['function_name'] != '#':
		[query, values] = calc(user['function_name'])
		users.update_one({'_id': userId}, {'$set': {'function_name': '#'}})

		print(query, values)
		possibles = globals().copy()
		possibles.update(locals())
		method = possibles.get(query)

		method(message, values)
	else:
		bot.send_message(userId, TEMPLATE_MESSAGE)

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