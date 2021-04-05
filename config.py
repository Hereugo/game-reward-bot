from functions import Map 
from PIL import Image
TOKEN = '1272925344:AAGArvS0kwYUB8W0wL3EufrsGn8kNRGar9w'
URL = ''

tree = Map({
	'menu': {
		'text': 'Здраствуйте я бот которой вы запустили я могу выдать приз когда вы выйграете игру!',
		'buttons': [
			[
				{
					'text': 'Список Игр',
					'callback': 'list_games?0',
				},
			],
			[
				{
					'text': 'Загурзить чек',
					'callback': 'get_check',
				},
			],
			[
				{
					'text': 'Условия',
					'callback': 'сonditions',
				},
			],
			[
				{
					'text': 'Задать вопрос',
					'callback': 'ask_question',
				},
			]
		],
	},
	'list_games': {
		'messages': [
			{
				'image': Image.open('./images/doodle_jump.png'),
				'text': 'Это игра doodle jump, набирите 5000 очков чтобы получить приз!',
				'url': 'https://doodle-jump.hereugo.repl.co/?{}',
			},
			{
				'image': Image.open('./images/spiderman.png'),
				'text': 'Интересная игра про spiderman-а пройдите 10000 метров чтобы получить приз!',
				'url': 'https://spiderman.hereugo.repl.co/?{}',
			},
			{
				'image': Image.open('./images/drovosek.png'),
				'text': 'Любишь играть в игры? Если да то вам понравится drovosek срубите 500 деревьев чтобы получить приз!',
				'url': 'https://drovosek.nomomon.repl.co/?{}',
			}
		],
		'buttons': [
			[
				{
					'text': '<',
					'callback': 'list_games?{}',
				},
				{
					'text': 'Играть в игру!',
					'url': '{}',
				},
				{
					'text': '>',
					'callback': 'list_games?{}'
				}
			],
			[
				{
					'text': 'Назад',
					'callback': 'menu',
				}
			],
		]
	},
	'get_check': {
		'text': [
			'Отправьте фото чека на проверку',
			'Пужалуйтса отправьте ФОТО чека',
			'Ваша фото принета на проверку, ждите когда проверят фото',
		],
		'buttons': [
			[
				{
					'text': 'Назад',
					'callback': 'menu',
				}
			]
		]
	},
	'сonditions': {
		'text': 'Условия\n\nДля получение приза должно выполнятся 2 условия:\n1) Чек действителен. Чек действителен если он из АЗС магазина и вы купили игрушку с стикером\n2) Вы набрали достаточное количество очков в игре',
		'buttons': [
			[
				{
					'text': 'Назад',
					'callback': 'menu',
				}
			]
		]	
	},
	'ask_question': {
		'text': 'FAQ\n\n Q) blah blah blah?\n A) blah blah blah blah!\n\n Q) blah blah?\n A) blah...',
		'buttons': [
			[
				{
					'text': 'Не помогло задать вопрос',
					'callback': 'question',
				}
			],
			[
				{
					'text': 'Назад',
					'callback': 'menu',
				}
			]
		]
	},
	'question': {
		'text': 'Свяжитесь с нашим операторам @H_reugo, вам ответ дадут как только сможем',
		'buttons': [
			[
				{
					'text': 'Назад',
					'callback': 'menu',
				}
			]
		]
	},

	'confirmation': {
		'text': 'Потвиредите чек пользователья @{}',
		'buttons': [
			[
				{
					'text': 'Одобрить',
					'callback': 'confirm?yes,{}',				
				},
				{
					'text': 'Отвергнуть',
					'callback': 'confirm?no,{}',
				}
			]
		]
	},
	'confirm': {
		'text': [
			'Извените но ваш чек не приняли',
			'Ваш чек успешно приняли ждите свой приз!',
			'Пользователь был {}',
		],
	}
})