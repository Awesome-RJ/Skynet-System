"""Gets ENV vars or Config vars then calls class."""

import traceback
import logging
import os
import re
import aiohttp
import json

from telethon import events
from telethon.sessions import StringSession
from motor import motor_asyncio
from datetime import datetime



logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

ENV = bool(os.environ.get("ENV", False))
if ENV:
    API_ID_KEY = int(os.environ.get("API_ID_KEY"))
    API_HASH_KEY = os.environ.get("API_HASH_KEY")
    STRING_SESSION = os.environ.get("STRING_SESSION")
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY")
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    RAW_Skynet = os.environ.get("Skynet", "")
    RAW_ENFORCERS = os.environ.get("ENFORCERS", "")
    Skynet = [int(x) for x in os.environ.get("Skynet", "").split()]
    INSPECTORS = [int(x) for x in os.environ.get("INSPECTORS", "").split()]
    ENFORCERS = [int(x) for x in os.environ.get("ENFORCERS", "").split()]
    MONGO_DB_URL = os.environ.get("MONGO_DB_URL")
    Skynet_logs = int(os.environ.get("Skynet_logs"))
    Skynet_approved_logs = int(os.environ.get("Skynet_approved_logs"))
    GBAN_MSG_LOGS = int(os.environ.get("GBAN_MSG_LOGS"))
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
else:
    import Skynet_System.config as Config

    API_ID_KEY = Config.API_ID
    API_HASH_KEY = Config.API_HASH
    STRING_SESSION = Config.STRING_SESSION
    MONGO_DB_URL = Config.MONGO_DB_URL
    with open(os.path.join(os.getcwd(), "Skynet_System/elevated_users.json"), "r") as f:
        data = json.load(f)
    Skynet = data["Skynet"]
    ENFORCERS = data["ENFORCERS"]
    INSPECTORS = data["INSPECTORS"]
    Skynet_logs = Config.Skynet_logs
    Skynet_approved_logs = Config.Skynet_approved_logs
    GBAN_MSG_LOGS = Config.GBAN_MSG_LOGS
    BOT_TOKEN = Config.BOT_TOKEN

INSPECTORS.extend(Skynet)
ENFORCERS.extend(INSPECTORS)

session = aiohttp.ClientSession()

MONGO_CLIENT = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)

from .client_class import SkynetClient

#try:
System = SkynetClient(StringSession(STRING_SESSION), API_ID_KEY, API_HASH_KEY)
#except:
 #   print(traceback.format_exc())
  #  exit(1)

collection = MONGO_CLIENT["Skynet"]["Main"]


async def make_collections() -> str:
    if (
        await collection.count_documents({"_id": 1}, limit=1) == 0
    ):  # Blacklisted words list
        dictw = {"_id": 1, "blacklisted": []}
        await collection.insert_one(dictw)

    if (
        await collection.count_documents({"_id": 2}, limit=1) == 0
    ):  # Blacklisted words in name list
        dictw = {"_id": 2, "Type": "Wlc Blacklist", "blacklisted_wlc": []}
        await collection.insert_one(dictw)
    if await collection.count_documents({"_id": 3}, limit=1) == 0:  # Gbanned users list
        dictw = {
            "_id": 3,
            "Type": "Gban:List",
            "victim": [],
            "gbanners": [],
            "reason": [],
            "proof_id": [],
        }

        await collection.insert_one(dictw)
    if await collection.count_documents({"_id": 4}, limit=1) == 0:  # Rank tree list
        sample_dict = {"_id": 4, "standalone": {}, "data": {}}
        for x in Skynet:
            sample_dict["data"][str(x)] = {}
            sample_dict["standalone"][str(x)] = {
                "added_by": 777000,
                "timestamp": datetime.timestamp(datetime.now()),
            }
        await collection.insert_one(sample_dict)
    return ""


def system_cmd(
    pattern=None,
    allow_Skynet=True,
    allow_enforcer=False,
    allow_inspectors=False,
    allow_slash=True,
    force_reply=False,
    **args
):
    if pattern and allow_slash:
#        args["pattern"] = re.compile(r"[\?\.!/](" + pattern + r")(?!@)")
        args["pattern"] = re.compile(r"[\?\.!/]" + pattern)
    else:
        args["pattern"] = re.compile(r"[\?\.!]" + pattern)
    if allow_Skynet and allow_enforcer:
        args["from_users"] = ENFORCERS
    elif allow_inspectors and allow_Skynet:
        args["from_users"] = INSPECTORS
    else:
        args["from_users"] = Skynet
    if force_reply:
        args["func"] = lambda e: e.is_reply
    return events.NewMessage(**args)
