# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands for interacting with SlavBin(https://slav.gengkapak.my.id)"""
import os

from requests import exceptions, get, post
from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register

DOGBIN_URL = "https://slav.gengkapak.my.id/"
NEKOBIN_URL = "https://nekobin.com/"


@register(outgoing=True, pattern=r"^\.paste(?: |$)([\s\S]*)")
async def paste(pstl):
    """ For .paste command, pastes the text directly to slavbin. """
    dogbin_final_url = ""
    match = pstl.pattern_match.group(1).strip()
    reply_id = pstl.reply_to_msg_id

    if not (match or reply_id):
        return await pstl.edit("`Elon Musk said I cannot paste void.`")

    if match:
        message = match
    elif reply_id:
        message = await pstl.get_reply_message()
        if message.media:
            downloaded_file_name = await pstl.client.download_media(
                message,
                TEMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                try:
                    message += m.decode("UTF-8") + "\r"
                except UnicodeDecodeError:
                    return await pstl.edit("**Can't Decode file to text!**")
            os.remove(downloaded_file_name)
        else:
            message = message.message

    # SlavBin
    await pstl.edit("`Pasting text . . .`")
    resp = post(DOGBIN_URL + "documents", data=message.encode("utf-8"))

    if resp.status_code == 200:
        response = resp.json()
        key = response["key"]
        dogbin_final_url = DOGBIN_URL + key

        if response["isUrl"]:
            reply_text = (
                "`Pasted successfully!`\n\n"
                f"[Shortened URL]({dogbin_final_url})\n\n"
                "`Original(non-shortened) URLs`\n"
                f"[SlavBin URL]({DOGBIN_URL}v/{key})\n"
                f"[View RAW]({DOGBIN_URL}raw/{key})"
            )
        else:
            reply_text = (
                "`Pasted successfully!`\n\n"
                f"[SlavBin URL]({dogbin_final_url})\n"
                f"[View RAW]({DOGBIN_URL}raw/{key})"
            )
    else:
        reply_text = "`Failed to reach SlavBin`"

    await pstl.edit(reply_text)


@register(outgoing=True, pattern=r"^\.getpaste(?: |$)(.*)")
async def get_dogbin_content(dog_url):
    """ For .getpaste command, fetches the content of a SlavBin URL. """
    textx = await dog_url.get_reply_message()
    message = dog_url.pattern_match.group(1)
    await dog_url.edit("`Getting slavbin content...`")

    if textx:
        message = str(textx.message)

    format_normal = f"{DOGBIN_URL}"
    format_view = f"{DOGBIN_URL}v/"

    if message.startswith(format_view):
        message = message[len(format_view):]
    elif message.startswith(format_normal):
        message = message[len(format_normal):]
    elif message.startswith("slav.gengkapak.my.id/"):
        message = message[len("slav.gengkapak.my.id/"):]
    else:
        return await dog_url.edit("`Is that even a SlavBin url?`")

    resp = get(f"{DOGBIN_URL}raw/{message}")

    try:
        resp.raise_for_status()
    except exceptions.HTTPError as HTTPErr:
        await dog_url.edit(
            "Request returned an unsuccessful status code.\n\n" + str(HTTPErr)
        )
        return
    except exceptions.Timeout as TimeoutErr:
        await dog_url.edit("Request timed out." + str(TimeoutErr))
        return
    except exceptions.TooManyRedirects as RedirectsErr:
        await dog_url.edit(
            "Request exceeded the configured number of maximum redirections."
            + str(RedirectsErr)
        )
        return

    reply_text = (
        "`Fetched SlavBin URL content successfully!`"
        "\n\n`Content:` " + resp.text)

    await dog_url.edit(reply_text)


@register(outgoing=True, pattern=r"^\.neko(?: |$)([\s\S]*)")
async def neko(nekobin):
    """For .paste command, pastes the text directly to nekobin."""
    nekobin_final_url = ""
    match = nekobin.pattern_match.group(1).strip()
    reply_id = nekobin.reply_to_msg_id

    if not match and not reply_id:
        return await nekobin.edit("`Cannot paste text.`")

    if match:
        message = match
    elif reply_id:
        message = await nekobin.get_reply_message()
        if message.media:
            downloaded_file_name = await nekobin.client.download_media(
                message,
                TEMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                try:
                    message += m.decode("UTF-8")
                except UnicodeDecodeError:
                    return await nekobin.edit("**Can't Decode file to text!**")
            os.remove(downloaded_file_name)
        else:
            message = message.text

    # Nekobin
    await nekobin.edit("`Pasting text . . .`")
    resp = post(NEKOBIN_URL + "api/documents", json={"content": message})

    if resp.status_code == 201:
        response = resp.json()
        key = response["result"]["key"]
        nekobin_final_url = NEKOBIN_URL + key
        reply_text = (
            "`Pasted successfully!`\n\n"
            f"[Nekobin URL]({nekobin_final_url})\n"
            f"[View RAW]({NEKOBIN_URL}raw/{key})"
        )
    else:
        reply_text = "`Failed to reach Nekobin`"

    await nekobin.edit(reply_text)


@register(outgoing=True, pattern=r"^\.kat(?: |$)([\s\S]*)")
async def kat(katbin):
    """For .kat command, pastes the text directly to katbin."""
    match = katbin.pattern_match.group(1).strip()
    reply_id = katbin.reply_to_msg_id

    if not match and not reply_id:
        return await katbin.edit("`Cannot paste text.`")

    if match:
        message = match
    elif reply_id:
        message = await katbin.get_reply_message()
        if message.media:
            downloaded_file_name = await katbin.client.download_media(
                message,
                TEMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                try:
                    message += m.decode("UTF-8")
                except UnicodeDecodeError:
                    return await katbin.edit("**Can't Decode file to text!**")
            os.remove(downloaded_file_name)
        else:
            message = message.text

    # Katbin
    await katbin.edit("`Pasting text . . .`")
    resp = post("https://api.katb.in/api/paste",
                json={"content": message}).json()

    if resp["msg"] == "Successfully created paste":
        await katbin.edit(
            f"**Pasted successfully:**\n[Katb.in](https://katb.in/{resp['paste_id']})\n[View RAW](https://katb.in/{resp['paste_id']}/raw)"
        )
    else:
        await katbin.edit("**Katb.in seems to be down.**")

CMD_HELP.update(
    {
        "paste": ">`.paste <text/reply>`"
        "\nUsage: Create a paste or a shortened url using [Slavbin](https://slav.gengkapak.my.id/)"
        "\n\n>`.getpaste`"
        "\nUsage: Gets the content of a paste or shortened url from [SlavBin](https://slav.gengkapak.my.id/)"
        "\n\n>`.neko`"
        "\nUsage: Same as `.paste` but with [Nekobin](https://nekobin.com/)"
        "\n\n>`.kat`"
        "\nUsage: Same as `.paste` but with [Katb.in](https://katb.in/)"})
