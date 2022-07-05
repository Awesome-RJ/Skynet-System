import re

from Skynet_System import Skynet_logs, ENFORCERS, Skynet, INSPECTORS
from Skynet_System.strings import (
    scan_request_string,
    reject_string,
    proof_string,
    forced_scan_string,
)
from Skynet_System import System, system_cmd
from Skynet_System.utils import seprate_flags, Flag


url_regex = re.compile("(http(s)?://)?t.me/(c/)?(\w+)/(\d+)")


def get_data_from_url(url: str) -> tuple:
    """
    >>> get_data_from_url("https://t.me/c/1476401326/36963")
    (1476401326, 36963)
    """

    match = url_regex.match(url)
    if not match:
        return False
    return (match.group(4), match.group(5))


@System.command(
    e=system_cmd(pattern=r"scan ", allow_enforcer=True),
    group="main",
    help="Reply to a message WITH reason to send a request to Inspect",
    flags=[
        Flag(
            "-f",
            "Force approve a scan. Using this with scan will auto approve it",
            "store_true"
        ),
        Flag(
            "-u",
            "Grab message from url. Use this with message link to scan the user the message link redirects to.",
        ),
        Flag(
            "-o",
            "Original Sender. Using this will gban orignal sender instead of forwarder.",
            "store_true",
        ),
        Flag(
            "-r",
            "Reason to scan message with.",
            nargs="*",
            default=None
        )
    ],
    allow_unknown=True
)
async def scan(event, flags):
    replied = await event.get_reply_message()
    if flags.r:
        reason = " ".join(flags.r)
    else:
        split = event.text.split(' ', 1)
        if len(split) == 1:
            return
        reason = seprate_flags(split[1]).strip()
        if not reason:
            return
    if flags.u:
        url = flags.u
        data = get_data_from_url(url)
        if not data:
            await event.reply("Invalid url")
            return
        try:
            message = await System.get_messages(
                int(data[0]) if data[0].isnumeric() else data[0], ids=int(data[1])
            )
        except:
            await event.reply("Failed to get data from url")
            return
        executor = await event.get_sender()
        executor = f"[{executor.first_name}](tg://user?id={executor.id})"
        if not message:
            await event.reply("Failed to get data from url")
            return
        if message.from_id.user_id in ENFORCERS:
            return
        msg = await System.send_message(
            Skynet_logs,
            scan_request_string.format(
                enforcer=executor,
                spammer=message.from_id.user_id,
                chat=f"https://t.me/{data[0]}/{data[1]}",
                message=message.text,
                reason=reason,
            ),
        )
        return
    if not event.is_reply:
        return
    if flags.o:
        if replied.fwd_from:
            reply = replied.fwd_from
            target = reply.from_id.user_id
            if reply.from_id.user_id in ENFORCERS or reply.from_id.user_id in Skynet:
                return
            if not reply.from_id.user_id:
                await event.reply("Cannot get user ID.")
                return
            if reply.from_name:
                sender = f"[{reply.from_name}](tg://user?id={reply.from_id.user_id})"
            else:
                sender = (
                    f"[{reply.from_id.user_id}](tg://user?id={reply.from_id.user_id})"
                )
    else:
        if replied.sender.id in ENFORCERS:
            return
        sender = f"[{replied.sender.first_name}](tg://user?id={replied.sender.id})"
        target = replied.sender.id
    executer = await event.get_sender()
    req_proof = req_user = False
    approve = bool(flags.f and executer.id in INSPECTORS)
    if replied.media:
        await replied.forward_to(Skynet_logs)
    executor = f"[{executer.first_name}](tg://user?id={executer.id})"
    chat = (
        f"t.me/{event.chat.username}/{event.message.id}"
        if event.chat.username
        else f"t.me/c/{event.chat.id}/{event.message.id}"
    )
    await event.reply("Connecting to Sylviorus for a cymatic scan.")
    if req_proof and req_user:
        await replied.forward_to(Skynet_logs)
        await System.gban(
            executer.id, req_user, reason, msg.id, executer, message=replied.text
        )
    if not approve:
        msg = await System.send_message(
            Skynet_logs,
            scan_request_string.format(
                enforcer=executor,
                spammer=sender,
                chat=chat,
                message=replied.text,
                reason=reason,
            ),
        )
        return
    msg = await System.send_message(
        Skynet_logs,
        forced_scan_string.format(
            ins=executor, spammer=sender, chat=chat, message=replied.text, reason=reason
        ),
    )
    await System.gban(
        executer.id, target, reason, msg.id, executer, message=replied.text
    )

@System.on(system_cmd(pattern=r"re(vive|vert|store) ", allow_inspectors=True))
async def revive(event):
    try:
        user_id = event.text.split(" ", 1)[1]
    except IndexError:
        return
    a = await event.reply("Reverting bans..")
    if not user_id.isnumeric():
        await a.edit("Invalid id")
        return
    if not (
        await System.ungban(int(user_id), f" By //{(await event.get_sender()).id}")
    ):
        await a.edit("User is not gbanned.")
        return
    await a.edit("Revert request sent to Sylviorus. This might take 10minutes or so.")


@System.on(system_cmd(pattern=r"Skynet logs"))
async def logs(event):
    await System.send_file(event.chat_id, "log.txt")

@System.command(
    e = system_cmd(pattern=r"approve", allow_inspectors=True, force_reply=True),
    group="main",
    help="Approve a scan request.",
    flags=[Flag("-or", "Overwrite reason", nargs="*")]
)
async def approve(event, flags):
    replied = await event.get_reply_message()
    match = re.match(r"\$SCAN", replied.text)
    auto_match = re.search(r"\$AUTO(SCAN)?", replied.text)
    me = await System.get_me()
    if auto_match and replied.sender.id == me.id:
        id = re.search(
            r"\*\*Scanned user:\*\* (\[\w+\]\(tg://user\?id=(\d+)\)|(\d+))",
            replied.text,
        )[2]

        try:
            message = re.search(
                "(\*\*)?Message:(\*\*)? (.*)", replied.text, re.DOTALL
            )[3]

        except:
            message = None
        try:
            bot = (await System.get_entity(id)).bot
        except:
            bot = False
        reason = re.search("\*\*Reason:\*\* (.*)", replied.text)[1]
        await System.gban(
            enforcer=me.id,
            target=id,
            reason=reason,
            msg_id=replied.id,
            auto=True,
            bot=bot,
            message=message,
        )
        return
    overwritten = False
    if match:
        reply = replied.sender.id
        sender = await event.get_sender()
        # checks to not gban the Gbanner and find who is who
        if reply == me.id:
            list = re.findall(r"tg://user\?id=(\d+)", replied.text)
            if getattr(flags, "or", None):
                reason = " ".join(getattr(flags, "or"))
                await replied.edit(
                    re.sub(
                        "(\*\*)?(Scan)? ?Reason:(\*\*)? (`([^`]*)`|.*)",
                        f'**Scan Reason:** `{reason}`',
                        replied.text,
                    )
                )
                overwritten = True
            else:
                reason = re.search(
                    r"(\*\*)?(Scan)? ?Reason:(\*\*)? (`([^`]*)`|.*)", replied.text
                )
                reason = reason[5] or reason[4]
            id1 = list[0]
            id2 = list[1] if len(list) > 1 else re.findall(r"(\d+)", replied.text)[1]
            if id1 in ENFORCERS or Skynet:
                enforcer = id1
                scam = id2
            else:
                enforcer = id2
                scam = id1
            try:
                bot = (await System.get_entity(scam)).bot
            except:
                bot = False
            try:
                message = re.search(
                    "(\*\*)?Target Message:(\*\*)? (.*)",
                    replied.text,
                    re.DOTALL,
                )[3]

            except:
                message = None
            await System.gban(
                enforcer, scam, reason, replied.id, sender, bot=bot, message=message
            )
            if orig := re.search(r"t.me/(\w+)/(\d+)", replied.text):
                try:
                    if overwritten:
                        await System.send_message(
                            orig[1],
                            f"User is a target for enforcement action.\nEnforcement Mode: Lethal Eliminator\nYour reason was overwritten with: `{reason}`",
                            reply_to=int(orig[2]),
                        )

                        return
                    await System.send_message(
                        orig[1],
                        "User is a target for enforcement action.\nEnforcement Mode: Lethal Eliminator",
                        reply_to=int(orig[2]),
                    )

                except:
                    await event.reply('Failed to notify enforcer about scan being accepted.')


@System.on(system_cmd(pattern=r"reject", allow_inspectors=True, force_reply=True))
async def reject(event):
    # print('Trying OmO')
    replied = await event.get_reply_message()
    me = await System.get_me()
    if replied.from_id.user_id == me.id:
        if match := re.match(r"\$(SCAN|AUTO(SCAN)?)", replied.text):
            # print('Matched OmU')
            id = replied.id
            await System.edit_message(Skynet_logs, id, reject_string)
    orig = re.search(r"t.me/(\w+)/(\d+)", replied.text)
    _orig = re.search(r"t.me/c/(\w+)/(\d+)", replied.text)
    flags, reason = seprate_flags(event.text)
    if _orig and "r" in flags.keys():
        await System.send_message(
            int(_orig[1]),
            f'Crime coefficient less than 100\nUser is not a target for enforcement action\nTrigger of dominator will be locked.\nReason: **{reason.split(" ", 1)[1].strip()}**',
            reply_to=int(_orig[2]),
        )

        return
    if orig and "r" in flags.keys():
        await System.send_message(
            orig[1],
            f'Crime coefficient less than 100\nUser is not a target for enforcement action\nTrigger of dominator will be locked.\nReason: **{reason.split(" ", 1)[1].strip()}**',
            reply_to=int(orig[2]),
        )


help_plus = """
Here is the help for **Main**:
Commands:
    `scan` - Reply to a message WITH reason to send a request to Inspectors/Skynet for judgement
    `approve` - Approve a scan request (Only works in Skynet System Base)
    `revert` or `revive` or `restore` - Ungban ID
    `qproof` - Get quick proof from database for given user id
    `proof` - Get message from proof id which is at the end of gban msg
    `reject` - Reject a scan request
Flags:
    scan:
        `-f` - Force approve a scan. Using this with scan will auto approve it (Inspectors+)
        `-u` - Grab message from url. Use this with message link to scan the user the message link redirects to. (Enforcers+)
        `-o` - Original Sender. Using this will gban orignal sender instead of forwarder (Enforcers+)
    approve:
        `-or` - Overwrite reason. Use this to change scan reason.
    reject:
        `-r` - Reply to the scan message with reject reason.
All commands can be used with ! or / or ? or .
"""

__plugin_name__ = "Main"
