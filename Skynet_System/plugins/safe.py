from Skynet_System import System, system_cmd
import os
import sys
import subprocess
import asyncio


@System.on(system_cmd(pattern=r"Skynet gitpull"))
async def gitpull(event):
    await event.reply("Starting git pull...")
    process = await asyncio.create_subprocess_shell(
        "git pull", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    out = stdout.decode() or ""
    err = stderr.decode() or ""
    
    reply_msg = "**Git Pull Output:**\n"
    if out:
        reply_msg += f"`{out}`\n"
    if err:
        reply_msg += f"**Errors:**\n`{err}`\n"
    
    await event.reply(reply_msg + "\nRestarting service...")
    os.system("restart.bat")
    sys.exit()


@System.on(system_cmd(pattern=r"Skynet restart"))
async def reboot(event):
    if event.fwd_from:
        return
    await event.reply("Restarting.....")
    await System.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
    sys.exit()


@System.on(system_cmd(pattern=r"Skynet shutdown"))
async def shutdown(event):
    if event.fwd_from:
        return
    await event.reply("Shutting Down... ")
    await System.disconnect()
