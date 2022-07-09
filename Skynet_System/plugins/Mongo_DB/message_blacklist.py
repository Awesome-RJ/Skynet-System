from Skynet_System import MONGO_CLIENT

db = MONGO_CLIENT["Skynet"]["Main"]


async def get_blacklist():
    json = await db.find_one({"_id": 1})
    return json.get("blacklisted", [])


async def update_blacklist(word, add=False):
    bl = await db.find_one({"_id": 1})
    current = bl["blacklisted"]
    if add and word in current or not add and word not in current:
        return False
    elif add:
        current.append(word)
    else:
        current.remove(word)
    upd = {"blacklisted": current}
    owo = {"$set": upd}
    await db.update_one(await db.find_one({"_id": 1}), owo)
    return True
