import asyncio
import os
import shlex
from os import getcwd
from os.path import basename, join
from textwrap import wrap
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFont
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image as catimage

from userbot import CMD_HELP, LOGS, bot
from userbot.events import register
from userbot.modules import memify as tempmemes

MARGINS = [50, 150, 250, 350, 450]


def get_warp_length(width):
    return int((20.0 / 1024.0) * (width + 0.0))


async def cat_meme(topString, bottomString, filename, endname):
    img = Image.open(filename)
    imageSize = img.size
    # find biggest font size that works
    fontSize = int(imageSize[1] / 9)
    font = ImageFont.truetype("userbot/utils/impact.ttf", fontSize)
    topTextSize = font.getsize(topString)
    bottomTextSize = font.getsize(bottomString)
    while topTextSize[0] > imageSize[0] - \
            20 or bottomTextSize[0] > imageSize[0] - 20:
        fontSize = fontSize - 1
        font = ImageFont.truetype(
            "userbot/utils/impact.ttf", fontSize)
        topTextSize = font.getsize(topString)
        bottomTextSize = font.getsize(bottomString)

    # find top centered position for top text
    topTextPositionX = (imageSize[0] / 2) - (topTextSize[0] / 2)
    topTextPositionY = 0
    topTextPosition = (topTextPositionX, topTextPositionY)

    # find bottom centered position for bottom text
    bottomTextPositionX = (imageSize[0] / 2) - (bottomTextSize[0] / 2)
    bottomTextPositionY = imageSize[1] - bottomTextSize[1]
    bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)
    draw = ImageDraw.Draw(img)
    # draw outlines
    # there may be a better way
    outlineRange = int(fontSize / 15)
    for x in range(-outlineRange, outlineRange + 1):
        for y in range(-outlineRange, outlineRange + 1):
            draw.text(
                (topTextPosition[0] + x, topTextPosition[1] + y),
                topString,
                (0, 0, 0),
                font=font,
            )
            draw.text(
                (bottomTextPosition[0] + x, bottomTextPosition[1] + y),
                bottomString,
                (0, 0, 0),
                font=font,
            )
    draw.text(topTextPosition, topString, (255, 255, 255), font=font)
    draw.text(bottomTextPosition, bottomString, (255, 255, 255), font=font)
    img.save(endname)


async def cat_meeme(upper_text, lower_text, picture_name, endname):
    main_image = catimage(filename=picture_name)
    main_image.resize(1024, int(
        ((main_image.height * 1.0) / (main_image.width * 1.0)) * 1024.0))
    upper_text = "\n".join(
        wrap(
            upper_text,
            get_warp_length(
                main_image.width))).upper()
    lower_text = "\n".join(
        wrap(
            lower_text,
            get_warp_length(
                main_image.width))).upper()
    lower_margin = MARGINS[lower_text.count("\n")]
    text_draw = Drawing()
    text_draw.font = join(getcwd(), "userbot/utils/impact.ttf")
    text_draw.font_size = 100
    text_draw.text_alignment = "center"
    text_draw.stroke_color = Color("black")
    text_draw.stroke_width = 3
    text_draw.fill_color = Color("white")
    if upper_text:
        text_draw.text((main_image.width) // 2, 80, upper_text)
    if lower_text:
        text_draw.text(
            (main_image.width) // 2,
            main_image.height - lower_margin,
            lower_text)
    text_draw(main_image)
    main_image.save(filename=endname)


def convert_toimage(image):
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    os.remove(image)
    return "temp.jpg"


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


@register(outgoing=True, pattern=r"^\.(mmf|mms) ?(.*)")
async def memes(cat):
    cmd = cat.pattern_match.group(1)
    catinput = cat.pattern_match.group(2).upper()
    reply = await cat.get_reply_message()
    catid = cat.reply_to_msg_id
    if not (reply and (reply.media)):
        await cat.edit("`Reply to supported Media...`")
        return
    if catinput:
        if ";" in catinput:
            top, bottom = catinput.split(";", 1)
        else:
            top = catinput
            bottom = ""
    else:
        await cat.edit("```What should i write on that u idiot give some text```")
        return
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    cat = await cat.edit("`Downloading media......`")

    await asyncio.sleep(2)
    catsticker = await reply.download_media(file="./temp/")
    if not catsticker.endswith(
            (".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(catsticker)
        await cat.edit("```Supported Media not found...```")
        return

    if catsticker.endswith(".tgs"):
        await cat.edit(
            "```Transfiguration Time! Mwahaha memifying this animated sticker! (」ﾟﾛﾟ)｣```"
        )
        catfile = os.path.join("./temp/", "meme.png")
        catcmd = (
            f"lottie_convert.py --frame 0 -if lottie -of png {catsticker} {catfile}"
        )
        stdout, stderr = (await runcmd(catcmd))[:2]
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found...`")
            LOGS.info(stdout + stderr)
        meme_file = catfile
    elif catsticker.endswith(".webp"):
        await cat.edit(
            "```Transfiguration Time! Mwahaha memifying this sticker! (」ﾟﾛﾟ)｣```"
        )
        catfile = os.path.join("./temp/", "memes.jpg")
        os.rename(catsticker, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("`Template not found... `")
            return
        meme_file = catfile
    elif catsticker.endswith((".mp4", ".mov")):
        await cat.edit(
            "```Transfiguration Time! Mwahaha memifying this video! (」ﾟﾛﾟ)｣```"
        )
        catfile = os.path.join("./temp/", "memes.jpg")
        await take_screen_shot(catsticker, 0, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("```Template not found...```")
            return
        meme_file = catfile
    else:
        await cat.edit(
            "```Transfiguration Time! Mwahaha memifying this image! (」ﾟﾛﾟ)｣```"
        )
        meme_file = catsticker
    meme_file = convert_toimage(meme_file)
    if cmd == "mmf":
        meme = "catmeme.jpg"
        if max(len(top), len(bottom)) < 21:
            await tempmemes.cat_meme(top, bottom, meme_file, meme)
        else:
            await tempmemes.cat_meeme(top, bottom, meme_file, meme)
        await bot.send_file(cat.chat_id, meme, reply_to=catid)
    elif cmd == "mms":
        meme = "catmeme.webp"
        if max(len(top), len(bottom)) < 21:
            await tempmemes.cat_meme(top, bottom, meme_file, meme)
        else:
            await tempmemes.cat_meeme(top, bottom, meme_file, meme)
        await bot.send_file(cat.chat_id, meme, reply_to=catid)
    await cat.delete()
    os.remove(meme)
    for files in (catsticker, meme_file):
        if files and os.path.exists(files):
            os.remove(files)


CMD_HELP.update(
    {
        "memify": "Plugin : `memify`\
    \n\n>`.mmf toptext ; bottomtext`\
    \nUsage : Creates a image meme with give text at specific locations and sends\
    \n\n>`.mms toptext ; bottomtext`\
    \nUsage : Creates a sticker meme with give text at specific locations and sends\
    "
    }
)
