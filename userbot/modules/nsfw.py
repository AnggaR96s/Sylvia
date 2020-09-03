# Credits to https://t.me/TheHardGamer
# Edited by @AnggaR96s
import asyncio
import json
import os
import random
import urllib
from asyncio import sleep
from urllib.parse import quote as urlencode

import aiohttp
import nekos
import requests
from jikanpy import Jikan

from userbot import CMD_HELP, bot
from userbot.events import register

_pats = []
jikan = Jikan()


@register(outgoing=True, pattern=r"^\.boobs(?: |$)(.*)")
async def boobs(e):
    await e.edit("`Finding some big boobs...`")
    await sleep(3)
    await e.edit("`Sending some big boobs...`")
    nsfw = requests.get("http://api.oboobs.ru/noise/1").json()[0]["preview"]
    urllib.request.urlretrieve(
        "http://media.oboobs.ru/{}".format(nsfw), "*.jpg")
    os.rename("*.jpg", "boobs.jpg")
    await bot.send_file(e.chat_id, "boobs.jpg")
    os.remove("boobs.jpg")
    await e.delete()


@register(outgoing=True, pattern=r"^\.butts(?: |$)(.*)")
async def butts(e):
    await e.edit("`Finding some beautiful butts...`")
    await sleep(3)
    await e.edit("`Sending some beautiful butts...`")
    nsfw = requests.get("http://api.obutts.ru/noise/1").json()[0]["preview"]
    urllib.request.urlretrieve(
        "http://media.obutts.ru/{}".format(nsfw), "*.jpg")
    os.rename("*.jpg", "butts.jpg")
    await bot.send_file(e.chat_id, "butts.jpg")
    os.remove("butts.jpg")
    await e.delete()


@register(outgoing=True, pattern=r"^.pat(?: |$)")
async def pat(e):
    global _pats

    url = "https://headp.at/js/pats.json"
    if not _pats:
        async with aiohttp.ClientSession() as session:
            async with session.post(url) as raw_resp:
                resp = await raw_resp.text()
        _pats = json.loads(resp)
    pats = _pats

    pats = [i for i in pats if os.path.splitext(i)[1] == ".gif"]

    pat = random.choice(pats)
    link = f"https://headp.at/pats/{urlencode(pat)}"

    await asyncio.wait([e.respond(file=link, reply_to=e.reply_to_msg_id), e.delete()])


@register(outgoing=True, pattern=r"^\.pgif(?: |$)(.*)")
async def pussyg(e):
    await e.edit("`Finding some pussy gifs...`")
    await sleep(2)
    target = "pussy"
    await bot.send_file(e.chat_id, nekos.img(target), reply_to=e.reply_to_msg_id)
    await e.delete()


@register(outgoing=True, pattern=r"^\.pjpg(?: |$)(.*)")
async def pussyp(e):
    await e.edit("`Finding some pussy pics...`")
    await sleep(2)
    target = "pussy_jpg"
    await bot.send_file(e.chat_id, nekos.img(target), reply_to=e.reply_to_msg_id)
    await e.delete()


@register(outgoing=True, pattern=r"^\.cum(?: |$)(.*)")
async def cum(e):
    await e.edit("`Finding some cum gifs...`")
    await sleep(2)
    target = "cum"
    await bot.send_file(e.chat_id, nekos.img(target), reply_to=e.reply_to_msg_id)
    await e.delete()


CMD_HELP.update(
    {
        "nsfw": ">`.boobs`"
        "\nUsage: Get boobs image.\n"
        ">`.butts`"
        "\nUsage: Get butts image.\n"
        ">`.pgif`"
        "\nUsage: Get pussy gif.\n"
        ">`.pjpg`"
        "\nUsage: Get pussy image.\n"
        ">`.pat`"
        "\nUsage: Get random pat gif.\n"
        ">`.cum`"
        "\nUsage: Get random cum gif."
    }
)
