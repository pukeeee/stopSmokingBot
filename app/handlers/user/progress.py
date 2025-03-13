from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery, FSInputFile, BufferedInputFile, InputMediaPhoto
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from app.states import Setting, Plan
from app.l10n.l10n import Message as L10nMessage
from database.requests import getCigaretteCount, getCigarettePrice, setCigaretteCount, setCigarettePrice, getUser, setPlan
from app.keyboards import settings_kb, setSettings_kb, plan_kb, checkPlan_kb, progress_kb
from app.core.utils.create_graph import create_plan_graph
from app.core.utils.graph_message import graph_message
import matplotlib.pyplot as plt
import io


router = Router()


@router.callback_query(F.data == "progress_button")
async def progress_callback(callback: CallbackQuery, language_code: str, key: bool = None):
    user = await getUser(callback.from_user.id)
    plan_days = len(user.actual)
    plan_days_left = len(user.plan) - len(user.actual)
    
    if key:
        await callback.message.answer(L10nMessage.get_message(language_code, "progress").format(
            plan_days = plan_days, plan_days_left = plan_days_left
        ), reply_markup = await progress_kb(language_code))
    
    else:
        await callback.message.edit_text(L10nMessage.get_message(language_code, "progress").format(
            plan_days = plan_days, plan_days_left = plan_days_left
        ), reply_markup = await progress_kb(language_code))
    
    await callback.answer()



@router.callback_query(F.data == "graph_button")
async def graph_callback(callback: CallbackQuery, language_code: str):
    user = await getUser(callback.from_user.id)
    plan = user.plan
    actual = user.actual
    
    message = await graph_message(callback.from_user.id, plan, user.cigarette_count, language_code)
    graph = await create_plan_graph(plan, actual)
    
    await callback.message.edit_media(
        media = InputMediaPhoto(
            media = BufferedInputFile(
                graph.getvalue(),
                filename="smoking_plan.png"
            ),
            caption = message
        )
    )
    await callback.answer()
    
    await progress_callback(callback, language_code, key = True)

