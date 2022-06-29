from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from configs import *
from keyboars import generate_languages
from googletrans import Translator
import sqlite3

storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)


class GetLanguages(StatesGroup):
    src = State()
    dest = State()
    text = State()


@dp.message_handler(commands=['start', 'help', 'sponsor'])
async def command_start(message: Message):
    if message.text == '/start':
        await message.answer(f'''<b>Здравстуйте</b> <i>{message.from_user.full_name}</i>!🙋‍♂️


<b>Я бот переводчик. Давайте начнем!</b>🧐''')
        await get_first_language(message)
    elif message.text == '/help':
        await message.answer(
            '''<b>При возникшем проблеме можете обращаться к</b> <tg-spoiler>@sadnesshistoryinelif</tg-spoiler>''')
    elif message.text == '/sponsor':
        await message.answer(f'''<b>Если хотите поддержать или подать рекламу
То можите обращаться к</b> <tg-spoiler>@sadnesshistoryinelif</tg-spoiler>''')


async def get_first_language(message: Message):
    await GetLanguages.src.set()
    await message.answer('<b>Выберите язык</b> 🌍: ', reply_markup=generate_languages())


@dp.message_handler(content_types=['text'], state=GetLanguages.src)
async def get_second_language(message: Message, state: FSMContext):
    if message.text in ['/start', '/help', '/sponsor']:
        await command_start(message)
    else:
        async with state.proxy() as data:
            data['src'] = message.text

        await GetLanguages.next()
        await message.answer('<b>Отправьте мне текст, который вам нужно перевести</b> 🔍: ',
                             reply_markup=generate_languages())


@dp.message_handler(content_types=['text'], state=GetLanguages.dest)
async def get_text(message: Message, state: FSMContext):
    if message.text in ['/start', '/help', '/sponsor']:
        await command_start(message)
    else:
        async with state.proxy() as data:
            data['dest'] = message.text
        await GetLanguages.next()
        await message.answer('Введите текст, который хотите перевести', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=['text'], state=GetLanguages.text)
async def translate_function(message: Message, state: FSMContext):
    if message.text in ['/start', '/help', '/sponsor']:
        await command_start(message)
    else:
        async with state.proxy() as data:
            data['text'] = message.text
        #         await message.answer(f'''Язык с которого вы переводите: {data['src']}
        # На который {data['dest']}
        # Текст: {data['text']}''')
        danil = Translator()
        src = get_key(data['src'])
        dest = get_key(data['dest'])

        result = danil.translate(text=data['text'],
                                 src=src,
                                 dest=dest).text
        await message.answer(result)
        await state.finish()
        database = sqlite3.connect('bot.db')
        cursor = database.cursor()

        cursor.execute('''
        INSERT INTO translate(telegram_id, src, dest, original_text, translated_text)
        VALUES (?,?,?,?,?)
        ''', (message.chat.id, src, dest, message.text, result))
        database.commit()
        database.close()

        await get_first_language(message)


executor.start_polling(dp)
