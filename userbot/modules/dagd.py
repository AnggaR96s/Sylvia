import requests

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.dns (.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/dns/{}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit("DNS records of {} are \n{}".format(input_str, response_api))
    else:
        await event.edit("Can't seem to find {} on the internet".format(input_str))


@register(outgoing=True, pattern=r"^\.url (.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url={}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit("Generated: {}\nInput URL: {}".format(response_api, input_str))
    else:
        await event.edit("Something is wrong. please try again later.")


@register(outgoing=True, pattern=r"^\.unshort (.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    r = requests.get(input_str, allow_redirects=False)
    if str(r.status_code).startswith("3"):
        await event.edit(
            "Input URL: {}\nReDirected URL: {}".format(
                input_str, r.headers["Location"]
            ),
        )
    else:
        await event.edit(
            "Input URL {} returned status_code {}".format(input_str, r.status_code),
        )


CMD_HELP.update(
    {
        "dagd": ">`.dns link`\
    \nUsage: Shows you Domain Name System(dns) of the given link . example `.dns google.com` or `.dns github.com`\
    \n\n>`.url link`\
    \nUsage: Shortens the given link.\
    \n\n>`.unshort link`\
    \nUsage: Unshortens the given short link.\
    "
    }
)
