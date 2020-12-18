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
    request = requests.get(url)
    parsed = json.loads(request.text)
    drequest = requests.get(durl)
    dparsed = json.loads(drequest.text)

    try:
        unc = parsed["data"]["unconfirmed_balance"]
        bal = parsed["data"]["balance"]
        hs = parsed["data"]["hashrate"]
        diff = dparsed["difficulty"]
        he = dparsed["height"]
    except KeyError:
        return await nanopool.edit("**Wallet not found or API error!!**")

    result = (
        f"**Mining Status**:\n"
        f"**Details :** [Nanopool](https://xmr.nanopool.org/account/{WALLET})\n"
        f"**Unconfirmed :** `{unc} XMR`\n"
        f"**Balance :** `{bal} XMR`\n"
        f"**Hashrate :** `{hs} H/s`\n\n"
        "**Coin Status :**\n"
        f"**Difficulty :** `{diff}\n`"
        f"**Height :** `{he}`")

    await nanopool.edit(result)


CMD_HELP.update(
    {
        "monero": ">`.xmr`\
        \nUsage: Gets mining status from nanopool."
    }
)
