from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from app.l10n.l10n import Message as L10nMessage
# from database.requests import example
# from app.keyboards import example

router = Router()


@router.message(F.text == 'example')
async def example_command(message: Message):
    await message.answer('example')


@router.callback_query(F.data == 'example_button')
async def example_callback(callback: CallbackQuery):
    await callback.message.answer('example')
