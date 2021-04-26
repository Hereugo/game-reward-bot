from functions import Map 
from PIL import Image
TOKEN = '1724144036:AAHUrJz65gV8AkoTp5UIou8roCA3dqnSuzs'
URL = 'https://work-dad.herokuapp.com/'
URI = 'mongodb+srv://Amir:2LSCfSNcwAz9x3!@cluster0.jxsw1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

TEMPLATE_MESSAGE = 'Напиши /start чтобы разбудить меня... 😴'


gifts = [
	Image.open('./images/girls_lol.png'),
	Image.open('./images/boys_cars.png')
]
gifts_names = [
	'Girl Lol',
	'Boy Cars'
]
tree = Map({
	'menu': {
		'text': 'Привет!😀 Только у нас дети 👼 получают подарки 🎁 играя в любимые игры! 🎮',
		'buttons': [
			[
				{
					'text': 'Выбрать подарок! 🎁',
					'callback': 'list_gifts?0',
				},
			],
			[
				{
					'text': 'Выбрать игру! 🎮',
					'callback': 'list_games?0',
				},
			],
			[
				{
					'text': 'Условия получения подарка 📋',
					'callback': 'сonditions',
				},
			],
			[
				{
					'text': 'Задать вопрос 📞',
					'callback': 'ask_question',
				},
			]
		],
	},
	'list_gifts': {
		'messages': [
			{
				'image': gifts[0],
			},
			{
				'image': gifts[1],
			},
		],
		'buttons': [
			[
				{
					'text': '<',
					'callback': 'list_gifts?{}',
				},
				{
					'text': 'Хочу это!',
					'callback': 'list_gifts2?{}',
				},
				{
					'text': '>',
					'callback': 'list_gifts?{}'
				}
			],
			[
				{
					'text': 'Назад 🏘',
					'callback': 'menu',
				}
			],
		]
	},
	'list_gifts2': {
		'buttons': [
			[
				{
					'text': 'Выбрать игру! 🎮',
					'callback': 'list_games?0',
				},
			],
			[
				{
					'text': 'Назад 🏘',
					'callback': 'menu',
				}
			],
		]
	},
	'list_games': {
		'messages': [
			{
				'image': Image.open('./images/doodle_jump.png'),
				'text': 'Покажи как далеко ты прыгаешь с Doodle Jump! До небес 🌤 не высоко! Всего лишь 5000 очков и подарок 🎁 твой!',
				'url': 'https://doodle-jump.hereugo.repl.co/?id={}',
			},
			{
				'image': Image.open('./images/spiderman.png'),
				'text': 'Любимый Spiderman 🕷, ему осталось всего 10 000 метров до подарка! 🎁',
				'url': 'https://spiderman.hereugo.repl.co/?id={}',
			},
			{
				'image': Image.open('./images/drovosek.png'),
				'text': 'Дровосек против полчища деревьев 🌲 и веток! Наруби 500 деревьев и забирай ПРИЗ! 🎁',
				'url': 'https://drovosek.nomomon.repl.co/?id={}',
			}
		],
		'buttons': [
			[
				{
					'text': '<',
					'callback': 'list_games?{}',
				},
				{
					'text': 'Играть!',
					'url': '{}',
				},
				{
					'text': '>',
					'callback': 'list_games?{}'
				}
			],
			[
				{
					'text': 'Назад 🏘',
					'callback': 'menu',
				}
			],
		]
	},
	'сonditions': {
		'text': 'Для получения подарка вам нужно :\n\n1. Купить игрушку в магазинах наших партнеров со стикером "ПОЛУЧИ ПРИЗ!"\n2. Сохранить чек подтвердающий покупку игрушки\n3. Набрать нужное кол-во очков для получения ПРИЗА\n',
		'buttons': [
			[
				{
					'text': 'Список партнеров 🏪',
					'callback': 'list_partners',
				},
			],
			[
				{
					'text': 'Назад 🏘',
					'callback': 'menu',
				}
			]
		]	
	},
	'list_partners': {
		'text': 'СПИСОК ПАРТНЕРОВ\n\n1. Сеть супермаркетов "Small"',
		'buttons': [
			[
				{
					'text': 'Назад 🏘',
					'callback': 'menu'
				}
			]
		]
	},
	'ask_question': {
		'text': 'В : Я купила игрушку НЕ в магазинах SMALL. Можно ли использовать другой чек?\nО : НЕТ. В акции участвуют только чеки магазинов SMALL\n\nВ : Я купила игрушку без стикера "ПОЛУЧИ ПРИЗ". Можно ли использовать такой чек?\nО : НЕТ. В акции участвуют только чеки подтверждающие покупку игрушки со стикером "ПОЛУЧИ ПРИЗ!"\n\nВ : Можно сначала попытаться выиграть приз, а потом предоставить чек о покупке?\nО : ДА. Вы можете играть до тех пор пока не добьетесь результата.\n\nВ : Сколько подарков можно получить по чеку?\nО : Один чек = один подарок. В случае если в чеке > 2  игрушек со стикером, то один стикер = один подарок.\n\nВ : Как я узнаю что выиграл Подарок?\nО : По достижении нужного количества баллов, вы получите в переписке с ботом форму для выбора подарка и заполнения формы контактов.\n\nВ : Бот написал, что чек недействителен, что делать?\nО : Проверьте соблюдение всех условий, а также четкости фотографии чека. Свяжитесь с оператором.',
		'buttons': [
			[
				{
					'text': 'Задать вопрос оператору 📞',
					'callback': 'question',
				}
			],
			[
				{
					'text': 'Назад 🏘',
					'callback': 'menu',
				}
			]
		]
	},
	'question': {
		'text': 'Напишите нашему оператору @H_reugo 📞, он вам обязательно ответит 👨‍💻',
		'buttons': [
			[
				{
					'text': 'Назад 🏘',
					'callback': 'menu',
				}
			]
		]
	},

	'confirmation': {
		'text': 'Подтвердите чек пользователя @{}',
		'buttons': [
			[
				{
					'text': 'Одобрить ✅',
					'callback': 'confirm?yes,{}',				
				},
				{
					'text': 'Отвергнуть ❌',
					'callback': 'confirm?no,{}',
				}
			]
		]
	},
	'confirm': {
		'text': [
			'Извини, но с твоим чеком что-то не то 😢',
			'Твой чек успешно подтверждён! Ждите звонка нашего курьера 📞! До свидания! 👋',
			'Пользователь был {}',
			'ДАННЫЕ О ПОЛЬЗОВАТЕЛЕ:\n\nИмя: {}\nАдрес: {}\nТелефон: {}\nСвязаться с пользователям: @{}',
		],
	},

	'form': {
		'text': 'Ура! Поздравляю с выигрышем! 🤩💐🎉🎊 Твой подарок 🎁 уже ждёт тебя! Ответь на пару вопросов, чтобы забрать Приз!😀',
		'stages': [
			[
				{
					'text': 'Напиши как тебя зовут?',
					'next_step': 'form?1,name',
				}
			],
			[
				{
					'text': 'Адрес доставки 📦🚚',
					'next_step': 'form?2,address'
				},
			],
			[
				{
					'text': 'Контактный номер 📞',
					'next_step': 'form?3,phone'
				},
			],
			[
				{
					'text': 'Мне также понадобится проверить твой чек🔍🛒🛍👀, отправь пожалуйста четкое фото 📸🗞',
					'next_step': 'form?4,photo_check,0',
				}
			],
			[
				{
					'text': 'Выбери приз!😋',
					'buttons': [
						[
							{
								'text': '<',
								'callback': 'form?4,#,{}'
							},
							{
								'text': '>',
								'callback': 'form?4,#,{}',
							}
						],
						[
							{
								'text': 'Хочу это!',
								'callback': 'form_complete?5,toy_choice,{}',
							}
						]
					],
					'prize': True,
					'next_step': '#',
				},
				{
					'text': 'Фото чека плиз!😂😂🙏🙏',
					'next_step': 'form?4,photo_check,0',
				}
			],
			[
				{
					'text': 'Спасибо! Мне нужно немного времени для проверки чека, будьте на связи!',
					'buttons': [
						[
							{
								'text': 'Обратно в меню 🏘',
								'callback': 'menu',
							}
						]
					]
				}
			]
		],
		'buttons': [
			[
				{
					'text': 'Я готов',
					'callback': 'form?0,#',
				}
			]
		]
	}
})