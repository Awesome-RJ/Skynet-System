from Skynet_System import MONGO_CLIENT

db = MONGO_CLIENT["Skynet"]["Main"]


async def get_blacklist():
    json = await db.find_one({"_id": 1})
    return json.get("blacklisted", [])


async def update_blacklist(word, add=False):
    # cant find better names
    upd = {}
    owo = {}
    bl = await db.find_one({"_id": 1})
    current = bl["blacklisted"]
    if add:
        if word in current:
            return False
        current.append(word)
    else:
        if word in current:
            current.remove(word)
        else:
            return False
    upd["blacklisted"] = current
    owo["$set"] = upd
    await db.update_one(await db.find_one({"_id": 1}), owo)
    return True
