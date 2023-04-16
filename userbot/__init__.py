# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot initialization. """

import os
import re
import time
from distutils.util import strtobool as sb
from logging import DEBUG, INFO, basicConfig, getLogger
from math import ceil
from sys import version_info
from time import sleep

from dotenv import load_dotenv
from pylast import LastFMNetwork, md5
from pySmartDL import SmartDL
from requests import get
from telethon.sessions import StringSession
from telethon.sync import TelegramClient, custom, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged

load_dotenv("config.env")

StartTime = time.time()


def paginate_help(page_number, loaded_modules, prefix):
    number_of_rows = 5
    number_of_cols = 2
    helpable_modules = [p for p in loaded_modules if not p.startswith("_")]
    helpable_modules = sorted(helpable_modules)
    modules = [
        custom.Button.inline("{} {}".format("🔸", x), data="ub_modul_{}".format(x))
        for x in helpable_modules
    ]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows: number_of_rows * (modulo_page + 1)
        ] + [
            (
                custom.Button.inline(
                    "⬅️", data="{}_prev({})".format(prefix, modulo_page)
                ),
                custom.Button.inline(
                    "➡️", data="{}_next({})".format(prefix, modulo_page)
                ),
            )
        ]
    return pairs


# Bot Logs setup:
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

ASYNC_POOL = []

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=INFO)
LOGS = getLogger(__name__)

if version_info < (3, 9, 0):
    LOGS.info(
        "You MUST have a python version of at least 3.8."
        "Multiple features depend on this. Bot quitting."
    )
    quit(1)

# Check if the config was edited by using the already used variable.
# Basically, its the 'virginity check' for the config file ;)
CONFIG_CHECK = os.environ.get(
    "___________PLOX_______REMOVE_____THIS_____LINE__________", None
)

if CONFIG_CHECK:
    LOGS.info(
        "Please remove the line mentioned in the first hashtag from the config.env file"
    )
    quit(1)

# Telegram App KEY and HASH
API_KEY = os.environ.get("API_KEY", None)
API_HASH = os.environ.get("API_HASH", None)

# UserBot Session String
STRING_SESSION = os.environ.get("STRING_SESSION", None)

# Logging channel/group ID configuration
BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", None))

# Userbot logging feature switch.
BOTLOG = sb(os.environ.get("BOTLOG", "False"))
LOGSPAMMER = sb(os.environ.get("LOGSPAMMER", "False"))

# Bleep Blop, this is a bot ;)
PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN", "False"))

# Heroku Credentials for updater.
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)

# Custom (forked) repo URL for updater.
UPSTREAM_REPO_URL = os.environ.get(
    "UPSTREAM_REPO_URL", "https://github.com/AnggaR96s/Sylvia.git"
)
# UPSTREAM_REPO_URL branch, the default is master
UPSTREAM_REPO_BRANCH = os.environ.get("UPSTREAM_REPO_BRANCH", "master")

# Console verbose logging
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

# SQL Database URI
DB_URI = os.environ.get("DATABASE_URL", None)

# DoodStream
APIDOOD = os.environ.get("APIDOOD", None)

# OCR API key
OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", None)

# remove.bg API key
REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)

# Default .alive name
ALIVE_NAME = os.environ.get("ALIVE_NAME", None)

# Chrome stuff
CHROME_DRIVER = os.environ.get("CHROME_DRIVER", "/usr/bin/chromedriver")
GOOGLE_CHROME_BIN = os.environ.get(
    "GOOGLE_CHROME_BIN",
    "/usr/bin/google-chrome")

# Weather stuff
OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)
WEATHER_DEFCITY = os.environ.get("WEATHER_DEFCITY", None)
WEATHER_DEFLANG = os.environ.get("WEATHER_DEFLANG", None)

# Anti Spambot
ANTI_SPAMBOT = sb(os.environ.get("ANTI_SPAMBOT", "False"))
ANTI_SPAMBOT_SHOUT = sb(os.environ.get("ANTI_SPAMBOT_SHOUT", "False"))

# Time & Date - Country and Time Zone
COUNTRY = str(os.environ.get("COUNTRY", ""))
TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))

# Clean Welcome
CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME", "True"))

# Last.fm Module
BIO_PREFIX = os.environ.get("BIO_PREFIX", None)
DEFAULT_BIO = os.environ.get("DEFAULT_BIO", None)

LASTFM_API = os.environ.get("LASTFM_API", None)
LASTFM_SECRET = os.environ.get("LASTFM_SECRET", None)
LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME", None)
LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD", None)
LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)
if LASTFM_API and LASTFM_SECRET and LASTFM_USERNAME and LASTFM_PASS:
    lastfm = LastFMNetwork(
        api_key=LASTFM_API,
        api_secret=LASTFM_SECRET,
        username=LASTFM_USERNAME,
        password_hash=LASTFM_PASS,
    )
else:
    lastfm = None


# bit.ly module
BITLY_TOKEN = os.environ.get("BITLY_TOKEN", None)

# Google Drive Module
G_DRIVE_DATA = os.environ.get("G_DRIVE_DATA", None)
G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
G_DRIVE_AUTH_TOKEN_DATA = os.environ.get("G_DRIVE_AUTH_TOKEN_DATA", None)
G_DRIVE_FOLDER_ID = os.environ.get("G_DRIVE_FOLDER_ID", None)

# Download directory location
TEMP_DOWNLOAD_DIRECTORY = os.environ.get(
    "TMP_DOWNLOAD_DIRECTORY", "./downloads")

# Terminal Alias
TERM_ALIAS = os.environ.get("TERM_ALIAS", None)

# Wolfram ID
# Get an API KEY from products.wolframalpha.com/api/
WOLFRAM_ID = os.environ.get("WOLFRAM_ID", None)

# Zipfile module
ZIP_DOWNLOAD_DIRECTORY = os.environ.get("ZIP_DOWNLOAD_DIRECTORY", "./zips")

# Genius Lyrics API
GENIUS = os.environ.get("GENIUS_ACCESS_TOKEN", None)

# Inline bot
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
BOT_USERNAME = os.environ.get("BOT_USERNAME", None)

# Genius Lyrics API
GENIUS = os.environ.get("GENIUS_ACCESS_TOKEN", None)
CMD_HELP = {}

# IMG Stuff
IMG_LIMIT = os.environ.get("IMG_LIMIT", None)

# JustWatch Country
WATCH_COUNTRY = os.environ.get("WATCH_COUNTRY", None)

# Custom Alive Header
HEADER = os.environ.get("HEADER", "Userbot is alive with status:")

# Jokes alive
JOKES = os.environ.get("JOKES", None)

# Image for alive
IMG = os.environ.get(
    "IMG",
    "https://telegra.ph/file/2a7b0bd8547a80c019493.jpg")

# Set default timezone
TZ = os.environ.get("TZ", "Asia/Jakarta")
time.tzset()

# Uptobox
USR_TOKEN = os.environ.get("USR_TOKEN_UPTOBOX", None)

# Kang pack name
NAMEPACK = os.environ.get("NAMEPACK", None)

# Bot version
BOT_VERSION = "DCLXVI-Slav01"

# Setting Up CloudMail.ru and MEGA.nz extractor binaries,
# and giving them correct perms to work properly.


def migration_workaround():
    try:
        from userbot.modules.sql_helper.globals import addgvar, delgvar, gvarstatus
    except BaseException:
        return None

    old_ip = gvarstatus("public_ip")
    new_ip = get("https://api.ipify.org").text

    if old_ip is None:
        delgvar("public_ip")
        addgvar("public_ip", new_ip)
        return None

    if old_ip == new_ip:
        return None

    sleep_time = 60
    LOGS.info(
        f"A change in IP address is detected, waiting for {sleep_time / 60} minutes before starting the bot."
    )
    sleep(sleep_time)
    LOGS.info("Starting bot...")

    delgvar("public_ip")
    addgvar("public_ip", new_ip)
    return None


if HEROKU_APP_NAME is not None and HEROKU_API_KEY is not None:
    migration_workaround()


# 'bot' variable
if STRING_SESSION:
    # pylint: disable=invalid-name
    bot = TelegramClient(
        StringSession(STRING_SESSION),
        API_KEY,
        API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
    )
else:
    # pylint: disable=invalid-name
    bot = TelegramClient("userbot", API_KEY, API_HASH)


async def check_botlog_chatid():
    if not BOTLOG_CHATID and LOGSPAMMER or not BOTLOG_CHATID and BOTLOG:
        LOGS.info(
            "You must set up the BOTLOG_CHATID variable in the config.env or environment variables, for the private error log storage to work."
        )
        quit(1)

    elif not (BOTLOG and LOGSPAMMER):
        return

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.info(
            "Your account doesn't have rights to send messages to BOTLOG_CHATID "
            "group. Check if you typed the Chat ID correctly.")
        quit(1)


with bot:
    try:
        bot(JoinChannelRequest("@akmjfeels"))
        bot(JoinChannelRequest("@GengKapak"))

        tgbot = TelegramClient(
            "TG_BOT_TOKEN",
            api_id=API_KEY,
            api_hash=API_HASH).start(
            bot_token=BOT_TOKEN)

        dugmeler = CMD_HELP
        me = bot.get_me()
        uid = me.id

        @tgbot.on(events.NewMessage(pattern="/start"))
        async def handler(event):
            if event.message.sender_id != uid:
                await event.reply(
                    f"Sylvia UserBot by `@MaximumSlav`! (`@{me.username}`) I am here to help you."
                )
            else:
                await event.reply("`I work for you :) I love you. ❤️`")

        @tgbot.on(events.InlineQuery)  # pylint:disable=E0602
        async def inline_handler(event):
            builder = event.builder
            result = None
            query = event.text
            if event.query.user_id == uid and query.startswith("@GengKapak"):
                buttons = paginate_help(0, dugmeler, "helpme")
                result = builder.article(
                    "Please Use Only With .help Command",
                    text="{}\nTotal loaded modules: {}".format(
                        "Sylvia UserBot by @MaximumSlav\n\nGitHub Repository [Here](https://github.com/AnggaR96s/Sylvia)\n",
                        len(dugmeler),
                    ),
                    buttons=buttons,
                    link_preview=False,
                )
            elif query.startswith("tb_btn"):
                result = builder.article(
                    "© @GengKapak",
                    text="@GengKapak",
                    buttons=[],
                    link_preview=True)
            else:
                result = builder.article(
                    "© @GengKapak",
                    text="""@GengKapak is for you!
You can convert your account to bot and use them. Remember, you can't manage someone else's bot! All installation details are explained from GitHub address below.""",
                    buttons=[
                        [
                            custom.Button.url(
                                "Follow Channel",
                                "https://t.me/GengKapak"),
                            custom.Button.url(
                                "Build by",
                                "https://t.me/MaximumSlav"),
                        ],
                        [
                            custom.Button.url(
                                "GitHub",
                                "https://github.com/AnggaR96s/Sylvia")],
                    ],
                    link_preview=False,
                )
            await event.answer([result] if result else None)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"helpme_next\((.+?)\)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                current_page_number = int(
                    event.data_match.group(1).decode("UTF-8"))
                buttons = paginate_help(
                    current_page_number + 1, dugmeler, "helpme")
                # https://t.me/TelethonChat/115200
                await event.edit(buttons=buttons)
            else:
                reply_pop_up_alert = "Please make for yourself, don't use my bot!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"helpme_prev\((.+?)\)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                current_page_number = int(
                    event.data_match.group(1).decode("UTF-8"))
                buttons = paginate_help(
                    current_page_number - 1, dugmeler, "helpme"  # pylint:disable=E0602
                )
                # https://t.me/TelethonChat/115200
                await event.edit(buttons=buttons)
            else:
                reply_pop_up_alert = "Please make for yourself, don't use my bot!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(b"ub_modul_(.*)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                modul_name = event.data_match.group(1).decode("UTF-8")

                cmdhel = str(CMD_HELP[modul_name])
                if len(cmdhel) > 150:
                    help_string = (
                        str(CMD_HELP[modul_name])[:150]
                        + "\n\nRead more .help "
                        + modul_name
                        + " "
                    )
                else:
                    help_string = str(CMD_HELP[modul_name])

                reply_pop_up_alert = (
                    help_string
                    if help_string is not None
                    else "{} No document has been written for module.".format(
                        modul_name
                    )
                )
            else:
                reply_pop_up_alert = "Please make for yourself, don't use my bot!"

            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    except BaseException:
        LOGS.info(
            "Support for inline is disabled on your bot. "
            "To enable it, define a bot token and enable inline mode on your bot. "
            "If you think there is a problem other than this, contact us.")

    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except BaseException:
        LOGS.info(
            "ERROR: The BOTLOG_CHATID variable entered is not valid. "
            "Please check the value you entered. "
            "Bot is crashed .."
        )
        quit(1)


async def update_restart_msg(chat_id, msg_id):
    DEFAULTUSER = ALIVE_NAME or "Set `ALIVE_NAME` ConfigVar!"
    message = (
        f"**UserBot v{BOT_VERSION} is back up and running!**\n\n"
        f"**Telethon:** {version.__version__}\n"
        f"**Python:** {python_version()}\n"
        f"**User:** {DEFAULTUSER}"
    )
    await bot.edit_message(chat_id, msg_id, message)
    return True


try:
    from userbot.modules.sql_helper.globals import delgvar, gvarstatus

    chat_id, msg_id = gvarstatus("restartstatus").split("\n")
    with bot:
        try:
            bot.loop.run_until_complete(
                update_restart_msg(
                    int(chat_id), int(msg_id)))
        except BaseException:
            pass
    delgvar("restartstatus")
except AttributeError:
    pass

# Global Variables
COUNT_MSG = 0
USERS = {}
BRAIN_CHECKER = []
BLACKLIST = []
COUNT_PM = {}
LASTMSG = {}
ENABLE_KILLME = True
ISAFK = False
AFKREASON = None
