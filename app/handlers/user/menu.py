from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from app.l10n.l10n import Message as L10nMessage
from database.requests import getUser
from app.keyboards import mainMenu_kb
from app.core.utils import mainMenu

router = Router()




@router.callback_query(F.data == "back_to_menu_button")
async def backToMenuButton(callback: CallbackQuery, language_code: str, state: FSMContext):
    text = await mainMenu(callback.from_user.id, language_code)
    await callback.message.edit_text(text, reply_markup = await mainMenu_kb(language_code))
    await callback.answer()
    
    # Очищаем состояние
    await state.clear()




