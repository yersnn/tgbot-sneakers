from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import app.keyboards as kb
import app.database.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Welcome to the sneaker store!', reply_markup=kb.main)


@router.message(F.text == 'Catalog')
async def catalog(message: Message):
    await message.answer('Sneaker brand', reply_markup=await kb.categories())

@router.message(F.text == 'Contacts')
async def contacts(message: Message):
    await message.answer('Managers phone: +77771234567 \nManagers email: example@gmail.com')

@router.message(F.text == 'About us')
async def about_us(message: Message):
    await message.answer('This is a test Telegram bot that sells Snickers online. Not a real store')


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.message.answer('Select sneaker model',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.message.answer(f'Model: {item_data.name}\nDescription: {item_data.description}\nPrice: {item_data.price}$')