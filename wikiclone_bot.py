from aiogram import Bot, executor, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle

import os
import hashlib


async def on_startup(_):
    print('Bot is online.')


async def on_shutdown(_):
    print('Bot is offline')


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text = query.query or 'Заглавная_страница'
    link = 'https://ru.wikipedia.org/wiki/' + text
    result_id: str = hashlib.md5(text.encode()).hexdigest()

    articles = [types.InlineQueryResultArticle(
        id=result_id,
        title='Статья Википедии: ',
        url=link,
        input_message_content=types.InputTextMessageContent(
            message_text=link
        ))]

    await query.answer(results=articles, cache_time=1, is_personal=True)


executor.start_polling(dp, skip_updates=True,
                       on_startup=on_startup, on_shutdown=on_shutdown)
