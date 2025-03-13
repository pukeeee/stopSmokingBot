from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery, FSInputFile, BufferedInputFile
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from app.states import Setting, Plan
from app.l10n.l10n import Message as L10nMessage
from database.requests import getCigaretteCount, getCigarettePrice, setCigaretteCount, setCigarettePrice, getUser, setPlan
from app.keyboards import settings_kb, setSettings_kb, plan_kb, checkPlan_kb
from app.core.utils.create_graph import create_plan_graph
from app.core.utils.graph_message import graph_message
import matplotlib.pyplot as plt
import io


router = Router()



@router.callback_query(F.data == "plan_button")
async def plan_callback(callback: CallbackQuery, language_code: str):
    await callback.message.edit_text(L10nMessage.get_message(language_code, "plan"), reply_markup = await plan_kb(language_code))
    await callback.answer()



@router.callback_query(F.data == "start_plan_button")
async def startPlan_callback(callback: CallbackQuery, language_code: str, state: FSMContext):
    user = await getUser(callback.from_user.id)
    if user.cigarette_count == 0:
        await callback.message.edit_text("введите количество сигарет в день")
        await state.set_state(Plan.setStartCigarettes)
    
    else:
        start_cigarettes = user.cigarette_count
        await state.update_data(start_cigarettes = start_cigarettes)
        
        await state.set_state(Plan.setEndCigarettes)
        await callback.message.answer(
            text=L10nMessage.get_message(language_code, "set_plan_cigarettes")
        )
        await callback.answer()



@router.message(Plan.setStartCigarettes)
async def setStartCigarettes_handler(message: Message, state: FSMContext, language_code: str):
    await state.update_data(start_cigarettes = message.text)
    await state.set_state(Plan.setEndCigarettes)
    await message.answer(L10nMessage.get_message(language_code, "set_plan_cigarettes"))



@router.message(Plan.setEndCigarettes)
async def setPlanCigarettes_handler(message: Message, state: FSMContext, language_code: str):
    await state.update_data(end_cigarettes = message.text)
    await state.set_state(Plan.setPlanDate)
    await message.answer(L10nMessage.get_message(language_code, "set_plan_date"))



@router.message(Plan.setPlanDate)
async def setPlanDate_handler(message: Message, state: FSMContext, language_code: str):
    await state.update_data(plan_date = message.text)
    plan_data = await state.get_data()
    start_cigarettes = plan_data.get("start_cigarettes")
    end_cigarettes = plan_data.get("end_cigarettes")
    plan_date = plan_data.get("plan_date")
    
    await message.answer(L10nMessage.get_message(language_code, "check_plan").format(
                                                                                        start_cigarettes = start_cigarettes, 
                                                                                        end_cigarettes = end_cigarettes, 
                                                                                        plan_date = plan_date
                                                                                    ),
                            reply_markup = await checkPlan_kb(language_code)
                        )



@router.callback_query(F.data == "done_plan_button")
async def donePlan_callback(callback: CallbackQuery, language_code: str, state: FSMContext):
    plan_data = await state.get_data()
    start_cigarettes = int(plan_data.get("start_cigarettes"))
    end_cigarettes = int(plan_data.get("end_cigarettes"))
    plan_date = int(plan_data.get("plan_date"))
    
    plan = await createPlan(plan_date, end_cigarettes, start_cigarettes)
    
    await setPlan(callback.from_user.id, plan)
    
    message = await graph_message(callback.from_user.id, plan, start_cigarettes, language_code)
    
    
    # Сначала отправляем график отдельным сообщением
    plot_buf = await create_plan_graph(plan)
    await callback.message.answer_photo(
        photo=BufferedInputFile(
            plot_buf.getvalue(),
            filename="smoking_plan.png"
        ),
        caption = message
    )
    
    # Затем отправляем сообщение с кнопками
    await callback.message.answer(
        text="Выберите действие:",
        reply_markup=await plan_kb(language_code)
    )
    
    await callback.answer()
    await state.clear()



@router.callback_query(F.data == "back_to_plan_button")
async def backToPlan_callback(callback: CallbackQuery, language_code: str, state: FSMContext):
    await plan_callback(callback, language_code)
    await callback.answer()
    await state.clear()



async def createPlan(days: int, cigEnd: int, cigStart: int):
    """
    Создает линейный план снижения количества сигарет.
    
    :param cigStart: начальное количество сигарет в день (например, 20)
    :param cigEnd: целевое количество сигарет к концу периода (например, 0)
    :param days: общее количество дней, за которые планируется снижение (например, 30)
    :return: список запланированных значений для каждого дня (индексация от 0 до days)
    """
    
    step = (cigStart - cigEnd) / days
    plan = [round(max(cigEnd, cigStart - step * i)) for i in range(days + 1)]
    return plan