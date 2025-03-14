from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.l10n.l10n import Message as L10nMessage
# from database.requests import user_requests
from datetime import datetime



async def progress_kb(language_code: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text = "Трекінг", callback_data = "track_button"),
        InlineKeyboardButton(text = "Графік", callback_data = "graph_button")
    )
    keyboard.row(
        InlineKeyboardButton(text = "Назад до меню", callback_data = "back_to_menu_button")
    )
    return keyboard.as_markup()



async def track_kb(language_code: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text = "Назад до трекінгу", callback_data = "back_to_progress_button")
    )
    keyboard.row(
        InlineKeyboardButton(text = "Назад до меню", callback_data = "back_to_menu_button")
    )
    return keyboard.as_markup()
