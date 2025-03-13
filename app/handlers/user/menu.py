from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from app.l10n.l10n import Message as L10nMessage
from database.requests import getUser
from app.keyboards import mainMenu_kb

router = Router()




@router.callback_query(F.data == "back_to_menu_button")
async def backToMenuButton(callback: CallbackQuery, language_code: str):
    text = await mainMenu(callback.from_user.id, language_code)
    await callback.message.edit_text(text, reply_markup = await mainMenu_kb(language_code))
    await callback.answer()



async def mainMenu(tg_id: int, language_code: str):
    user = await getUser(tg_id)
    if user.cigarette_count != 0 and user.cigarette_price != 0:
        
        text = L10nMessage.get_message(language_code, "menu").format(
            price = user.cigarette_price,
            count = user.cigarette_count,
            price_7 = (user.cigarette_count * 7) / 20 * user.cigarette_price,
            count_7 = user.cigarette_count * 7,
            price_30 = (user.cigarette_count * 30) / 20 * user.cigarette_price,
            count_30 = user.cigarette_count * 30
        )
    else:
        text = L10nMessage.get_message(language_code, "welcome")

    return text
