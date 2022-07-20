# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

import asyncio
import json
import re
from re import findall as re_findall, search as re_search
from requests import get as rget
import urllib.parse
from asyncio import create_subprocess_shell as asyncSubprocess
from asyncio.subprocess import PIPE as asyncPIPE
from cgi import parse_header
from random import choice
from urllib.parse import urlparse
from base64 import standard_b64encode
import aiohttp
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from humanize import naturalsize
import lk21
import cfscrape
from userbot import CMD_HELP, USR_TOKEN
from userbot.events import register
from userbot.utils import humanbytes, time_formatter


async def subprocess_run(cmd):
    reply = ""
    subproc = await asyncSubprocess(cmd, stdout=asyncPIPE, stderr=asyncPIPE)
    result = await subproc.communicate()
    exitCode = subproc.returncode
    if exitCode != 0:
        reply += (
            "**An error was detected while running subprocess.**\n"
            f"exitCode : `{exitCode}`\n"
            f"stdout : `{result[0].decode().strip()}`\n"
            f"stderr : `{result[1].decode().strip()}`"
        )
        return reply
    return result


@register(outgoing=True, pattern=r"^\.direct(?: |$)([\s\S]*)")
async def direct_link_generator(request):
    await request.edit("`Processing...`")
    textx = await request.get_reply_message()
    message = request.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await request.edit("`Usage: .direct <url>`")
        return
    reply = ""
    links = re.findall(r"\bhttps?://.*\.\S+", message)
    if not links:
        reply = "`No links found!`"
        await request.edit(reply)
    for link in links:
        if "zippyshare.com" in link:
            reply += await zippy_share(link)
        elif "yadi.sk" in link:
            reply += await yandex_disk(link)
        elif "cloud.mail.ru" in link:
            reply += await cm_ru(link)
        elif "mediafire.com" in link:
            reply += await mediafire(link)
        elif "sourceforge.net" in link:
            reply += await sourceforge(link)
        elif "osdn.net" in link:
            reply += await osdn(link)
        elif "github.com" in link:
            reply += await github(link)
        elif "androidfilehost.com" in link:
            reply += await androidfilehost(link)
        elif "1drv.ms" in link:
            reply += await onedrive(link)
        elif "solidfiles.com" in link:
            reply += await solid(link)
        elif 'hxfile.co' in link:
            reply += await hxfile(link)
        elif 'anonfiles.com' in link:
            reply += await anonfiles(link)
        elif 'letsupload.io' in link:
            reply += await letsupload(link)
        elif 'fembed.net' in link:
            reply += await fembed(link)
        elif 'fembed.com' in link:
            reply += await fembed(link)
        elif 'femax20.com' in link:
            reply += await fembed(link)
        elif 'fcdn.stream' in link:
            reply += await fembed(link)
        elif 'feurl.com' in link:
            reply += await fembed(link)
        elif 'naniplay.nanime.in' in link:
            reply += await fembed(link)
        elif 'naniplay.nanime.biz' in link:
            reply += await fembed(link)
        elif 'naniplay.com' in link:
            reply += await fembed(link)
        elif 'layarkacaxxi.icu' in link:
            reply += await fembed(link)
        elif 'sbembed.com' in link:
            reply += await sbembed(link)
        elif 'streamsb.net' in link:
            reply += await sbembed(link)
        elif 'sbplay.org' in link:
            reply += await sbembed(link)
        elif 'pixeldrain.com' in link:
            reply += await pixeldrain(link)
        elif 'antfiles.com' in link:
            reply += await antfiles(link)
        elif 'streamtape.com' in link:
            reply += await streamtape(link)
        elif 'bayfiles.com' in link:
            reply += await anonfiles(link)
        elif 'racaty.net' in link:
            reply += await racaty(link)
        elif '1fichier.com' in link:
            reply += await fichier(link)
        elif "uptobox.com" in link:
            await uptobox(request, link)
            return None
        else:
            reply += re.findall(r"\bhttps?://(.*?[^/]+)",
                                link)[0] + "is not supported"
    await request.edit(reply)


async def zippy_share(url: str) -> str:
    try:
        link = re_findall(r'\bhttps?://.*zippyshare\.com\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("ERROR: No Zippyshare links found")
    try:
        base_url = re_search('http.+.zippyshare.com/', link).group()
        response = rget(link).content
        pages = BeautifulSoup(response, "lxml")
        js_script = pages.find(
            "div",
            style="margin-left: 24px; margin-top: 20px; text-align: center; width: 303px; height: 105px;")
        js_content = re_findall(r'\.href.=."/(.*?)";', str(js_script))[0]
        js_content = str(js_content).split('"')
        a = str(js_script).split('var a = ')[1].split(';')[0]
        value = int(a) ** 3 + 3
        return base_url + js_content[0] + str(value) + js_content[2]
    except IndexError:
        raise DirectDownloadLinkException("ERROR: Can't find download button")


async def yandex_disk(url: str) -> str:
    reply = ""
    try:
        link = re.findall(r"\bhttps?://.*yadi\.sk\S+", url)[0]
    except IndexError:
        reply = "`No Yandex.Disk links found`\n"
        return reply
    api = "https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}"
    try:
        dl_url = requests.get(api.format(link)).json()["href"]
        name = dl_url.split("filename=")[1].split("&disposition")[0]
        reply += f"[{name}]({dl_url})\n"
    except KeyError:
        reply += "`Error: File not found / Download limit reached`\n"
        return reply
    return reply


async def cm_ru(url: str) -> str:
    reply = ""
    try:
        link = re.findall(r"\bhttps?://.*cloud\.mail\.ru\S+", url)[0]
    except IndexError:
        reply = "`No cloud.mail.ru links found`\n"
        return reply
    cmd = f"bin/cmrudl -s {link}"
    result = subprocess_run(cmd)
    try:
        result = result[0].splitlines()[-1]
        data = json.loads(result)
    except json.decoder.JSONDecodeError:
        reply += "`Error: Can't extract the link`\n"
        return reply
    except IndexError:
        return reply
    dl_url = data["download"]
    name = data["file_name"]
    size = naturalsize(int(data["file_size"]))
    reply += f"[{name} ({size})]({dl_url})\n"
    return reply


async def mediafire(url: str) -> str:
    try:
        link = re.findall(r"\bhttps?://.*mediafire\.com\S+", url)[0]
    except IndexError:
        reply = "`No MediaFire links found`\n"
        return reply
    reply = ""
    page = BeautifulSoup(requests.get(link).content, "lxml")
    info = page.find("a", {"aria-label": "Download file"})
    dl_url = info.get("href")
    size = re.findall(r"\(.*\)", info.text)[0]
    name = page.find("div", {"class": "filename"}).text
    reply += f"[{name} {size}]({dl_url})\n"
    return reply


async def sourceforge(url: str) -> str:
    try:
        link = re.findall(r"\bhttps?://.*sourceforge\.net\S+", url)[0]
    except IndexError:
        reply = "`No SourceForge links found`\n"
        return reply
    file_path = re.findall(r"files(.*)/download", link)[0]
    reply = f"Mirrors for __{file_path.split('/')[-1]}__\n"
    project = re.findall(r"projects?/(.*?)/files", link)[0]
    mirrors = (
        f"https://sourceforge.net/settings/mirror_choices?"
        f"projectname={project}&filename={file_path}"
    )
    page = BeautifulSoup(requests.get(mirrors).content, "html.parser")
    info = page.find("ul", {"id": "mirrorList"}).findAll("li")
    for mirror in info[1:]:
        name = re.findall(r"\((.*)\)", mirror.text.strip())[0]
        dl_url = (
            f'https://{mirror["id"]}.dl.sourceforge.net/project/{project}/{file_path}'
        )
        reply += f"[{name}]({dl_url}) "
    return reply


async def osdn(url: str) -> str:
    osdn_link = "https://osdn.net"
    try:
        link = re.findall(r"\bhttps?://.*osdn\.net\S+", url)[0]
    except IndexError:
        reply = "`No OSDN links found`\n"
        return reply
    page = BeautifulSoup(
        requests.get(
            link,
            allow_redirects=True).content,
        "lxml")
    info = page.find("a", {"class": "mirror_link"})
    link = urllib.parse.unquote(osdn_link + info["href"])
    reply = f"Mirrors for __{link.split('/')[-1]}__\n"
    mirrors = page.find("form", {"id": "mirror-select-form"}).findAll("tr")
    for data in mirrors[1:]:
        mirror = data.find("input")["value"]
        name = re.findall(r"\((.*)\)", data.findAll("td")[-1].text.strip())[0]
        dl_url = re.sub(r"m=(.*)&f", f"m={mirror}&f", link)
        reply += f"[{name}]({dl_url}) "
    return reply


async def github(url: str) -> str:
    try:
        link = re.findall(r"\bhttps?://.*github\.com.*releases\S+", url)[0]
    except IndexError:
        reply = "`No GitHub Releases links found`\n"
        return reply
    reply = ""
    dl_url = ""
    download = requests.get(url, stream=True, allow_redirects=False)
    try:
        dl_url = download.headers["location"]
    except KeyError:
        reply += "`Error: Can't extract the link`\n"
    name = link.split("/")[-1]
    reply += f"[{name}]({dl_url}) "
    return reply


async def androidfilehost(url: str) -> str:
    try:
        link = re.findall(r"\bhttps?://.*androidfilehost.*fid.*\S+", url)[0]
    except IndexError:
        reply = "`No AFH links found`\n"
        return reply
    fid = re.findall(r"\?fid=(.*)", link)[0]
    headers = Headers().generate()
    res = requests.get(link)
    headers = {
        "User-Agent": headers["User-Agent"],
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": f"https://androidfilehost.com/?fid={fid}",
        "X-MOD-SBB-CTYPE": "xhr",
        "X-Requested-With": "XMLHttpRequest",
    }
    data = {
        "submit": "submit",
        "action": "getdownloadmirrors",
        "fid": f"{fid}"}
    mirrors = None
    reply = ""
    error = "**ERROR:** `Can't find Mirrors for the link`\n"

    try:
        req = requests.post(
            "https://androidfilehost.com/libs/otf/mirrors.otf.php",
            headers=headers,
            data=data,
            cookies=res.cookies,
        )
        mirrors = req.json()["MIRRORS"]
    except (json.decoder.JSONDecodeError, TypeError):
        reply += error

    if not mirrors:
        reply += error
        return reply
    for item in mirrors:
        name = item["name"]
        dl_url = item["url"]
        reply += f"[{name}]({dl_url}) | "
    _, params = parse_header(requests.head(
        dl_url).headers["Content-Disposition"])
    reply = f"Mirrors for `{params['filename']}`\n{reply.rstrip('| ')}"
    return reply


async def solid(url: str) -> str:
    """ Solidfiles direct links generator
    Based on https://github.com/Xonshiz/SolidFiles-Downloader
    By https://github.com/Jusidama18 """
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    pageSource = requests.get(url, headers=headers).text
    mainOptions = str(
        re.search(
            r'viewerOptions\'\,\ (.*?)\)\;',
            pageSource).group(1))
    reply = json.loads(mainOptions)["downloadUrl"]
    return reply


async def uptobox(request, url: str) -> str:
    try:
        link = re.findall(r"\bhttps?://.*uptobox\.com\S+", url)[0]
    except IndexError:
        await request.edit("`No uptobox links found.`")
        return
    if USR_TOKEN is None:
        await request.edit("`Set USR_TOKEN_UPTOBOX first!`")
        return
    if link.endswith("/"):
        index = -2
    else:
        index = -1
    FILE_CODE = link.split("/")[index]
    origin = "https://uptobox.com/api/link"
    uri = f"{origin}/info?fileCodes={FILE_CODE}"
    await request.edit("`Retrieving file informations...`")
    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as response:
            result = json.loads(await response.text())
            data = result.get("data").get("list")[0]
            if "error" in data:
                await request.edit(
                    "`[ERROR]`\n"
                    f"`statusCode`: **{data.get('error').get('code')}**\n"
                    f"`reason`: **{data.get('error').get('message')}**"
                )
                return
            file_name = data.get("file_name")
            file_size = naturalsize(data.get("file_size"))
    uri = f"{origin}?token={USR_TOKEN}&file_code={FILE_CODE}"
    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as response:
            result = json.loads(await response.text())
            status = result.get("message")
            if status == "Waiting needed":
                wait = result.get("data").get("waiting")
                waitingToken = result.get("data").get("waitingToken")
                await request.edit(f"`Waiting for about {time_formatter(wait)}.`")
                # for some reason it doesn't go as i planned
                # so make it 1 minute just to be save enough
                await asyncio.sleep(wait + 60)
                uri += f"&waitingToken={waitingToken}"
                async with session.get(uri) as response:
                    await request.edit("`Generating direct download link...`")
                    result = json.loads(await response.text())
                    status = result.get("message")
                    if status == "Success":
                        webLink = result.get("data").get("dlLink")
                        await request.edit(f"[{file_name} ({file_size})]({webLink})")
                        return
                    else:
                        await request.edit(
                            "`[ERROR]`\n"
                            f"`statusCode`: **{result.get('statusCode')}**\n"
                            f"`reason`: **{result.get('data')}**\n"
                            f"`status`: **{status}**"
                        )
                        return
            elif status == "Success":
                webLink = result.get("data").get("dlLink")
                await request.edit(f"[{file_name} ({file_size})]({webLink})")
                return
            else:
                await request.edit(
                    "`[ERROR]`\n"
                    f"`statusCode`: **{result.get('statusCode')}**\n"
                    f"`reason`: **{result.get('data')}**\n"
                    f"`status`: **{status}**"
                )
                return


async def onedrive(link: str) -> str:
    link_without_query = urlparse(link)._replace(query=None).geturl()
    direct_link_encoded = str(
        standard_b64encode(
            bytes(
                link_without_query,
                "utf-8")),
        "utf-8")
    direct_link1 = f"https://api.onedrive.com/v1.0/shares/u!{direct_link_encoded}/root/content"
    resp = requests.head(direct_link1)
    if resp.status_code != 302:
        return "`Error: Unauthorized link, the link may be private`"
    dl_link = resp.next.url
    file_name = dl_link.rsplit("/", 1)[1]
    resp2 = requests.head(dl_link)
    dl_size = humanbytes(int(resp2.headers["Content-Length"]))
    return f"[{file_name} ({dl_size})]({dl_link})"


async def fembed(link: str) -> str:
    """ Fembed direct link generator
    Based on https://github.com/zevtyardt/lk21
             https://github.com/breakdowns/slam-aria-mirror-bot """
    bypasser = lk21.Bypass()
    dl_url = bypasser.bypass_fembed(link)
    reply = []
    count = len(dl_url)
    for i in reply:
        reply.append(dl_url[i])
    return reply[count - 1]


async def sbembed(link: str) -> str:
    """ Sbembed direct link generator
    Based on https://github.com/zevtyardt/lk21
             https://github.com/breakdowns/slam-aria-mirror-bot """
    bypasser = lk21.Bypass()
    dl_url = bypasser.bypass_sbembed(link)
    reply = []
    count = len(dl_url)
    for i in dl_url:
        reply.append(dl_url[i])
    return reply[count - 1]


async def hxfile(url: str) -> str:
    """ Hxfile direct link generator
    Based on https://github.com/zevtyardt/lk21
             https://github.com/breakdowns/slam-aria-mirror-bot """
    bypasser = lk21.Bypass()
    reply = bypasser.bypass_filesIm(url)
    return reply


async def anonfiles(url: str) -> str:
    """ Anonfiles direct link generator
    Based on https://github.com/zevtyardt/lk21
             https://github.com/breakdowns/slam-aria-mirror-bot """
    bypasser = lk21.Bypass()
    reply = bypasser.bypass_anonfiles(url)
    return reply


async def letsupload(url: str) -> str:
    """ Letsupload direct link generator
    Based on https://github.com/zevtyardt/lk21
             https://github.com/breakdowns/slam-aria-mirror-bot """
    reply = ''
    try:
        link = re.findall(r'\bhttps?://.*letsupload\.io\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("No Letsupload links found\n")
    bypasser = lk21.Bypass()
    reply = bypasser.bypass_url(link)
    return reply


async def pixeldrain(url: str) -> str:
    """ Based on https://github.com/yash-dk/TorToolkit-Telegram """
    url = url.strip("/ ")
    file_id = url.split("/")[-1]
    info_link = f"https://pixeldrain.com/api/file/{file_id}/info"
    reply = f"https://pixeldrain.com/api/file/{file_id}"
    resp = requests.get(info_link).json()
    if resp["success"]:
        return reply
    else:
        raise DirectDownloadLinkException(
            "ERROR: Cant't download due {}.".format(
                resp.text["value"]))


async def antfiles(url: str) -> str:
    """ Antfiles direct link generator
    Based on https://github.com/zevtyardt/lk21
             https://github.com/breakdowns/slam-aria-mirror-bot """
    bypasser = lk21.Bypass()
    reply = bypasser.bypass_antfiles(url)
    return reply


async def streamtape(url: str) -> str:
    """ Streamtape direct link generator
    Based on https://github.com/zevtyardt/lk21
             https://github.com/breakdowns/slam-aria-mirror-bot """
    bypasser = lk21.Bypass()
    reply = bypasser.bypass_streamtape(url)
    return reply


async def racaty(url: str) -> str:
    """ Racaty direct links generator
    based on https://github.com/breakdowns/slam-aria-mirror-bot """
    reply = ''
    try:
        link = re.findall(r'\bhttps?://.*racaty\.net\S+', url)[0]
    except IndexError:
        raise DirectDownloadLinkException("No Racaty links found\n")
    scraper = cfscrape.create_scraper()
    r = scraper.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    op = soup.find("input", {"name": "op"})["value"]
    ids = soup.find("input", {"name": "id"})["value"]
    rpost = scraper.post(url, data={"op": op, "id": ids})
    rsoup = BeautifulSoup(rpost.text, "lxml")
    reply = rsoup.find("a", {"id": "uniqueExpirylink"})[
        "href"].replace(" ", "%20")
    return reply


async def fichier(link: str) -> str:
    """ 1Fichier direct links generator
    Based on https://github.com/Maujar
             https://github.com/breakdowns/slam-aria-mirror-bot """
    regex = r"^([http:\/\/|https:\/\/]+)?.*1fichier\.com\/\?.+"
    gan = re.match(regex, link)
    if not gan:
        raise DirectDownloadLinkException(
            "ERROR: The link you entered is wrong!")
    if "::" in link:
        pswd = link.split("::")[-1]
        url = link.split("::")[-2]
    else:
        pswd = None
        url = link
    try:
        if pswd is None:
            req = requests.post(url)
        else:
            pw = {"pass": pswd}
            req = requests.post(url, data=pe)
    except BaseException:
        raise DirectDownloadLinkException(
            "ERROR: Unable to reach 1fichier server!")
    if req.status_code == 404:
        raise DirectDownloadLinkException(
            "ERROR: File not found/The link you entered is wrong!")
    soup = BeautifulSoup(req.content, 'lxml')
    if soup.find("a", {"class": "ok btn-general btn-orange"}) is not None:
        reply = soup.find("a", {"class": "ok btn-general btn-orange"})["href"]
        if reply is None:
            raise DirectDownloadLinkException(
                "ERROR: Unable to generate Direct Link 1fichier!")
        else:
            return reply
    else:
        if len(soup.find_all("div", {"class": "ct_warn"})) == 2:
            str_2 = soup.find_all("div", {"class": "ct_warn"})[-1]
            if "you must wait" in str(str_2).lower():
                numbers = [int(word)
                           for word in str(str_2).split() if word.isdigit()]
                if len(numbers) == 0:
                    raise DirectDownloadLinkException(
                        "ERROR: 1fichier is on a limit. Please wait a few minutes/hour.")
                else:
                    raise DirectDownloadLinkException(
                        f"ERROR: 1fichier is on a limit. Please wait {numbers[0]} minute.")
            elif "protect access" in str(str_2).lower():
                raise DirectDownloadLinkException(
                    "ERROR: This link requires a password!\n\n<b>This link requires a password!</b>\n- Insert sign <b>::</b> after the link and write the password after the sign.\n\n<b>Example:</b>\n<code>/mirror https://1fichier.com/?smmtd8twfpm66awbqz04::love you</code>\n\n* No spaces between the signs <b>::</b>\n* For the password, you can use a space!")
            else:
                raise DirectDownloadLinkException(
                    "ERROR: Error trying to generate Direct Link from 1fichier!")
        elif len(soup.find_all("div", {"class": "ct_warn"})) == 3:
            str_1 = soup.find_all("div", {"class": "ct_warn"})[-2]
            str_3 = soup.find_all("div", {"class": "ct_warn"})[-1]
            if "you must wait" in str(str_1).lower():
                numbers = [int(word)
                           for word in str(str_1).split() if word.isdigit()]
                if len(numbers) == 0:
                    raise DirectDownloadLinkException(
                        "ERROR: 1fichier is on a limit. Please wait a few minutes/hour.")
                else:
                    raise DirectDownloadLinkException(
                        f"ERROR: 1fichier is on a limit. Please wait {numbers[0]} minute.")
            elif "bad password" in str(str_3).lower():
                raise DirectDownloadLinkException(
                    "ERROR: The password you entered is wrong!")
            else:
                raise DirectDownloadLinkException(
                    "ERROR: Error trying to generate Direct Link from 1fichier!")
        else:
            raise DirectDownloadLinkException(
                "ERROR: Error trying to generate Direct Link from 1fichier!")


async def useragent():
    useragents = BeautifulSoup(
        requests.get(
            "https://developers.whatismybrowser.com/"
            "useragents/explore/operating_system_name/android/"
        ).content,
        "lxml",
    ).findAll("td", {"class": "useragent"})
    user_agent = choice(useragents)
    return user_agent.text


CMD_HELP.update(
    {
        "direct": ">`.direct <url>`"
        "\nUsage: Reply to a link or paste a URL to\n"
        "generate a direct download link\n\n"
        "List of supported URLs:\n"
        "`Cloud Mail - Yandex.Disk - AFH - "
        "ZippyShare - MediaFire - SourceForge - OSDN - GitHub - Uptobox`"
    }
)
