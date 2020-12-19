import datetime as dt
import json

import requests

from userbot import CMD_HELP, WALLET
from userbot.events import register


@register(outgoing=True, pattern=r"^\.xmr$")
async def xmr(nanopool):
    await nanopool.edit("`Getting Information..`")
    if WALLET is None:
        await nanopool.edit("`Provide nanopool wallet address to Heroku ConfigVars...`")
        return False
    else:
        await nanopool.edit("`Processing..`")

    url = f"https://api.nanopool.org/v1/xmr/user/{WALLET}"
    durl = "https://localmonero.co/blocks/api/get_stats"
    purl = "https://min-api.cryptocompare.com/data/price?fsym=XMR&tsyms=IDR"
    wurl = f"https://api.nanopool.org/v1/xmr/payments/{WALLET}"
    request = requests.get(url)
    parsed = json.loads(request.text)
    drequest = requests.get(durl)
    dparsed = json.loads(drequest.text)
    prequest = requests.get(purl)
    pparsed = json.loads(prequest.text)
    wrequest = requests.get(wurl)
    wparsed = json.loads(wrequest.text)

    try:
        unc = parsed["data"]["unconfirmed_balance"]
        bal = parsed["data"]["balance"]
        hs = parsed["data"]["hashrate"]
        diff = dparsed["difficulty"]
        he = dparsed["height"]
        p = pparsed["IDR"]
        idr = float(p) * float(bal)
        d = wparsed["data"][0]["date"]
        dp = dt.datetime.fromtimestamp(int(d) / 1)
        tx = wparsed["data"][0]["txHash"]
        am = wparsed["data"][0]["amount"]
        cn = wparsed["data"][0]["confirmed"]

    except KeyError:
        return await nanopool.edit("**Wallet not found or API error!!**")

    result = (
        f"**Mining Status**:\n"
        f"**Details :** [Nanopool](https://xmr.nanopool.org/account/{WALLET})\n"
        f"**Hashrate :** `{hs} H/s`\n"
        f"**Unconfirmed :** `{unc} XMR`\n"
        f"**Balance Details :**\n"
        f"**XMR :** `{bal}\n`"
        f"**IDR :** `{idr}\n\n`"
        "**Latest Withdraw :**\n"
        f"**Date :** `{dp}`\n"
        f"**TxHash :** [Details](https://xmrchain.net/tx/{tx})\n"
        f"**Amount :** `{am} XMR`\n"
        f"**Confirmed :** `{cn}`\n\n"
        "**Coin Status :**\n"
        f"**XMR Price :** `{p} IDR`\n"
        f"**Difficulty :** `{diff}\n`"
        f"**Height :** `{he}`")

    await nanopool.edit(result)


CMD_HELP.update(
    {
        "monero": ">`.xmr`\
        \nUsage: Gets mining status from nanopool."
    }
)
