from telethon.tl.functions.users import GetFullUserRequest
from Skynet_System import System, system_cmd


@System.on(system_cmd(pattern=r"whois"))
async def whois(event):
    try:
        to_get = event.pattern_match.group(1)
    except Exception:
        if not event.reply:
            return
        replied = await event.get_reply_message()
        to_get = int(replied.sender.id)
    try:
        to_get = to_get
    except Exception:
        pass
    try:
        data = await System(GetFullUserRequest(to_get))
    except Exception:
        await event.reply("Failed to get data of the user")
        return
    await System.send_message(
        event.chat_id,
        f"╒═══「 Appraisal results: 」\n❂ First Name: `{data.user.last_name}`\n❂ Last Name: `{data.user.first_name}`\n❂ Username: @{data.user.username}\n❂ Userlink: [{data.user.first_name}](tg://user?id={data.user.id})\n❂ User ID: `{data.user.id}`\n❂ About: {data.about}",
    )


help_plus = """ Here is Help for **Whois** -
`whois` - get data of the user
**Notes:**
`/` `?` `.` `!` are supported prefixes.
**Example:** `/addenf` or `?addenf` or `.addenf`
"""
__plugin_name__ = "whois"
