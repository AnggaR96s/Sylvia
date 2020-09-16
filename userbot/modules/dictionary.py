from PyDictionary import PyDictionary

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.dict (.*)")
async def dict(event):
    word = event.pattern_match.group(1)
    dictionary = PyDictionary()
    cmd = dictionary.meaning(word)
    output = f"**Word:** __{word}__\n\n"
    try:
        for a, b in cmd.items():
            output += f"**{a}**\n"
            for i in b:
                output += f"☞ __{i}__\n"
        await event.edit(output)
    except Exception:
        await event.edit(f"Couldn't fetch meaning of {word}")


CMD_HELP.update(
    {
        "dictionary": "**Plugin :** `dictionary`\
    \n\n>`.dict query`\
    \nUsage: Fetches meaning of the given word\
    "
    }
)
