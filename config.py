from functions import Map 
from PIL import Image
TOKEN = '1272925344:AAGArvS0kwYUB8W0wL3EufrsGn8kNRGar9w'
URL = 'https://work-dad.herokuapp.com/'
URI = 'mongodb+srv://Amir:2LSCfSNcwAz9x3!@cluster0.jxsw1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

TEMPLATE_MESSAGE = 'Nothing to see here, '

tree = Map({
	'menu': {
		'text': 'Привет! Только у нас дети получают подарки играя в любимые игры!',
		'buttons': [
			[
				{
					'text': 'Выбрать игру',
					'callback': 'list_games?0',
				},
			],
			[
				{
					'text': 'Условия получения подарка',
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
				'text': 'Покажи как далеко ты прыгаешь с Doodle Jump!  До небес не высоко! Всего лишь 5000 очков и подарок твой!',
				'url': 'https://doodle-jump.hereugo.repl.co/?id={}',
			},
			{
				'image': Image.open('./images/spiderman.png'),
				'text': 'Любимый Spiderman, ему осталось всего 10 000 метров до подарка!',
				'url': 'https://spiderman.hereugo.repl.co/?id={}',
			},
			{
				'image': Image.open('./images/drovosek.png'),
				'text': 'Drovosek против полчища деревьев и веток! Наруби 500 деревьев и забирай ПРИЗ!',
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
					'text': 'Хочу играть!',
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
	'сonditions': {
		'text': 'Для получения подарка вам нужно :\n\n1. Купить игрушку в магазинах наших партнеров со стикером "ПОЛУЧИ ПРИЗ!"\n2. Сохранить чек подтвердающий покупку игрушки\n3. Набрать нужное кол-во очков для получения ПРИЗА\n',
		'buttons': [
			[
				{
					'text': 'Список партнеров',
					'callback': 'list_partners',
				},
			],
			[
				{
					'text': 'Назад',
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
					'text': 'Назад',
					'callback': 'menu'
				}
			]
		]
	},
	'ask_question': {
		'text': 'В : Я купила игрушку НЕ в магазинах SMALL. Можно ли использовать другой чек?\n\nО : НЕТ. В акции участвуют только чеки магазинов SMALL\n\nВ : Я купила игрушку без стикера "ПОЛУЧИ ПРИЗ". Можно ли использовать такой чек?\n\nО : НЕТ. В акции участвуют только чеки подтверждающие покупку игрушки со стикером "ПОЛУЧИ ПРИЗ!"\n\nВ : Можно сначала попытаться выиграть приз, а потом предоставить чек о покупке?\n\nО : ДА. Вы можете играть до тех пор пока не добьетесь результата.\n\nВ : Сколько подарков можно получить по чеку?\n\nО : Один чек = один подарок. В случае если в чеке > 2  игрушек со стикером, то один стикер = один подарок.\n\nВ : Как я узнаю что выиграл Подарок?\n\nО : По достижении нужного количества баллов, вы получите в переписке с ботом форму для выбора подарка и заполнения формы контактов.\n\nВ : Бот написал, что чек недействителен, что делать?\n\nО : Проверьте соблюдение всех условий, а также четкости фотографии чека. Свяжитесь с оператором.',
		'buttons': [
			[
				{
					'text': 'Задать вопрос оператору',
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
	},

	'form': {
		'text': 'Начать форму',
		'stages': [
			{
				'text': 'Напишите нам Имя, фамилия. Это делайется для конформатции вас'
			},
			{
				'text': ['Загурзите чек покупки игрушки',
						 'Пожалуйста отправте фото для продолжение формы']
			},
			{
				'text': 'Выбирите игрушку',
				'imgs': [
					Image.open('./images/spongebob_toy.png'),
					Image.open('./images/cars_toy.png'),
					Image.open('./images/fox_toy.png')
				],
				'buttons': [
					[
						{
							'text': '<',
							'callback': 'form?2,{},#'
						},
						{
							'text': '>',
							'callback': 'form?2,{},#',
						}
					],
					[
						{
							'text': 'Выбрать это игрушку',
							'callback': 'form?3,{},toy_choice',
						}
					]
				]
			},
			{
				'text': 'Имя и фамилия: {}\n',
				'buttons': [
					[
						{
							'text': 'Потвиредить',
							'callback': 'form?4,#,#',
						}
					],
					[
						{
							'text': 'Поменять',
							'callback': 'form?0,#,#',
						}
					]
				]
			},
			{
				'text': 'Все готово! Подождите пока мы проверим ваш чек',
				'buttons': [
					[
						{
							'text': 'Обратно в меню',
							'callback': 'menu',
						}
					]
				]
			}
		],
		'buttons': [
			[
				{
					'text': 'Начать',
					'callback': 'form?0,#,#',
				}
			]
		]
	}
})