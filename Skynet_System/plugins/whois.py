from telethon.tl.functions.users import GetFullUserRequest
from Skynet_System import System, system_cmd


@System.on(system_cmd(pattern=r"whois"))
async def whois(event):
    to_get = None
    parts = event.text.split(" ", 1)
    if len(parts) > 1:
        to_get = parts[1].strip()
        # If it's a numeric ID, convert to int
        if to_get.isdigit():
            to_get = int(to_get)
        elif to_get.startswith("-") and to_get[1:].isdigit():
            to_get = int(to_get)
    else:
        if event.is_reply:
            replied = await event.get_reply_message()
            if replied and replied.sender_id:
                to_get = replied.sender_id
        else:
            to_get = event.sender_id

    if not to_get:
        await event.reply("Please reply to a user or specify a user ID / username.")
        return

    try:
        data = await System(GetFullUserRequest(to_get))
    except Exception as e:
        await event.reply(f"Failed to get data of the user: {e}")
        return

    first_name = data.user.first_name or ""
    last_name = data.user.last_name or ""
    username = f"@{data.user.username}" if data.user.username else "None"
    about = data.about or "None"

    await System.send_message(
        event.chat_id,
        f"╒═══「 Appraisal results: 」\n❂ First Name: `{first_name}`\n❂ Last Name: `{last_name}`\n❂ Username: {username}\n❂ Userlink: [{first_name}](tg://user?id={data.user.id})\n❂ User ID: `{data.user.id}`\n❂ About: {about}",
    )


help_plus = """ Here is Help for **Whois** -
`whois` - get data of the user
**Notes:**
`/` `?` `.` `!` are supported prefixes.
**Example:** `/addenf` or `?addenf` or `.addenf`
"""
__plugin_name__ = "whois"
