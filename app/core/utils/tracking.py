from datetime import datetime, timedelta
from database.requests import getUser




weekday_dict = {
    'monday': 'понеділок',
    'tuesday': 'вівторок',
    'wednesday': 'середа',
    'thursday': 'четвер',
    'friday': "п'ятниця",
    'saturday': 'субота',
    'sunday': 'неділя'
}



async def get_formatted_date(date: datetime) -> tuple[str, str]:
    """Возвращает отформатированную дату и день недели на украинском"""
    weekday = date.strftime('%A').lower()
    weekday_ua = weekday_dict.get(weekday, weekday)
    formatted_date = date.strftime("%d.%m")
    return weekday_ua, formatted_date



async def format_tracking_message(day_number: int, date: datetime, count: int = None, is_input_required: bool = False) -> str:
    """Формирует сообщение для трекинга"""
    weekday_ua, formatted_date = await get_formatted_date(date)
    
    message = f"День {day_number + 1}\n📅 {weekday_ua}, {formatted_date}\n\n"
    
    if is_input_required:
        message += "Введи кількість викурених сигарет за цей день:"
    else:
        if count is not None:
            message += f"Кількість сигарет: {count}\n\n"
            message += "Якщо хочеш змінити кількість - просто введи нове значення"
    
    return message

async def get_tracking_date(user_id: int, tracking_day: int) -> datetime:
    """Возвращает дату для указанного дня трекинга"""
    user = await getUser(user_id)
    start_date = datetime.fromtimestamp(user.plan_date)
    return start_date.date() + timedelta(days=tracking_day)