from Sibyl_System import MONGO_CLIENT
from datetime import datetime
from random import choice

db = MONGO_CLIENT["Sibyl"]["Main"]


async def get_data() -> dict:
    data = await db.find_one({"_id": 4})
    return data


async def add_developer(cardinal: int, developer: int) -> True:
    data = await get_data()
    data["data"][str(cardinal)][str(developer)] = []
    data["standalone"][str(developer)] = {
        "addedby": cardinal,
        "timestamp": datetime.timestamp(datetime.now()),
    }
    await db.replace_one(await get_data(), data)


async def add_manager(developer: int, manager: int) -> True:
    data = await get_data()
    cardinal = data["standalone"][str(developer)]["addedby"]
    if sibyl == 777000:
        s = data["data"][str(developer)]
        s[list(choice(s.keys()))].append([manager])
    else:
        data["data"][str(cardinal)][str(developer)].append([manager])
    data["standalone"][str(manager)] = {
        "addedby": developer,
        "timestamp": datetime.timestamp(datetime.now()),
    }
    await db.replace_one(await get_data(), data)
