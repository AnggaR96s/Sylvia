#   Credits to @mrconfused and @sandy1709
#    Copyright (C) 2020  sandeep.n(π.$)
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import re

import requests
from PIL import Image
from telegraph import exceptions, upload_file

# from . import *
from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import register
from validators.url import url


@register(outgoing=True, pattern=r"^\.threats(?: |$)(.*)")
async def dclxvi(event):
    replied = await event.get_reply_message()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await event.edit("reply to a supported media file")
        return
    if replied.media:
        await event.edit("passing to telegraph...")
    else:
        await event.edit("reply to a supported media file")
        return
    download_location = await bot.download_media(replied, TEMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await event.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
            os.remove(download_location)
            return
        await event.edit("generating image..")
    else:
        await event.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await event.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    gpx = f"https://telegra.ph{response[0]}"
    gpx = await threats(gpx)
    await event.delete()
    await bot.send_file(event.chat_id, gpx, reply_to=replied)


@register(outgoing=True, pattern=r"^\.trash(?: |$)(.*)")
async def dclxvi(event):
    replied = await event.get_reply_message()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await event.edit("reply to a supported media file")
        return
    if replied.media:
        await event.edit("passing to telegraph...")
    else:
        await event.edit("reply to a supported media file")
        return
    download_location = await bot.download_media(replied, TEMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await event.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
            os.remove(download_location)
            return
        await event.edit("generating image..")
    else:
        await event.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await event.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    gpx = f"https://telegra.ph{response[0]}"
    gpx = await trash(gpx)
    await event.delete()
    await bot.send_file(event.chat_id, gpx, reply_to=replied)


@register(outgoing=True, pattern=r"^\.trap(?: |$)(.*)")
async def dclxvi(event):
    input_str = event.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if "." in input_str:
        text1, text2 = input_str.split(".")
    else:
        await event.edit(
            "**Syntax :** reply to image or sticker with `.trap (name of the person to trap).(trapper name)`"
        )
        return
    replied = await event.get_reply_message()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await event.edit("reply to a supported media file")
        return
    if replied.media:
        await event.edit("passing to telegraph...")
    else:
        await event.edit("reply to a supported media file")
        return
    download_location = await bot.download_media(replied, TEMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await event.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
            os.remove(download_location)
            return
        await event.edit("generating image..")
    else:
        await event.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await event.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    gpx = f"https://telegra.ph{response[0]}"
    gpx = await trap(text1, text2, gpx)
    await event.delete()
    await bot.send_file(event.chat_id, gpx, reply_to=replied)


@register(outgoing=True, pattern=r"^\.phub(?: |$)(.*)")
async def dclxvi(event):
    input_str = event.pattern_match.group(1)
    input_str = deEmojify(input_str)
    if "." in input_str:
        username, text = input_str.split(".")
    else:
        await event.edit(
            "**Syntax :** reply to image or sticker with `.phub (username).(text in comment)`"
        )
        return
    replied = await event.get_reply_message()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if not replied:
        await event.edit("reply to a supported media file")
        return
    if replied.media:
        await event.edit("passing to telegraph...")
    else:
        await event.edit("reply to a supported media file")
        return
    download_location = await bot.download_media(replied, TEMP_DOWNLOAD_DIRECTORY)
    if download_location.endswith((".webp")):
        download_location = convert_toimage(download_location)
    size = os.stat(download_location).st_size
    if download_location.endswith((".jpg", ".jpeg", ".png", ".bmp", ".ico")):
        if size > 5242880:
            await event.edit(
                "the replied file size is not supported it must me below 5 mb"
            )
            os.remove(download_location)
            return
        await event.edit("generating image..")
    else:
        await event.edit("the replied file is not supported")
        os.remove(download_location)
        return
    try:
        response = upload_file(download_location)
        os.remove(download_location)
    except exceptions.TelegraphException as exc:
        await event.edit("ERROR: " + str(exc))
        os.remove(download_location)
        return
    gpx = f"https://telegra.ph{response[0]}"
    gpx = await phcomment(gpx, text, username)
    await event.delete()
    await bot.send_file(event.chat_id, gpx, reply_to=replied)


EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+"
)


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, "", inputString)


def convert_toimage(image):
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    os.remove(image)
    return "temp.jpg"


async def iphonex(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=iphonex&url={text}").json()
    query = r.get("message")
    gpxurl = url(query)
    if not gpxurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(query).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def baguette(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=baguette&url={text}"
    ).json()
    query = r.get("message")
    gpxurl = url(query)
    if not gpxurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(query).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def threats(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=threats&url={text}").json()
    query = r.get("message")
    gpxurl = url(query)
    if not gpxurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(query).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def lolice(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=lolice&url={text}").json()
    query = r.get("message")
    gpxurl = url(query)
    if not gpxurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(query).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def trash(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=trash&url={text}").json()
    query = r.get("message")
    gpxurl = url(query)
    if not gpxurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(query).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def awooify(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=awooify&url={text}").json()
    query = r.get("message")
    gpxurl = url(query)
    if not gpxurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(query).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def trap(text1, text2, text3):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=trap&name={text1}&author={text2}&image={text3}"
    ).json()
    query = r.get("message")
    gpxurl = url(query)
    if not gpxurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(query).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def phcomment(text1, text2, text3):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=phcomment&image={text1}&text={text2}&username={text3}"
    ).json()
    query = r.get("message")
    gpxurl = url(query)
    if not gpxurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(query).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


CMD_HELP.update(
    {
        "trolls": "TROLLS\
      \n\n>`.threats` reply to image or sticker \
      \nUsage: Changes the given pic to another pic which shows that pic content is threat to society as that of nuclear bomb .\
      \n\n>`.trash` reply to image or sticker\
      \nUsage: Changes the given pic to another pic which shows that pic content is as equal as to trash(waste).\
      \n\n>`.trap` (name of the person to trap).(trapper name) as reply to sticker/image.\
      \nUsage: Changes the given pic to another pic which shows that pic content is trapped in trap card.\
      \n\n>`.phub` (username).(text in comment) as reply to sticker/image.\
      \nUsage: Changes the given pic to another pic which shows that pic content as dp and shows a comment in phub with the given username.\
      "
    }
)
