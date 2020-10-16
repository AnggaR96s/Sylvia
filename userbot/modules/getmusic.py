import asyncio
import glob
import os
import time
from asyncio.exceptions import TimeoutError

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pylast import User
from selenium import webdriver
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, GOOGLE_CHROME_BIN, LASTFM_USERNAME, bot, lastfm
from userbot.events import register
from userbot.utils import progress


# For song and vsong
async def catmusic(cat, QUALITY):
    search = cat
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://www.youtube.com/results?search_query=" + search)
    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    for i in user_data:
        video_link = i.get_attribute("href")
        break
    if not os.path.isdir("./temp/"):
        os.makedirs("./temp/")
    command = (
        'youtube-dl -o "./temp/%(title)s.%(ext)s" --extract-audio --audio-format mp3 --audio-quality ' +
        QUALITY +
        " " +
        video_link)
    os.system(command)
    thumb = (
        'youtube-dl -o "./temp/%(title)s.%(ext)s" --write-thumbnail --skip-download ' +
        video_link)
    os.system(thumb)


async def catmusicvideo(cat):
    search = cat
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://www.youtube.com/results?search_query=" + search)
    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    for i in user_data:
        video_link = i.get_attribute("href")
        break
    if not os.path.isdir("./temp/"):
        os.makedirs("./temp/")
    command = (
        'youtube-dl -o "./temp/%(title)s.%(ext)s" -f "[filesize<50M]" ' +
        video_link)
    os.system(command)
    thumb = (
        'youtube-dl -o "./temp/%(title)s.%(ext)s" --write-thumbnail --skip-download ' +
        video_link)
    os.system(thumb)


@register(outgoing=True, pattern=r"^\.song(?: |$)(.*)")
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
        await event.edit("`Wait..! I am finding your song..`")
    elif reply.message:
        query = reply.message
        await event.edit("`Wait..! I am finding your song..`")
    else:
        await event.edit("`What I am Supposed to find?`")
        return
    await catmusic(str(query), "320k")
    l = glob.glob("./temp/*.mp3")
    if l:
        await event.edit("`Yeah..! I found something..`")
    else:
        await event.edit(f"Sorry..! I can't find anything with `{query}`")
        return
    thumbcat = glob.glob("./temp/*.jpg") + glob.glob("./temp/*.webp")
    if thumbcat:
        catthumb = thumbcat[0]
    else:
        catthumb = None
    loa = l[0]
    await event.edit("`Yeah.. Uploading your song..`")
    c_time = time.time()
    await bot.send_file(
        event.chat_id,
        loa,
        force_document=False,
        allow_cache=False,
        caption=query,
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "[UPLOAD]", loa)
        ),
    )
    await event.delete()
    os.system("rm -rf ./temp/*.mp3")
    os.system("rm -rf ./temp/*.jpg")
    os.system("rm -rf ./temp/*.webp")


@register(outgoing=True, pattern=r"^\.vsong(?: |$)(.*)")
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
        await event.edit("`Wait..! I am finding your videosong..`")
    elif reply.message:
        query = reply.message
        await event.edit("`Wait..! I am finding your videosong..`")
    else:
        await event.edit("`What I am Supposed to find?`")
        return
    await catmusicvideo(query)
    l = glob.glob(("./temp/*.mp4"))
    if l:
        await event.edit("`Yeah..! I found something..`")
    else:
        await event.edit(f"Sorry..! I can't find anything with `{query}`")
        return
    thumbcat = glob.glob("./temp/*.jpg") + glob.glob("./temp/*.webp")
    if thumbcat:
        catthumb = thumbcat[0]
    else:
        catthumb = None
    loa = l[0]
    metadata = extractMetadata(createParser(loa))
    if metadata.has("duration"):
        metadata.get("duration").seconds
    if metadata.has("width"):
        metadata.get("width")
    if metadata.has("height"):
        metadata.get("height")
    await event.edit("`Uploading video.. Please wait..`")
    c_time = time.time()
    await bot.send_file(
        event.chat_id,
        loa,
        force_document=False,
        allow_cache=False,
        thumb=catthumb,
        caption=query,
        supports_streaming=True,
        reply_to=reply_to_id,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "[UPLOAD]", loa)
        ),
    )
    await event.delete()
    os.system("rm -rf ./temp/*.mp4")
    os.system("rm -rf ./temp/*.jpg")
    os.system("rm -rf ./temp/*.webp")


@register(outgoing=True, pattern=r"^\.smd (?:(now)|(.*) - (.*))")
async def _(event):
    if event.fwd_from:
        return
    if event.pattern_match.group(1) == "now":
        playing = User(LASTFM_USERNAME, lastfm).get_now_playing()
        if playing is None:
            return await event.edit("`Error: No scrobbling data found.`")
        artist = playing.get_artist()
        song = playing.get_title()
    else:
        artist = event.pattern_match.group(2)
        song = event.pattern_match.group(3)
    track = str(artist) + " - " + str(song)
    chat = "@SpotifyMusicDownloaderBot"
    try:
        await event.edit("`Getting Your Music`")
        async with bot.conversation(chat) as conv:
            await asyncio.sleep(2)
            await event.edit("`Downloading...`")
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=752979930)
                )
                msg = await bot.send_message(chat, track)
                respond = await response
                res = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=752979930)
                )
                r = await res
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.reply("`Unblock `@SpotifyMusicDownloaderBot` and retry`")
                return
            await bot.forward_messages(event.chat_id, respond.message)
        await event.client.delete_messages(conv.chat_id, [msg.id, r.id, respond.id])
        await event.delete()
    except TimeoutError:
        return await event.edit(
            "`Error: `@SpotifyMusicDownloaderBot` is not responding or Song not found!.`"
        )


@register(outgoing=True, pattern=r"^\.net (?:(now)|(.*) - (.*))")
async def _(event):
    if event.fwd_from:
        return
    if event.pattern_match.group(1) == "now":
        playing = User(LASTFM_USERNAME, lastfm).get_now_playing()
        if playing is None:
            return await event.edit("`Error: No current scrobble found.`")
        artist = playing.get_artist()
        song = playing.get_title()
    else:
        artist = event.pattern_match.group(2)
        song = event.pattern_match.group(3)
    track = str(artist) + " - " + str(song)
    chat = "@WooMaiBot"
    link = f"/netease {track}"
    await event.edit("`Searching...`")
    try:
        async with bot.conversation(chat) as conv:
            await asyncio.sleep(2)
            await event.edit("`Processing... Please wait`")
            try:
                msg = await conv.send_message(link)
                response = await conv.get_response()
                respond = await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.reply("`Please unblock @WooMaiBot and try again`")
                return
            await event.edit("`Sending Your Music...`")
            await asyncio.sleep(3)
            await bot.send_file(event.chat_id, respond)
        await event.client.delete_messages(
            conv.chat_id, [msg.id, response.id, respond.id]
        )
        await event.delete()
    except TimeoutError:
        return await event.edit(
            "`Error: `@WooMaiBot` is not responding or Song not found!.`"
        )


@register(outgoing=True, pattern=r"^\.sdd(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    d_link = event.pattern_match.group(1)
    if ".com" not in d_link:
        await event.edit("`Enter a valid link to download from`")
    else:
        await event.edit("`Processing...`")
    chat = "@MusicsHunterbot"
    try:
        async with bot.conversation(chat) as conv:
            try:
                msg_start = await conv.send_message("/start")
                response = await conv.get_response()
                msg = await conv.send_message(d_link)
                details = await conv.get_response()
                song = await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.edit("`Unblock `@MusicsHunterbot` and retry`")
                return
            await bot.send_file(event.chat_id, song, caption=details.text)
            await event.client.delete_messages(
                conv.chat_id, [msg_start.id, response.id, msg.id, details.id, song.id]
            )
            await event.delete()
    except TimeoutError:
        return await event.edit(
            "`Error: `@MusicsHunterbot` is not responding or Song not found!.`"
        )


CMD_HELP.update(
    {
        "song": ">`.song` **Artist - Song Title**"
        "\nUsage: Finding and uploading song.\n\n"
        ">`.vsong` **Artist - Song Title**"
        "\nUsage: Finding and uploading videoclip.\n\n"
        ">`.smd` **Artist - Song Title**"
        "\nUsage: Download music from spotify use `@SpotifyMusicDownloaderBot`.\n\n"
        ">`.smd now`"
        "\nUsage: Download current LastFM scrobble use `@SpotifyMusicDownloaderBot`.\n\n"
        ">`.net` **Artist - Song Title**"
        "\nUsage: Download music use `@WooMaiBot`.\n\n"
        ">`.net now`"
        "\nUsage: Download current LastFM scrobble use `@WooMaiBot`.\n\n"
        ">`.sdd <Spotify/Deezer Link>`"
        "\nUsage: Download music from Spotify or Deezer use `@MusicsHunterbot`."})
