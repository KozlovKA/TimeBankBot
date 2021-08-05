from time import sleep

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram import Bot, Dispatcher, executor, types, utils
from aiogram import Bot, Dispatcher, executor
import datetime
import asyncio
import botConfig
import jsonRequests
from database import *

bot = Bot(token=botConfig.TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
db = SQLighter('db.db')



@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(
        "  Здраствуйте, добро пожаловать в бота TimeBank!\n"
        "  Банк Времени - это еврейская волонтерская платформа Беларуси.\n"
        "  Данный бот предоставляет возможность получать уведомления о помощи, требуемой людям.\n"
        "  О концепции проекта вы можете ознакомиться по ссылке - https://timebank.by/about_us\n"
        "  Для получения более подробной информации о функциоанале бота наберите /help ")


# команда вызова описания команд

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    """
    This handler will be called when user sends /help
    """
    await message.reply(
        "/help - открыть список доступных команд с описанием\n"
        "/subscribe - подписаться на рассылку уведомлений\n"
        "/unsubscribe - отписаться от рассылки")


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    """
        This handler will be called when user sends /subscribe
        """
    user_fio = message.from_user.full_name
    if not db.subscriber_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id, user_fio)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, True)

    await message.answer(
        "Вы успешно подписались на рассылку!")


# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписаны от рассылки.")


async def notifier(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        subscriptions = db.get_subscriptions()
        for s in subscriptions:
            if jsonRequests.post_checking():
                await bot.send_message(s[1], jsonRequests.notification_message())
            sleep(20)


@dp.message_handler()
async def none(message: types.Message):
    await message.answer("Такой комманды не существует, введите /help для помощи")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(notifier(25))
    executor.start_polling(dp, skip_updates=True)

# @bot.message_handler(commands=["start"])  # Обработка /start
# def handle_start(message):
#     bot.send_message(message.from_user.id, 'Hi! \nMy friend')


# @bot.message_handler(content_types=["text"])
# def handle_t(message):
#     if message.text[:7] == "Погода " or message.text[:7] == "погода ":
#         city = message.text[7:]
#         r = requests.get(
#             'http://api.openweathermap.org/data/2.5/weather?&units=metric&q=%s&appid=0c9f3c052f1d81b7062750ff0926f345<img src="https://habrastorage.org/files/8fa/5f5/313/8fa5f5313b37438eb250b22cf041f2dd.png" alt="image"/>' % (
#                 city))
#         data = r.json()
#         temp = data["main"]["temp"]
#         bot.send_message(message.chat.id, "Температура в {}: {} C".format(city, temp))
#
#
# bot.polling(none_stop=True, interval=0)
