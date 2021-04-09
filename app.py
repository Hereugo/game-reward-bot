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

def form(message, values):
	userId = message.chat.id
	stage = int(values[0])
	print(message, userId, values)
	# values to store
	if values[2] == 'name':
		users.update_one({'_id': userId}, {'$set': {values[2]: message.text}})
	elif values[2] == 'address':
		users.update_one({'_id': userId}, {'$set': {values[2]: message.text}})
	elif values[2] == 'phone':
		users.update_one({'_id': userId}, {'$set': {values[2]: message.text}})
	elif values[2] == 'toy_choice':
		users.update_one({'_id': userId}, {'$set': {values[2]: message.text}})
	elif values[2] == 'photo_check':
		if message.content_type != 'photo':
			bot.send_message(userId, tree.form.stages[stage-1].text[1])
			users.update_one({'_id': userId}, {'$set': {'function_name': 'form?4,0,check'}})
			return
		users.update_one({'_id': userId}, {'$set': {values[2]: message.message_id}})


	user = users.find_one({'_id': userId})
	if stage == 0: # Get name 
		bot.send_message(userId, tree.form.stages[stage].text)
		users.update_one({'_id': userId}, {'$set': {'function_name': 'form?1,#,name'}})
	elif stage == 1: # Get address
		bot.send_message(userId, tree.form.stages[stage].text)
		users.update_one({'_id': userId}, {'$set': {'function_name': 'form?2,#,address'}})
	elif stage == 2: # Get phone number
		bot.send_message(userId, tree.form.stages[stage].text)
		users.update_one({'_id': userId}, {'$set': {'function_name': 'form?3,#,phone'}})
	elif stage == 3: # Get check photo
		bot.send_message(userId, tree.form.stages[stage].text[0])
		users.update_one({'_id': userId}, {'$set': {'function_name': 'form?4,0,check'}})
	elif stage == 4: # Get toy choice
		index = int(values[1])
		print(index)
		currentInlineState = [
			{'type': 'callback', 'texts':[''], 'callbacks':[max(index - 1, 0)]},
			{'type': 'callback', 'texts':[''], 'callbacks':[min(index + 1, len(tree.form.stages[stage].imgs) - 1)]},
			{'type': 'callback', 'texts':[''], 'callbacks':[index]},
		]
		keyboard = create_keyboard(tree.form.stages[stage].buttons, currentInlineState)

		bot.send_photo(chat_id=userId, 
					   photo=tree.form.stages[stage].imgs[index], 
					   caption=tree.form.stages[2].text,
					   reply_markup=keyboard)
	elif stage == 5: # Show selected things		
		bot.send_photo(chat_id=userId, photo=tree.form.stages[4].imgs[user['toy_choice']])  # Toy choice
		bot.forward_message(userId, userId, user['photo_check'])		 					# Check

		currentInlineState = [keyFormat, keyFormat]											# Confirmation message
		keyboard = create_keyboard(tree.form.stages[stage].buttons, currentInlineState)
		bot.send_message(userId, tree.form.stages[stage].text.format(user['name'], user['address'], user['phone']), reply_markup=keyboard)
	elif stage == 6: # Confirmed
		currentInlineState = [keyFormat]
		keyboard = create_keyboard(tree.form.stages[stage].buttons, currentInlineState)
		bot.send_message(userId, tree.form.stages[stage].text, reply_markup=keyboard)


		# Send photo of a receipt to channel for confirmation
		bot.forward_message(groupChatId, userId, user['photo_check'])
		currentInlineState = [{'type': 'callback', 'texts':[''], 'callbacks':[userId]},
							  {'type': 'callback', 'texts':[''], 'callbacks':[userId]}]
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