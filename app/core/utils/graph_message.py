from database.requests import getUser
from app.l10n.l10n import Message as L10nMessage


async def graph_message(tgId: int, plan: list, start_cigarettes: int, language_code: str):
    user = await getUser(tgId)
    
    if user.cigarette_price != 0:
        counter = 0
        
        for i in range(len(plan)):
            counter += start_cigarettes - plan[i]
        
        plan = len(plan)
        earn = round((counter / 20) * user.cigarette_price, 2)
        month_earn = round((user.cigarette_count / 20) * user.cigarette_price * 30, 2)
        
        message = L10nMessage.get_message(language_code, "graph_message").format(
            plan_days = plan, counter = counter, earn = earn, month_earn = month_earn
        )

    else:
        message = f"Щоб порахувати скільки ти заощадиш, вкажи ціну сигарет в налаштуваннях"
        
    return message
