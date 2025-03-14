from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.l10n.l10n import Message as L10nMessage
# from database.requests import user_requests
from datetime import datetime



async def settings_kb(language_code: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text = "Кількість сигарет", callback_data = "cigarette_count_button"),
        InlineKeyboardButton(text = "Ціна сигарет", callback_data = "cigarette_price_button")
    )
    keyboard.row(
        InlineKeyboardButton(text = "Назад до меню", callback_data = "back_to_menu_button")
    )
    return keyboard.as_markup()



async def setSettings_kb(language_code: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text = "Назад до налаштувань", callback_data = "back_to_settings_button")
    )
    return keyboard.as_markup()
