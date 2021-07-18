# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting information about the server. """
import distro
import platform
import sys
import time
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from datetime import datetime
from os import remove
from platform import python_version, uname
from shutil import which

import psutil
from telethon import __version__, version

from userbot import ALIVE_NAME, BOT_VERSION, CMD_HELP, DB_URI, HEADER, IMG, JOKES, StartTime, bot
from userbot.events import register

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


@register(outgoing=True, pattern=r"^\.spc")
async def psu(event):
    uname = platform.uname()
    softw = "**System Information**\n"
    softw += f"`System   : {uname.system}`\n"
    softw += f"`Release  : {uname.release}`\n"
    softw += f"`Version  : {uname.version}`\n"
    softw += f"`Machine  : {uname.machine}`\n"
    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"`Boot Time: {bt.day}/{bt.month}/{bt.year}  {bt.hour}:{bt.minute}:{bt.second}`\n"
    # CPU Cores
    cpuu = "**CPU Info**\n"
    cpuu += "`Physical cores   : " + \
        str(psutil.cpu_count(logical=False)) + "`\n"
    cpuu += "`Total cores      : " + \
        str(psutil.cpu_count(logical=True)) + "`\n"
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    cpuu += f"`Max Frequency    : {cpufreq.max:.2f}Mhz`\n"
    cpuu += f"`Min Frequency    : {cpufreq.min:.2f}Mhz`\n"
    cpuu += f"`Current Frequency: {cpufreq.current:.2f}Mhz`\n\n"
    # CPU usage
    cpuu += "**CPU Usage Per Core**\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpuu += f"`Core {i}  : {percentage}%`\n"
    cpuu += "**Total CPU Usage**\n"
    cpuu += f"`All Core: {psutil.cpu_percent()}%`\n"
    # Disk Usage
    partitions = psutil.disk_partitions()
    for partition in partitions:
        device = {partition.device}
        mountpoint = {partition.mountpoint}
        fstype = {partition.fstype}
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
    disk = "**Disk Usage**\n"
    disk += f"`Device    : {device}`\n"
    disk += f"`Mountpoint: {mountpoint}`\n"
    disk += f"`FS Type   : {fstype}`\n"
    disk += f"`Total Size: {get_size(partition_usage.total)}`\n"
    disk += f"`Used      : {get_size(partition_usage.used)}`\n"
    disk += f"`Free      : {get_size(partition_usage.free)}`\n"
    disk += f"`Percentage: {partition_usage.percent}%`\n"
    # RAM Usage
    svmem = psutil.virtual_memory()
    memm = "**Memory Usage**\n"
    memm += f"`Total     : {get_size(svmem.total)}`\n"
    memm += f"`Available : {get_size(svmem.available)}`\n"
    memm += f"`Used      : {get_size(svmem.used)}`\n"
    memm += f"`Percentage: {svmem.percent}%`\n"
    # Bandwidth Usage
    bw = "**Bandwith Usage**\n"
    bw += f"`Upload  : {get_size(psutil.net_io_counters().bytes_sent)}`\n"
    bw += f"`Download: {get_size(psutil.net_io_counters().bytes_recv)}`\n"
    # Help Strings
    help_string = f"{str(softw)}\n"
    help_string += f"{str(cpuu)}\n"
    help_string += f"{str(disk)}\n"
    help_string += f"{str(memm)}\n"
    help_string += f"{str(bw)}\n"
    help_string += "**Engine Info**\n"
    help_string += f"`Python {sys.version}`\n"
    help_string += f"`Telethon {__version__}`"
    await event.edit(help_string)


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def check_data_base_heal_th():
    is_database_working = False
    output = "Failing"

    if not DB_URI:
        return is_database_working, output

    from userbot.modules.sql_helper import SESSION

    try:
        SESSION.execute("SELECT 1")
    except Exception as e:
        output = f"Failing {str(e)}"
        is_database_working = False
    else:
        output = "Connected"
        is_database_working = True

    return is_database_working, output


@register(outgoing=True, pattern=r"^\.sysd$")
async def sysdetails(sysd):
    """ For .sysd command, get system info using neofetch. """
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            fetch = await asyncrunapp(
                "neofetch", "--stdout", stdout=asyncPIPE, stderr=asyncPIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) + \
                str(stderr.decode().strip())

            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("`Install neofetch first !!`")


@register(outgoing=True, pattern=r"^\.botver$")
async def bot_ver(event):
    """ For .botver command, get the bot version. """
    if event.text[0].isalpha() or event.text[0] in ("/", "#", "@", "!"):
        return
    if which("git") is not None:
        ver = await asyncrunapp(
            "git", "describe", "--all", "--long", stdout=asyncPIPE, stderr=asyncPIPE,
        )
        stdout, stderr = await ver.communicate()
        verout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        rev = await asyncrunapp(
            "git", "rev-list", "--all", "--count", stdout=asyncPIPE, stderr=asyncPIPE,
        )
        stdout, stderr = await rev.communicate()
        revout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        await event.edit(
            "`Userbot Version: " f"{verout}" "` \n" "`Revision: " f"{revout}" "`"
        )
    else:
        await event.edit(
            "Shame that you don't have git, you're running - 'v1.beta.4' anyway!"
        )


@register(outgoing=True, pattern=r"^\.pip(?: |$)(.*)")
async def pipcheck(pip):
    """ For .pip command, do a pip search. """
    if pip.text[0].isalpha() or pip.text[0] in ("/", "#", "@", "!"):
        return
    pipmodule = pip.pattern_match.group(1)
    if pipmodule:
        await pip.edit("`Searching . . .`")
        pipc = await asyncrunapp(
            "pip3", "search", pipmodule, stdout=asyncPIPE, stderr=asyncPIPE,
        )

        stdout, stderr = await pipc.communicate()
        pipout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        if pipout:
            if len(pipout) > 4096:
                await pip.edit("`Output too large, sending as file`")
                file = open("output.txt", "w+")
                file.write(pipout)
                file.close()
                await pip.client.send_file(
                    pip.chat_id, "output.txt", reply_to=pip.id,
                )
                remove("output.txt")
                return
            await pip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`"
                f"{pipout}"
                "`"
            )
        else:
            await pip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`No Result Returned/False`"
            )
    else:
        await pip.edit("`Use .help pip to see an example`")


@register(outgoing=True, pattern=r"^\.(?:alive|on)\s?(.)?")
async def amireallyalive(alive):
    """ For .on command, check if the bot is running.  """
    uptime = await get_readable_time((time.time() - StartTime))
    img = IMG
    jk = await asyncrunapp(
        "pyjoke", "-c", "all", stdout=asyncPIPE, stderr=asyncPIPE,
    )

    stdout, stderr = await jk.communicate()
    jokes = str(stdout.decode().strip())
    db = check_data_base_heal_th()
    os = distro.linux_distribution(
        full_distribution_name=False)[0].capitalize()
    ver = distro.linux_distribution(full_distribution_name=False)[1]
    caption = (
        "`"
        f"{HEADER}\n\n"
        f"👤 User             : {DEFAULTUSER}\n\n"
        f"🤖 Bot Version      : {BOT_VERSION}\n\n"
        f"🖥 Run On           : {os} Version {ver}\n\n"
        f"🐍 Python Version   : {python_version()}\n\n"
        f"💻 Telethon Version : {version.__version__}\n\n"
        f"🕒 Bot Uptime       : {uptime}\n\n"
        f"💾 Database Status  : {db}\n"
        "`"
    )
    if IMG:
        try:
            img = IMG
            if JOKES:
                await bot.send_file(alive.chat_id, img, caption=caption + f"\n\n**{jokes}**")
            else:
                await bot.send_file(alive.chat_id, img, caption=caption)
            await alive.delete()
        except BaseException:
            await alive.edit(
                caption + "\n\n *`The provided logo is invalid."
                "\nMake sure the link is directed to the logo picture`"
            )
    else:
        await alive.edit(caption)


@register(outgoing=True, pattern=r"^\.aliveu")
async def amireallyaliveuser(username):
    """ For .aliveu command, change the username in the .alive command. """
    message = username.text
    output = ".aliveu [new user without brackets] nor can it be empty"
    if message != ".aliveu" and message[7:8] == " ":
        newuser = message[8:]
        global DEFAULTUSER
        DEFAULTUSER = newuser
        output = "Successfully changed user to " + newuser + "!"
    await username.edit("`" f"{output}" "`")


@register(outgoing=True, pattern=r"^\.resetalive$")
async def amireallyalivereset(ureset):
    """ For .resetalive command, reset the username in the .alive command. """
    global DEFAULTUSER
    DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
    await ureset.edit("`" "Successfully reset user for alive!" "`")


CMD_HELP.update({"sysd": ">`.sysd`"
                 "\nUsage: Shows system information using neofetch.\n\n"
                 ">`.spc`"
                 "\nUsage: Show system specification.",
                 "botver": ">`.botver`"
                 "\nUsage: Shows the userbot version.",
                 "pip": ">`.pip <module(s)>`"
                 "\nUsage: Does a search of pip modules(s).",
                 "alive": ">`.alive`"
                 "\nUsage: Type .alive to see wether your bot is working or not."
                 "\n\n>`.aliveu <text>`"
                 "\nUsage: Changes the 'user' in alive to the text you want."
                 "\n\n>`.resetalive`"
                 "\nUsage: Resets the user to default.",
                 })
