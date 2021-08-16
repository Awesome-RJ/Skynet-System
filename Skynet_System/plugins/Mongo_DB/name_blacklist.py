from Skynet_System import MONGO_CLIENT

db = MONGO_CLIENT["Skynet"]["Main"]


async def update_wlc_blacklist(word, add=False):
    bl = await db.find_one({"_id": 2})
    current = bl["blacklisted_wlc"]
    upd, owo = {}, {}
    if add:
        if word in current:
            return False
        current.append(word)
    else:
        if word in current:
            current.remove(word)
        else:
            return False
    upd["blacklisted_wlc"] = current
    owo["$set"] = upd
    await db.update_one(await db.find_one({"_id": 2}), owo)
    return True


async def get_wlc_bl():
    json = await db.find_one({"_id": 2})
    return json.get("blacklisted_wlc", [])
