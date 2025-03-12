from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from app.states import Setting
from app.l10n.l10n import Message as L10nMessage
from database.requests import getCigaretteCount, getCigarettePrice, setCigaretteCount, setCigarettePrice
from app.keyboards import settings_kb, setSettings_kb


router = Router()



@router.callback_query(F.data == 'settings_button')
async def settings_handler(callback: CallbackQuery, language_code: str):
    await callback.message.edit_text(L10nMessage.get_message(language_code, "settings"), reply_markup = await settings_kb(language_code))
    await callback.answer()


@router.callback_query(F.data == "cigarette_count_button")
async def cigaretteCount_button(callback: CallbackQuery, language_code: str, state: FSMContext):
    await state.set_state(Setting.setCigaretteCount)
    
    count = await getCigaretteCount(callback.from_user.id)
    await callback.message.edit_text(L10nMessage.get_message(language_code, "cigarette_count").format(count = count), reply_markup = await setSettings_kb(language_code))



@router.callback_query(F.data == "cigarette_price_button")
async def cigarettePrice_button(callback: CallbackQuery, language_code: str, state: FSMContext):
    await state.set_state(Setting.setCigarettePrice)
    
    price = await getCigarettePrice(callback.from_user.id)
    await callback.message.edit_text(L10nMessage.get_message(language_code, "cigarette_price").format(price = price), reply_markup = await setSettings_kb(language_code))



@router.callback_query(F.data == "back_to_settings_button")
async def backToSettingsHandler(callback: CallbackQuery, language_code: str, state: FSMContext):
    await settings_handler(callback, language_code)
    await state.clear()



@router.message(Setting.setCigaretteCount)
async def setCigaretteCount_handler(message: Message, state: FSMContext, language_code: str):
    count = message.text
    await state.update_data(cigarette_count = count)
    
    await setCigaretteCount(message.from_user.id, count)
    await message.answer(L10nMessage.get_message(language_code, "cigarette_count").format(count = count),
                                    reply_markup = await setSettings_kb(language_code))



@router.message(Setting.setCigarettePrice)
async def setCigarettePrice_handler(message: Message, state: FSMContext, language_code: str):
    price = message.text
    await state.update_data(cigarette_price = price)
    
    await setCigarettePrice(message.from_user.id, price)
    await message.answer(L10nMessage.get_message(language_code, "cigarette_price").format(price = price),
                                    reply_markup = await setSettings_kb(language_code))