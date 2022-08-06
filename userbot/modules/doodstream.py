import os
import time
from telethon.tl.types import DocumentAttributeFilename
from userbot import APIDOOD, CMD_HELP, bot
from userbot.events import register
from doodstream import DoodStream
from FastTelethonhelper import fast_download

api = APIDOOD
d = DoodStream(api)


@register(outgoing=True, pattern=r"^\.dood")
async def dood(event):
    if not event.reply_to_msg_id:
        await event.edit("`Reply to any media..`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("`reply to a video..`")
        return
    if reply_message.photo:
        return await event.edit("`Hey..this is an image!`")
    if (
        DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
        in reply_message.media.document.attributes
    ):
        return await event.edit("`Unsupported files..`")
    elif (
        DocumentAttributeFilename(file_name="sticker.webp")
        in reply_message.media.document.attributes
    ):
        return await event.edit("`Unsupported files..`")
    time.time()
    r = await event.edit("`Downloading media..`")
    ss = await fast_download(bot, reply_message, r)
    try:
        await r.edit("`Proccessing..`")
        up = d.local_upload(f"{ss}")
        res = f"Status : {up['status']}\n"
        res += f"Video ID : {up['result'][0]['filecode']}\n"
        res += f"Video Url : {up['result'][0]['download_url']}\n"
        res += f"Splash IMG : {up['result'][0]['splash_img']}"
        os.remove(ss)
        await r.edit(res)
    except BaseException as e:
        return await r.edit(f"{e}")


@register(outgoing=True, pattern=r"^\.dr ?(.*)")
async def upload(event):
    await event.edit("`Processing..`")
    await event.get_reply_message()
    message = event.pattern_match.group(1)
    if "http://" in message or "https://" in message:
        r = d.remote_upload(f"{message}")
        res = f"Status : {r['msg']}\n"
        res += f"File ID : {r['result']['filecode']}\n"
        res += f"Video  Url : `https://doodstream.com/d/{r['result']['filecode']}`"
        await event.edit(res)
    else:
        await event.edit("`Error..`")


CMD_HELP.update(
    {
        "doodstream": ">`.dood` Reply to media."
        "\nUsage: Upload media to doodstrean.\n\n"
        ">`.dr` <direct link>"
        "\nUsage: Mirror direct link video to doodstream"
    }
)
