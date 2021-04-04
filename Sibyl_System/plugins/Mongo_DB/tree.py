from Sibyl_System import MONGO_CLIENT
from datetime import datetime
from random import choice

db = MONGO_CLIENT["Sibyl"]["Main"]


async def get_data() -> dict:
    data = await db.find_one({"_id": 4})
    return data


async def add_inspector(sibyl: int, inspector: int) -> True:
    data = await get_data()
    data["data"][str(sibyl)][str(inspector)] = []
    data["standalone"][str(inspector)] = {
        "addedby": sibyl,
        "timestamp": datetime.timestamp(datetime.now()),
    }
    await db.replace_one(await get_data(), data)


async def add_enforcers(inspector: int, enforcer: int) -> True:
    data = await get_data()
    sibyl = data["standalone"][str(inspector)]["addedby"]
    if sibyl == 777000:
        s = data["data"][str(inspector)]
        s[list(choice(s.keys()))].append([enforcer])
    else:
        data["data"][str(sibyl)][str(inspector)].append([enforcer])
    data["standalone"][str(enforcer)] = {
        "addedby": inspector,
        "timestamp": datetime.timestamp(datetime.now()),
    }
    await db.replace_one(await get_data(), data)
