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
    request = requests.get(url)
    parsed = json.loads(request.text)

    acc = WALLET
    unc = parsed["data"]["unconfirmed_balance"]
    bal = acc = parsed["data"]["balance"]
    hs = parsed["data"]["hashrate"]

    result = (
        f"**Mining Status**:\n"
        f"**Wallet :** `{WALLET}`\n"
        f"**Unconfirmed :** `{unc} XMR`\n"
        f"**Balance :** `{bal} XMR`\n"
        f"**Hashrate :** `{hs} H/s`"
    )

    await nanopool.edit(result)


CMD_HELP.update(
    {
        "monero": ">`.xmr`\
        \nUsage: Gets mining status from nanopool."
    }
)
