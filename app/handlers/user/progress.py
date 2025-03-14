from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery, FSInputFile, BufferedInputFile, InputMediaPhoto
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from app.states import Setting, Plan, Track
from app.l10n.l10n import Message as L10nMessage
from database.requests import updateUserActual, getUser
from app.keyboards import settings_kb, setSettings_kb, plan_kb, checkPlan_kb, progress_kb, track_kb
from app.core.utils import create_plan_graph, graph_message, format_tracking_message, get_tracking_date
import matplotlib.pyplot as plt
import io
from datetime import datetime, timedelta

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



@router.callback_query(F.data == "track_button")
async def track_callback(callback: CallbackQuery, language_code: str, state: FSMContext):
    user = await getUser(callback.from_user.id)
    
    startDate = datetime.fromtimestamp(user.plan_date)
    today = datetime.now()
    days_passed = (today.date() - startDate.date()).days
    
    tracking_day = len(user.actual)
    if tracking_day > days_passed:
        tracking_day = days_passed
    
    track_date = await get_tracking_date(callback.from_user.id, tracking_day)
    await state.update_data(tracking_day=tracking_day)
    
    if tracking_day < len(user.actual):
        count = user.actual[tracking_day]
        message = await format_tracking_message(tracking_day, track_date, count)
    else:
        message = await format_tracking_message(tracking_day, track_date, is_input_required=True)
    
    await callback.message.edit_text(message, reply_markup=await track_kb(language_code))
    await state.set_state(Track.trackCigarettes)
    await callback.answer()



@router.message(Track.trackCigarettes)
async def track_cigarettes_message(message: Message, language_code: str, state: FSMContext):
    try:
        count = int(message.text)
        if count < 0:
            await message.answer("Кількість не може бути від'ємною")
            return
        
        user = await getUser(message.from_user.id)
        today = datetime.now()
        days_passed = (today.date() - datetime.fromtimestamp(user.plan_date).date()).days
        
        state_data = await state.get_data()
        tracking_day = state_data.get('tracking_day', 0)
        
        if tracking_day >= len(user.actual):
            user.actual.append(count)
        else:
            user.actual[tracking_day] = count
            
        await updateUserActual(message.from_user.id, user.actual)
        
        next_tracking_day = tracking_day + 1
        if next_tracking_day <= days_passed:
            next_track_date = await get_tracking_date(message.from_user.id, next_tracking_day)
            await state.update_data(tracking_day=next_tracking_day)
            
            message_text = (
                f"✅ Збережено: {count} сигарет\n\n"
                f"Тепер введи кількість за наступний день:\n"
            ) + await format_tracking_message(next_tracking_day, next_track_date, is_input_required=True)
            
            await message.answer(message_text, reply_markup=await track_kb(language_code))
        else:
            track_date = await get_tracking_date(message.from_user.id, tracking_day)
            message_text = await format_tracking_message(tracking_day, track_date, count)
            message_text = f"✅ Збережено: {count} сигарет\n\n" + message_text
            
            await message.answer(message_text, reply_markup=await track_kb(language_code))
        
    except ValueError:
        await message.answer("Будь ласка, введи число:")


@router.callback_query(F.data == "back_to_progress_button")
async def back_to_progress_callback(callback: CallbackQuery, language_code: str, state: FSMContext):
    await progress_callback(callback, language_code)

    # Очищаем состояние
    await state.clear()

