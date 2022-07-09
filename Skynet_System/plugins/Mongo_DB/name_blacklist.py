from Skynet_System import MONGO_CLIENT

db = MONGO_CLIENT["Skynet"]["Main"]


async def update_wlc_blacklist(word, add=False):
    bl = await db.find_one({"_id": 2})
    current = bl["blacklisted_wlc"]
    upd, owo = {}, {}
    if add and word in current or not add and word not in current:
        return False
    elif add:
        current.append(word)
    else:
        current.remove(word)
    upd["blacklisted_wlc"] = current
    owo["$set"] = upd
    await db.update_one(await db.find_one({"_id": 2}), owo)
    return True


async def get_wlc_bl():
    json = await db.find_one({"_id": 2})
    return json.get("blacklisted_wlc", [])
