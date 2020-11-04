import os
from asyncio.exceptions import TimeoutError

from PIL import Image
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.spotnow$")
async def _(event):
    if event.fwd_from:
        return
    chat = "@SpotifyNowBot"
    now = f"/now"
    await event.edit("`Processing...`")
    try:
        async with event.client.conversation(chat) as conv:
            try:
                msg = await conv.send_message(now)
                response = await conv.get_response()
                """don't spam notif"""
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.reply("`Please unblock` @SpotifyNowBot`...`")
                return
            if response.text.startswith("You're"):
                await event.edit(
                    "`You're not listening to anything on Spotify at the moment`"
                )
                await event.client.delete_messages(conv.chat_id, [msg.id, response.id])
                return
            if response.text.startswith("Ads."):
                await event.edit("`You're listening to those annoying ads.`")
                await event.client.delete_messages(conv.chat_id, [msg.id, response.id])
                return
            else:
                downloaded_file_name = await event.client.download_media(
                    response.media, TEMP_DOWNLOAD_DIRECTORY
                )
                gambar = Image.open(f"{downloaded_file_name}").convert("RGB")
                gambar.save("spotify.webp", "webp")
                link = response.reply_markup.rows[0].buttons[0].url
                await event.client.send_file(
                    event.chat_id,
                    file="spotify.webp",
                    force_document=False,
                    reply_to=event.message.id,
                )
                """cleanup chat after completed"""
                await event.client.delete_messages(conv.chat_id, [msg.id, response.id])
        await event.edit(f"[Play on Spotify]({link})")
        os.remove(downloaded_file_name)
        return os.remove("spotify.webp")
    except TimeoutError:
        return await event.edit("`Error: `@SpotifyNowBot` is not responding!.`")


CMD_HELP.update(
    {
        "spotifynow": ">`.spotnow`"
        "\nUsage: Show what you're listening on spotify."
        "\n@SpotifyNowBot"
    }
)
