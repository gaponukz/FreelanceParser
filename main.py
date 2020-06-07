from aiogram import Bot, Dispatcher, executor, types
from db import SQLiter, Parse
import asyncio
import codecs

bot = Bot(token = 'API_KEY')
dp = Dispatcher(bot)
db = SQLiter('db.db')

@dp.message_handler(commands = ['subscribe'])
async def subscribe(message: types.Message):
	if not db.user_exists(message.from_user.id):
		db.add_user(message.from_user.id)
	else:
		db.update_user(message.from_user.id, True)

	await message.answer("Вы успешно подписались на рассылку!")

@dp.message_handler(commands = ['unsubscribe'])
async def unsubscribe(message: types.Message):
	if not db.user_exists(message.from_user.id):
		db.add_user(message.from_user.id, False)
		await message.answer("Вы итак не подписаны.")
	else:
		db.update_user(message.from_user.id, False)
		await message.answer("Вы успешно отписаны от рассылки!")

async def sheduler(wait_for):
	while True:
		await asyncio.sleep(wait_for)
		data = codecs.open( "lastwork.txt", "r", "utf_8_sig" ).read().split('\n')
		post = Parse('https://freelance.ua/orders/?page=1&st=2&clear=1')
		users = db.get_users()

		difference = [item for item in post.urls if item not in data]

		if difference:
			post.write_data()
			for user in users:
				await bot.send_message(user[1], text = difference[0])

if __name__ == '__main__':
	dp.loop.create_task(sheduler(10))
	executor.start_polling(dp, skip_updates = True)
