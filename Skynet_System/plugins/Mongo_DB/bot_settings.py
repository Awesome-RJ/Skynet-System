from Skynet_System import MONGO_CLIENT
from typing import Optional, Dict, Union

db = MONGO_CLIENT["SkynetSystemRobot"]["Main"]

async def get_chat(chat: int) -> Optional[Dict[str, Union[str, int]]]:
    settings = await db.find_one({'chat_id': chat})
    return settings

async def add_chat(chat: int) -> bool:
    exists = await db.find_one({'chat_id': chat})
    if exists:
        return False
    await db.insert_one({'chat_id': chat, 'alert': True, 'alertmode': 'warn'})
    return True

async def change_settings(chat: int, alert: bool, alertmode: str) -> bool:
    chat_data = await get_chat(chat)
    if not chat_data:
        return False
    copied_data = chat_data.copy()
    copied_data['alert'] = alert
    copied_data['alertmode'] = alertmode
    await db.replace_one(chat_data, copied_data)
    return True
