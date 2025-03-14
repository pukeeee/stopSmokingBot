from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.l10n.l10n import Message as L10nMessage
# from database.requests import user_requests
from datetime import datetime



async def plan_kb(language_code: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text = "Почати план", callback_data = "start_plan_button")
    )
    keyboard.row(
        InlineKeyboardButton(text = "Назад до меню", callback_data = "back_to_menu_button")
    )
    return keyboard.as_markup()



async def checkPlan_kb(language_code: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text = "Зберегти план", callback_data = "done_plan_button")
    )
    keyboard.row(
        InlineKeyboardButton(text = "Назад до плану", callback_data = "back_to_plan_button")
    )
    return keyboard.as_markup()
