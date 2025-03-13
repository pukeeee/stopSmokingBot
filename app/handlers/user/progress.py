from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery, FSInputFile, BufferedInputFile
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from app.states import Setting, Plan
from app.l10n.l10n import Message as L10nMessage
from database.requests import getCigaretteCount, getCigarettePrice, setCigaretteCount, setCigarettePrice, getUser, setPlan
from app.keyboards import settings_kb, setSettings_kb, plan_kb, checkPlan_kb, progress_kb
from app.core.utils.create_graph import create_plan_graph
import matplotlib.pyplot as plt
import io


router = Router()


@router.callback_query(F.data == "progress_button")
async def progress_callback(callback: CallbackQuery, language_code: str):
    await callback.message.edit_text(L10nMessage.get_message(language_code, "progress"), reply_markup = await progress_kb(language_code))
    await callback.answer()



@router.callback_query(F.data == "graph_button")
async def graph_callback(callback: CallbackQuery, language_code: str):
    user = await getUser(callback.from_user.id)
    plan = user.plan
    actual = user.actual
    
    graph = await create_plan_graph(plan, actual)
    await callback.message.answer_photo(
        photo=BufferedInputFile(
            graph.getvalue(),
            filename="smoking_plan.png"
        ),
        caption="План по дням:"
    )
    await callback.answer()

