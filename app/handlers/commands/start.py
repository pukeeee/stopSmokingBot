from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from app.l10n.l10n import Message as L10nMessage
from database.requests import getUser, createUser
from app.keyboards import mainMenu_kb
from app.handlers.user.menu import mainMenu
router = Router()



@router.message(CommandStart())
async def welcome(message: Message, language_code: str):
    user = await getUser(message.from_user.id)
    
    if not user:
        await createUser(message.from_user.id)
    
    text = await mainMenu(message.from_user.id, language_code)
    await message.answer(text, reply_markup = await mainMenu_kb(language_code))