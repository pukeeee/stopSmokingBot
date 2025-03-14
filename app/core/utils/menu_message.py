from app.l10n.l10n import Message as L10nMessage
from database.requests import getUser



async def mainMenu(tg_id: int, language_code: str):
    user = await getUser(tg_id)
    if user.cigarette_count != 0 and user.cigarette_price != 0:
        
        text = L10nMessage.get_message(language_code, "menu").format(
            price = user.cigarette_price,
            count = user.cigarette_count,
            price_7 = (user.cigarette_count * 7) / 20 * user.cigarette_price,
            count_7 = user.cigarette_count * 7,
            price_30 = (user.cigarette_count * 30) / 20 * user.cigarette_price,
            count_30 = user.cigarette_count * 30
        )
    else:
        text = L10nMessage.get_message(language_code, "welcome")

    return text