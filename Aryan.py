import aiohttp, aiofiles, asyncio, base64, logging
import os, platform, random, re, socket
import sys, time, textwrap, yt_dlp

from os import getenv
from io import BytesIO
from time import strftime
from functools import partial
from dotenv import load_dotenv
from datetime import datetime
from typing import Union, List, Pattern
from logging.handlers import RotatingFileHandler

from pyrogram import Client, filters
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_async_

from pyrogram import Client, filters as pyrofl
from pytgcalls import PyTgCalls, filters as pytgfl


from pyrogram import idle, __version__ as pyro_version
from pytgcalls.__version__ import __version__ as pytgcalls_version

from ntgcalls import TelegramServerError
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import (
    ChatAdminRequired,
    FloodWait,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pytgcalls.exceptions import NoActiveGroupCall
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls.types import ChatUpdate, Update, GroupCallConfig
from pytgcalls.types import Call, MediaStream, AudioQuality, VideoQuality

from PIL import Image, ImageDraw, ImageEnhance
from PIL import ImageFilter, ImageFont, ImageOps
from youtubesearchpython.__future__ import VideosSearch


loop = asyncio.get_event_loop()


# versions dictionary
__version__ = {
    "AP": "1.0.0 Mini",
    "Python": platform.python_version(),
    "Pyrogram": pyro_version,
    "PyTgCalls": pytgcalls_version,
}


# store all logs
logging.basicConfig(
    format="[%(name)s]:: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    handlers=[
        RotatingFileHandler("logs.txt", maxBytes=(1024 * 1024 * 5), backupCount=10),
        logging.StreamHandler(),
    ],
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)

LOGGER = logging.getLogger("SYSTEM")


# config variables
if os.path.exists("Config.env"):
    load_dotenv("Config.env")

API_ID = int(getenv("14050586", 0))
API_HASH = getenv("42a60d9c657b106370c79bb0a8ac560c", None)
BOT_TOKEN = getenv("BOT_TOKEN", None)
STRING_SESSION = getenv("BQDWZRoAc1PhtwD3mMkFN9NDLtj9D90FZsuxiB-YhxdgRwOpAYdyBJCXjT655LNPxRNBZRUnYn3fD77NdqYgdBKA3Ic7qNvzQn7aLB0tVu-3Beb599TIOqvFEhlyO96r1WZFrk7EekYzpM-RYrtu5K6o9SWFF-u8w4xC1j2mIZtZglOx4DCaae2aa1cFLFGle3RK63fcNm8KmNFHnoJIMmX32mU2bH7patjYr3-IA9XpYgHGNVeDhN2mWwN2N0_i2ngdCZTwhLHg0ASAjzUMIKRIcGX1bK0z9MmQj4bOT0Ptu1UyrvfvQVQA1jhJjHmff_q7Lh1rzRkK_oQPZ7cauDz9omnyWQAAAAHMk1gFAQ", None)
MONGO_DB_URL = getenv("MONGO_DB_URL", "mongodb+srv://Krishna:pss968048@cluster0.4rfuzro.mongodb.net/?retryWrites=true&w=majority")
OWNER_ID = int(getenv("OWNER_ID", "1839567584"))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID","-1002380431147"))
START_IMAGE_URL = getenv("START_IMAGE_URL","https://t.me/MasterMindBots/121")


# Memory Database

ACTIVE_AUDIO_CHATS = []
ACTIVE_VIDEO_CHATS = []
ACTIVE_MEDIA_CHATS = []

QUEUE = {}


# Command & Callback Handlers


def cdx(commands: Union[str, List[str]]):
    return pyrofl.command(commands, ["/", "!", "."])


def cdz(commands: Union[str, List[str]]):
    return pyrofl.command(commands, ["", "/", "!", "."])


def rgx(pattern: Union[str, Pattern]):
    return pyrofl.regex(pattern)


bot_owner_only = pyrofl.user(OWNER_ID)


# all clients

app = Client(
    name="App",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=str(STRING_SESSION),
)

bot = Client(
    name="Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

call = PyTgCalls(app)
call_config = GroupCallConfig(auto_start=False)

mongo_async_cli = _mongo_async_(MONGO_DB_URL)
mongodb = mongo_async_cli.adityaxdb

# store start time
__start_time__ = time.time()


# start and run


async def main():
    LOGGER.info("🐬 Updating Directories ...")
    if "cache" not in os.listdir():
        os.mkdir("cache")
    if "cookies.txt" not in os.listdir():
        LOGGER.info("⚠️ 'cookies.txt' - Not Found❗")
        sys.exit()
    if "downloads" not in os.listdir():
        os.mkdir("downloads")
    for file in os.listdir():
        if file.endswith(".session"):
            os.remove(file)
    for file in os.listdir():
        if file.endswith(".session-journal"):
            os.remove(file)
    LOGGER.info("✅ All Directories Updated.")
    await asyncio.sleep(1)
    LOGGER.info("🌐 Checking Required Variables ...")
    if API_ID == 0:
        LOGGER.info("❌ 'API_ID' - Not Found ‼️")
        sys.exit()
    if not API_HASH:
        LOGGER.info("❌ 'API_HASH' - Not Found ‼️")
        sys.exit()
    if not BOT_TOKEN:
        LOGGER.info("❌ 'BOT_TOKEN' - Not Found ‼️")
        sys.exit()
    if not STRING_SESSION:
        LOGGER.info("❌ 'STRING_SESSION' - Not Found ‼️")
        sys.exit()

    if not MONGO_DB_URL:
        LOGGER.info("'MONGO_DB_URL' - Not Found !!")
        sys.exit()
    try:
        await mongo_async_cli.admin.command('ping')
    except Exception:
        LOGGER.info("❌ 'MONGO_DB_URL' - Not Valid !!")
        sys.exit()
    LOGGER.info("✅ Required Variables Are Collected.")
    await asyncio.sleep(1)
    LOGGER.info("🌀 Starting All Clients ...")
    try:
        await bot.start()
    except Exception as e:
        LOGGER.info(f"🚫 Bot Error: {e}")
        sys.exit()
    if LOG_GROUP_ID != 0:
        try:
            await bot.send_message(LOG_GROUP_ID, "**🤖 Bot Started.**")
        except Exception:
            pass
    LOGGER.info("✅ Bot Started.")
    try:
        await app.start()
    except Exception as e:
        LOGGER.info(f"🚫 Assistant Error: {e}")
        sys.exit()
    try:
        await app.join_chat("https://t.me/+gV4wCWz0wEtmZTY1")
        await app.join_chat("aryan_misic_bot_chat")
    except Exception:
        pass
    if LOG_GROUP_ID != 0:
        try:
            await app.send_message(LOG_GROUP_ID, "**🦋 Assistant Started.**")
        except Exception:
            pass
    LOGGER.info("✅ Assistant Started.")
    try:
        await call.start()
    except Exception as e:
        LOGGER.info(f"🚫 PyTgCalls Error: {e}")
        sys.exit()
    LOGGER.info("✅ PyTgCalls Started.")
    await asyncio.sleep(1)
    LOGGER.info("✅ Sucessfully Hosted Your Bot !!")
    LOGGER.info("✅ Now Do Visit: https://t.me/+gV4wCWz0wEtmZTY1 !!")
    await idle()









# Some Required Functions ...!!


def _netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    s.close()


async def paste_queue(content):
    loop = asyncio.get_running_loop()
    link = await loop.run_in_executor(None, partial(_netcat, "ezup.dev", 9999, content))
    return link



def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time





# Mongo Database Functions

chatsdb = mongodb.chatsdb
usersdb = mongodb.usersdb




# Served Chats

async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def get_served_chats() -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})



# Served Users

async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list


async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})







#lnolo#





# Callback & Message Queries
@bot.on_message(pyrofl.command(["start", "help"]) & pyrofl.private)
async def start_message_private(client, message):
    user_id = message.from_user.id
    mention = message.from_user.mention
    await add_served_user(user_id)  # Ensure this function exists

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name.startswith("verify"):
            pass  # Handle verification if needed
    else:
        baby = await message.reply_text("[□□□□□□□□□□] 0%")
        progress = [
            "[■□□□□□□□□□] 10%",
            "[■■□□□□□□□□] 20%",
            "[■■■□□□□□□□] 30%",
            "[■■■■□□□□□□] 40%",
            "[■■■■■□□□□□] 50%",
            "[■■■■■■□□□□] 60%",
            "[■■■■■■■□□□] 70%",
            "[■■■■■■■■□□] 80%",
            "[■■■■■■■■■□] 90%",
            "[■■■■■■■■■■] 100%"
        ]
        for step in progress:
            await baby.edit_text(f"**{step}**")
            await asyncio.sleep(0.2)

        await baby.edit_text("**❖ Jᴀʏ sʜʀᴇᴇ ʀᴀᴍ 🚩...**")
        await asyncio.sleep(2)
        await baby.delete()

        caption = f"""**┌────── ˹ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ˼──────•
┆◍ ʜᴇʏ {mention},
└──────────────────────•
» ✦ ϻσsᴛ ᴘσᴡєꝛғυʟʟ ϻυsɪᴄ ʙσᴛ  
» ✦ ʙєsᴛ ғєᴧᴛυꝛє ʙσᴛ ση ᴛєʟєɢꝛᴧϻ 
» ✦ ᴧᴅᴅ ϻє ɢꝛσυᴘ ᴛσ sєє ϻʏ ᴘσᴡєʀ
•──────────────────────•
❖ 𝐏ᴏᴡᴇʀᴇᴅ ʙʏ  :-  [Aryan ʙσᴛ ](https://t.me/+gV4wCWz0wEtmZTY1)❤️‍🔥
•──────────────────────•**"""

        buttons = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="❖ ᴛᴧᴘ тᴏ sᴇᴇ ᴍᴧɪᴄ ❖",
                        url=f"https://t.me/{bot.me.username}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="˹ ❍ᴡɴᴇꝛ ˼",
                        user_id=OWNER_ID,
                    ),
                    InlineKeyboardButton(
                        text="˹ ᴍᴜsɪᴄ ˼",
                        callback_data="RISHU_RAJPUT",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="˹ ᴧʙᴏᴜᴛ ˼",
                        callback_data="RISHU",
                    )
            ]
        )

        # Ensure only one message is sent
        if START_IMAGE_URL:
            try:
                await message.reply_photo(
                    photo=START_IMAGE_URL, caption=caption, reply_markup=buttons
                )
                return  # Stop further execution if photo is sent
            except Exception as e:
                LOGGER.info(f"🚫 Start Image Error: {e}")

        # If photo fails or not available, send text message
        try:
            await message.reply_text(text=caption, reply_markup=buttons)
        except Exception as e:
            LOGGER.info(f"🚫 Start Error: {e}")


#my backloli #

CBUTTON = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("˹ sᴜᴘᴘᴏꝛᴛ ˼", url="https://t.me/aryan_misic_bot_chat")
        ],
        [
            InlineKeyboardButton("˹ ᴜᴘᴅᴧᴛᴇ ˼", url="https://t.me/+gV4wCWz0wEtmZTY1"),
            InlineKeyboardButton("˹ ᴧʟʟ ʙᴏᴛ ˼", url="https://t.me/+qDKFOaG48MQ3NTRl")
        ],
        [
            InlineKeyboardButton("↺ ʙᴧᴄᴋ ↻", callback_data="back_to_home")
        ]
    ]
)


# Define ABUTTON outside of the HELP_X string
ABUTTON = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("↺ ʙᴧᴄᴋ ↻", callback_data="back_to_home")
        ]
    ]
)

HELP_C = """```
⌬ ๏ ʟᴇᴛ's ɪɴᴛʀᴏᴅᴜᴄᴇ ᴍᴜsɪᴄ ʙᴏᴛ```

**⌬ [【 Aryan-ϻυsɪᴄ 】](https://t.me/+gV4wCWz0wEtmZTY1) ɪs ᴏɴᴇ ᴏғ ᴛʜᴇ ʙᴇsᴛ ᴍᴜsɪᴄ | ᴠɪᴅᴇᴏ sᴛꝛᴇᴀᴍɪɴɢ ʙᴏᴛ ᴏɴ ᴛᴇʟᴇɢꝛᴧᴍ ғᴏꝛ ʏᴏᴜꝛ ɢꝛᴏᴜᴘs ᴀɴᴅ ᴄʜᴧɴɴᴇʟ**
```\n⌬ ʙᴇsᴛ ғᴇᴀsɪʙɪʟɪᴛʏ ᴏɴ ᴛᴏᴘ  ?```

**✦ ʙᴇsᴛ sᴏᴜɴᴅ ǫᴜᴀʟɪᴛʏ
✦ ɴᴏ ᴘꝛᴏᴍᴏᴛɪᴏɴᴧʟ ᴧᴅs | ʜɪɢʜ ᴜᴘ-ᴛɪᴍᴇ 
✦ ʜɪɢʜ ɪɴғꝛᴧsᴛꝛᴜᴄᴛᴜꝛᴇ sᴇꝛᴠᴇꝛ
✦ ꝛᴇ-ᴇᴅɪᴛᴇᴅ ᴄᴏꝛᴇ | ʜɪɢʜʟʏ ᴏᴘᴛɪᴍɪsᴇ
✦ ɴᴏ ᴍᴏꝛᴇ ʟᴧɢ ᴀɴᴅ ᴅᴏᴡɴ-ᴛɪᴍᴇ
✦ ᴍᴀɴʏ ᴍᴏʀᴇ ғᴇᴀᴛᴜʀᴇs........

ᴀʟʟ ᴛʜᴇ ғᴇᴀᴛᴜʀᴇs ᴀʀᴇ ᴡᴏʀᴋɪɴɢ ғɪɴᴇ

⌬ ᴍᴏʀᴇ ɪɴғᴏ. [ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ](https://t.me/+gV4wCWz0wEtmZTY1)**"""

HELP_X = """```
    【 Aryan-ϻυsɪᴄ 】 ᴍᴇɴᴜ```

**ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : /

✦ /play - Pʟᴀʏ ʏᴏᴜʀ ғᴀᴠᴏʀɪᴛᴇ sᴏɴɢ [ᴀᴜɪᴅᴏ].

✦ /vplay - Pʟᴀʏ ʏᴏᴜʀ ғᴀᴠᴏʀɪᴛᴇ sᴏɴɢ [ᴠɪᴅᴇᴏ].

✦ /pause - Sᴛᴏᴘ sᴏɴɢ[ᴀᴜɪᴅᴏ & ᴠɪᴅᴇᴏ].

✦ /resume - Cᴏɴᴛɪɴᴜᴇ ᴘʟᴀʏ sᴏɴɢ [ᴀᴜɪᴅᴏ & ᴠɪᴅᴇᴏ]

✦ /skip - Sᴋɪᴘ sᴏɴɢ [ᴀᴜɪᴅᴏ & ᴠɪᴅᴇᴏ]

✦ /end - Cʟᴇᴀʀ , ᴇɴᴅ ᴀʟʟ sᴏɴɢ [ᴀᴜɪᴅᴏ & ᴠɪᴅᴇᴏ]

❖ 𝐏ᴏᴡᴇʀᴇᴅ ʙʏ - [Aryan ʙσᴛ](https://t.me/+gV4wCWz0wEtmZTY1)**"""

# Callback query handler
@bot.on_callback_query(filters.regex("RISHU_RAJPUT"))
async def helper_cb(client, CallbackQuery):
    await CallbackQuery.edit_message_text(HELP_X, reply_markup=ABUTTON)
    
    
        
@bot.on_callback_query(filters.regex("RISHU"))
async def helper_cb(client, CallbackQuery):
    await CallbackQuery.edit_message_text(HELP_C, reply_markup=CBUTTON)





   


@bot.on_callback_query(rgx("force_close"))
async def delete_cb_query(client, query):
    try:
        return await query.message.delete()
    except Exception:
        return

@bot.on_callback_query(filters.regex("back_to_home"))
async def back_to_home_menu(client, query):
    mention = query.from_user.mention
    caption = f"""**┌────── ˹ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ˼──────•\n┆◍ ʜᴇʏ {mention},\n└──────────────────────•\n» ✦ ϻσsᴛ ᴘσᴡєꝛғυʟʟ ϻυsɪᴄ ʙσᴛ  \n» ✦ ʙєsᴛ ғєᴧᴛυꝛє ʙσᴛ ση ᴛєʟєɢꝛᴧϻ \n» ✦ ᴧᴅᴅ ϻє ɢꝛσυᴘ ᴛσ sєє ϻʏ ᴘσᴡєꝛ\n•──────────────────────•\n❖ 𝐏ᴏᴡᴇʀᴇᴅ ʙʏ  :-  [Aryan ʙσᴛ ](https://t.me/+gV4wCWz0wEtmZTY1)❤️‍🔥\n•──────────────────────•**"""

    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❖ ᴛᴧᴘ тᴏ sᴇᴇ ᴍᴧɪᴄ ❖",
                    url=f"https://t.me/{bot.me.username}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="˹ ❍ᴡɴᴇꝛ ˼",
                    user_id=OWNER_ID,  # Ensure OWNER_ID is defined or replace with actual ID
                ),
                InlineKeyboardButton(
                    text="˹ ᴍᴜsɪᴄ ˼",
                    callback_data="RISHU_RAJPUT",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="˹ ᴧʙᴏᴜᴛ ˼",
                    callback_data="RISHU",
                ),
            ]
        ]
    )
    try:
        return await query.edit_message_text(text=caption, reply_markup=buttons)
    except Exception as e:
        LOGGER.info(f"🚫 Back Menu Error: {e}")
        return
# Thumbnail Generator Area


async def download_thumbnail(vidid: str):
    async with aiohttp.ClientSession() as session:
        links = [
            f"https://i.ytimg.com/vi/{vidid}/maxresdefault.jpg",
            f"https://i.ytimg.com/vi/{vidid}/sddefault.jpg",
            f"https://i.ytimg.com/vi/{vidid}/hqdefault.jpg",
            START_IMAGE_URL,
        ]
        thumbnail = f"cache/temp_{vidid}.png"
        for url in links:
            async with session.get(url) as resp:
                if resp.status != 200:
                    continue
                else:
                    f = await aiofiles.open(thumbnail, mode="wb")
                    await f.write(await resp.read())
                    await f.close()
                    return thumbnail


async def get_user_logo(user_id):
    try:
        user_chat = await bot.get_chat(user_id)
        userimage = user_chat.photo.big_file_id
        user_logo = await bot.download_media(userimage, f"cache/{user_id}.png")
    except:
        user_chat = await bot.get_me()
        userimage = user_chat.photo.big_file_id
        user_logo = await bot.download_media(userimage, f"cache/{bot.id}.png")
    return user_logo


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


def circle_image(image, size):
    size = (size, size)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output


def random_color_generator():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


async def create_thumbnail(results, user_id):
    if not results:
        return START_IMAGE_URL
    title = results.get("title")
    title = re.sub("\W+", " ", title)
    title = title.title()
    vidid = results.get("id")
    duration = results.get("duration")
    views = results.get("views")
    channel = results.get("channel")
    image = await download_thumbnail(vidid)
    logo = await get_user_logo(user_id)
    image_string = "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
