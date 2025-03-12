from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.l10n.l10n import Message as L10nMessage
# from database.requests import user_requests
from datetime import datetime



async def mainMenu_kb(language_code: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text=L10nMessage.get_message(language_code, "plan_button"), callback_data = "plan_button"),
        InlineKeyboardButton(text=L10nMessage.get_message(language_code, "progress_button"), callback_data = "progress_button")
    )
    keyboard.row(
        InlineKeyboardButton(text=L10nMessage.get_message(language_code, "settings_button"), callback_data = "settings_button")
    )
    return keyboard.as_markup()
