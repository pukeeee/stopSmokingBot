from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.l10n.l10n import Message as L10nMessage
# from database.requests import example
from datetime import datetime



async def example_kb(language_code: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text=L10nMessage.get_message(language_code, "example_button"), callback_data="example_button")
    )
    return keyboard.as_markup()
