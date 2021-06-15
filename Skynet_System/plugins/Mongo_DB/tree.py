from Skynet_System import MONGO_CLIENT
from datetime import datetime
from random import choice

db = MONGO_CLIENT["skynet"]["Main"]


async def get_data() -> dict:
    data = await db.find_one({"_id": 4})
    return data


async def add_inspector(skynet: int, inspector: int) -> True:
    data = await get_data()
    data["data"][str(skynet)][str(inspector)] = []
    data["standalone"][str(inspector)] = {
        "addedby": skynet,
        "timestamp": datetime.timestamp(datetime.now()),
    }
    await db.replace_one(await get_data(), data)


async def add_enforcers(inspector: int, enforcer: int) -> True:
    data = await get_data()
    skynet = data["standalone"][str(inspector)]["addedby"]
    if skynet == 777000:
        s = data["data"][str(inspector)]
        s[list(choice(s.keys()))].append([enforcer])
    else:
        data["data"][str(skynet)][str(inspector)].append([enforcer])
    data["standalone"][str(enforcer)] = {
        "addedby": inspector,
        "timestamp": datetime.timestamp(datetime.now()),
    }
    await db.replace_one(await get_data(), data)
