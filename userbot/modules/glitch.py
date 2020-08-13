import asyncio
import os
import shlex
from os.path import basename
from typing import Optional, Tuple

from glitch_this import ImageGlitcher
from PIL import Image

from userbot import CMD_HELP, LOGS, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.(glg|gls)(?: |$)(.*)")
async def glitch(cat):
    await cat.edit("`Glitching... 😁`")
    cmd = cat.pattern_match.group(1)
    catinput = cat.pattern_match.group(2)
    reply = await cat.get_reply_message()
    if not (reply and (reply.media)):
        await cat.edit("`Media not found...`")
        return
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    catid = cat.reply_to_msg_id
    catsticker = await reply.download_media(file="./temp/")
    if not catsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg")):
        os.remove(catsticker)
        await cat.edit("`Media not found...`")
        return
    os.path.join("./temp/", "glitch.png")
    if catinput:
        if not catinput.isdigit():
            await cat.edit("`You input is invalid, check help`")
            return
        catinput = int(catinput)
        if not 0 < catinput < 9:
            await cat.edit("`Invalid Range...`")
            return
    else:
        catinput = 2
    if catsticker.endswith(".tgs"):
        catfile = os.path.join("./temp/", "glitch.png")
        catcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {catsticker} {catfile}"
        )
        stdout, stderr = (await runcmd(catcmd))[:2]
        if not os.path.lexists(catfile):
            await cat.edit("`File not found...`")
            LOGS.info(stdout + stderr)
        glitch_file = catfile
    elif catsticker.endswith(".webp"):
        catfile = os.path.join("./temp/", "glitch.png")
        os.rename(catsticker, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("`File not found... `")
            return
        glitch_file = catfile
    elif catsticker.endswith(".mp4"):
        catfile = os.path.join("./temp/", "glitch.png")
        await take_screen_shot(catsticker, 0, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("`Files not found...`")
            return
        glitch_file = catfile
    else:
        glitch_file = catsticker
    glitcher = ImageGlitcher()
    img = Image.open(glitch_file)
    if cmd == "gls":
        glitched = "./temp/" + "glitched.webp"
        glitch_img = glitcher.glitch_image(img, catinput, color_offset=True)
        glitch_img.save(glitched)
        await bot.send_file(cat.chat_id, glitched, reply_to_message_id=catid)
        os.remove(glitched)
        await cat.delete()
    elif cmd == "glg":
        Glitched = "./temp/" + "glitch.gif"
        glitch_img = glitcher.glitch_image(
            img, catinput, color_offset=True, gif=True)
        DURATION = 200
        LOOP = 0
        glitch_img[0].save(
            Glitched,
            format="GIF",
            append_images=glitch_img[1:],
            save_all=True,
            duration=DURATION,
            loop=LOOP,
        )
        await bot.send_file(cat.chat_id, Glitched, reply_to_message_id=catid)
        os.remove(Glitched)
        await cat.delete()
    for files in (catsticker, glitch_file):
        if files and os.path.exists(files):
            os.remove(files)


async def take_screen_shot(
    video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    print(
        "[[[Extracting a frame from %s ||| Video duration => %s]]]",
        video_file,
        duration,
    )
    ttl = duration // 2
    thumb_image_path = path or os.path.join(
        "./temp/", f"{basename(video_file)}.jpg")
    command = f"ffmpeg -ss {ttl} -i '{video_file}' -vframes 1 '{thumb_image_path}'"
    err = (await runcmd(command))[1]
    if err:
        print(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


CMD_HELP.update(
    {
        "glitch": ">`.glg` <range> as reply to mediafile."
        "\nUsage: Glitches the given mediafile (gif, stickers, image, videos) to a gif and glitch range is from 1 to 8. If nothing is mentioned then by default it is 2"
        "\n\n>`.gls` <range> as reply to media file."
        "\nUsage: Glitches the given mediafile (gif, stickers, image, videos) to a sticker and glitch range is from 1 to 8. If nothing is mentioned then by default it is 2"
    }
)
