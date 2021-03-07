from telethon.sync import TelegramClient
from telethon.sessions import StringSession

print("""==============================
String Session Generator

You are about to generate an string sessions that works

If you don't have both API ID and hash for Telegram, please get one from https://my.telegram.org.
==============================
""")

APP_ID = int(input("[PROMPT] Enter your APP ID here: "))
API_HASH = input("[PROMPT] Enter your API HASH here: ")

# Copied from https://github.com/SpEcHiDe/UniBorg/blob/master/GenerateStringSession.py#L19
with TelegramClient(StringSession(), APP_ID, API_HASH) as client:
    session_string = client.session.save()
    saved_messages_template = """Here's your <code>STRING_SESSION</code>: <code>{}</code>

⚠️ <i>It is forbidden to pass it to third-parties.</i>""".format(session_string)
    client.send_message("me", saved_messages_template, parse_mode="html")
    print("[INFO] Check your target account's saved messages for the string session. Keep it safe!")
