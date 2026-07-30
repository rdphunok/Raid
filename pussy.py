from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import asyncio
import logging
import sys
import time
import random
from difflib import get_close_matches
import edge_tts
import os

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

TOKENS = [
    "8666502260:AAG52YosLmCHkQvdY5_oSlpItsBy_zoiyjM",
    "8613761158:AAFi8xz7IumiRAgMTsRa2iAJAEpqgflY1bQ",
    "8994320628:AAFzf4YQvODJPngEqkPtbSAMIi3tisgE300",
    "8630777697:AAGojTI8wFR-ZONN-jKjjvwtlUepin_J0pk",
    "8616814880:AAEXTAzGoo2y_Nbg5yug7A-lJrXSBWCtxP0",
    "8070259728:AAEfdIZbcF-go6ZF8PC76noj77HjiAcM0Nw"
]
MASTER_TOKEN = TOKENS[0]
OWNER_ID = 7699820685
BOT_NAME = "SIREN V3"

sudo_users = set([OWNER_ID])
muted_users = set()

swipe_targets = {}
swipe_texts = {}
swipe_index = {}
cswipe_targets = {}
cswipe_texts = {}

raid_targets = set()
BURST_MODE = False
swipe_speed = 0.3
START_TIME = time.time()

roast_texts = [
    "You’re proof that natural selection is taking a break",
    "Your brain is like a browser with 100 tabs open... and all of them frozen",
    "Congrats on being the reason we have instruction manuals",
    "If common sense was currency, you’d be broke",
    "You have the energy of a phone at 1%",
    "I’d explain it to you but I left my crayons at home",
    "You’re the human equivalent of are you still watching?",
    "Your IQ is room temperature",
    "I’m not ignoring you, I’m just prioritizing my sanity",
    "You’re like a software update... nobody wants you but you keep showing up",
    "You bring new meaning to the word background character",
    "If you were a challenge, I’d skip you",
    "Congrats, you’re the reason the gene pool needs a lifeguard",
    "Your face is like a WiFi signal... 1 bar and people still connect",
    "I’m jealous of people who don’t know you",
    "You’re proof that even mistakes can walk and talk",
    "If you were a spice you’d be flour",
    "You have the charisma of a wet sock",
    "I’d agree with you but then we’d both be wrong",
    "You bring everyone so much joy... when you leave the room",
    "Your IQ is like a phone battery... dies fast",
    "I’m not ignoring you, I’m giving you time to realize how dumb that was",
    "You’re the human version of 404 error not found",
    "If brains were WiFi, you’d be on airplane mode",
    "You’re proof that evolution can take a day off",
    "If stupidity was a sport, you’d be Olympic champion",
    "Your brain has 2 settings: lag and crash",
    "You have the personality of a wet cardboard box",
    "You’re like WiFi… everyone sees you but no one wants to connect",
    "I’d roast you more but I don’t want to hurt your 2 brain cells",
    "You’re the human version of skip ad",
    "Your aura is like airplane mode... completely off"
]

raid_texts = [
    "𝗔𝗡𝗧𝗘𝗥 𝗠𝗔𝗡𝗧𝗘𝗥 𝗦𝗛𝗘𝗧𝗔𝗡𝗜 𝗞𝗛𝗢𝗣𝗗𝗔 < {target}> 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗔 𝗕𝗛𝗢𝗦𝗗𝗔 🪼⋆｡𖦹°🫧⋆.ೃ࿔*:･ --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------𝗔𝗡𝗧𝗘𝗥 𝗠𝗔𝗡𝗧𝗘𝗥 𝗦𝗛𝗘𝗧𝗔𝗡𝗜 𝗞𝗛𝗢𝗣𝗗𝗔  < {target}> 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗔 𝗕𝗛𝗢𝗦𝗗𝗔 🪼⋆｡𖦹°🫧⋆.ೃ࿔*:･",
    "𝗠𝗔𝗜 𝗣𝗜𝗧𝗔 𝗛𝗨𝗡 𝗣𝗔𝗡𝗜 < {target}> 𝗞𝗜 𝗠𝗔𝗔 𝗥𝗔𝗡𝗗𝗜𝗢𝗡 𝗞𝗜 𝗥𝗔𝗡𝗜 ˖°𓇼🌊⋆🐚🫧--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------𝗠𝗔𝗜 𝗣𝗜𝗧𝗔 𝗛𝗨𝗡 𝗣𝗔𝗡𝗜 < {target}> 𝗞𝗜 𝗠𝗔𝗔 𝗥𝗔𝗡𝗗𝗜𝗢𝗡 𝗞𝗜 𝗥𝗔𝗡𝗜 ˖°𓇼🌊⋆🐚🫧",
    "< {target} > ----------𝗢𝗬𝗘 𝗧𝗘𝗥𝗜 𝗥𝗔𝗡𝗗𝗜 𝗠𝗔𝗔 𝗞𝗢 𝗛𝗔𝗞𝗟𝗔 𝗞𝗘 𝗖𝗛𝗢𝗗𝗨 ‧₊˚🖇️✩ ₊˚🎧⊹♡--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------< {target} > ---------- 𝗢𝗬𝗘 𝗧𝗘𝗥𝗜 𝗥𝗔𝗡𝗗𝗜 𝗠𝗔𝗔 𝗞𝗢 𝗛𝗔𝗞𝗟𝗔 𝗞𝗘 𝗖𝗛𝗢𝗗𝗨 ‧₊˚🖇️✩ ₊˚🎧⊹♡",
    "< {target} > -----------  𝗢𝗬𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗣𝗘 𝗠𝗢𝗢𝗧 𝗗𝗨𝗡𝗚𝗔 🫧𓇼𓏲*ੈ✩‧₊˚🎐--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------< {target} > ----------   𝗢𝗬𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗜 𝗖𝗛𝗨𝗧 𝗣𝗘 𝗠𝗢𝗢𝗧 𝗗𝗨𝗡𝗚𝗔 🫧𓇼𓏲*ੈ✩‧₊˚🎐",
    "𝗔𝗖𝗛𝗔 𝗦𝗨𝗡 𝗧𝗢 < {target}> 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗢 𝗕𝗛𝗔𝗚𝗔 𝗕𝗛𝗔𝗚𝗔 𝗖𝗛𝗢𝗗𝗨 ‧₊˚ ☁️⋅♡🪐༘⋆--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------𝗔𝗖𝗛𝗔 𝗦𝗨𝗡 𝗧𝗢 < {target}> 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗢 𝗕𝗛𝗔𝗚𝗔 𝗕𝗛𝗔𝗚𝗔 𝗖𝗛𝗢𝗗𝗨 ‧₊˚ ☁️⋅♡🪐༘⋆",
    "< {target} > ---------- 𝗧𝗘𝗥𝗜 𝗕𝗛𝗘𝗡 𝗞𝗜 𝗧𝗔𝗡𝗚 𝗨𝗧𝗛𝗔 𝗞𝗘 𝗜𝗗𝗛𝗘𝗥 𝗨𝗗𝗛𝗘𝗥 𝗖𝗛𝗢𝗗𝗨𝗡𝗚𝗔 ༘⋆🌷🫧💭₊˚ෆ--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------< {target} > ----------- 𝗧𝗘𝗥𝗜 𝗕𝗛𝗘𝗡 𝗞𝗜 𝗧𝗔𝗡𝗚 𝗨𝗧𝗛𝗔 𝗞𝗘 𝗜𝗗𝗛𝗘𝗥 𝗨𝗗𝗛𝗘𝗥 𝗖𝗛𝗢𝗗𝗨𝗡𝗚𝗔 ༘⋆🌷🫧💭₊˚ෆ",
    "< {target} > ----------𝗧𝗘𝗥𝗜 𝗕𝗛𝗘𝗡 𝗞𝗢 𝗨𝗟𝗧𝗔 𝗞𝗥𝗞𝗘 𝗖𝗢𝗗 𝗗𝗨𝗡𝗚𝗔 𝗛𝗘𝗛𝗘 ✩°𓏲⋆🌿. ⋆⸜ 🍵✮˚--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------< {target} > ---------- 𝗧𝗘𝗥𝗜 𝗕𝗛𝗘𝗡 𝗞𝗢 𝗨𝗟𝗧𝗔 𝗞𝗥𝗞𝗘 𝗖𝗢𝗗 𝗗𝗨𝗡𝗚𝗔 𝗛𝗘𝗛𝗘 ✩°𓏲⋆🌿. ⋆⸜ 🍵✮˚",
    "< {target} > -----𝗞𝗨𝗧𝗧𝗜𝗬𝗔 𝗕𝗔𝗡𝗔 𝗞𝗜 𝗖𝗢𝗗𝗨 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗢 🧉❀🐚🐉︎ ࿔*:･ﾟ☾--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------< {target} > -----𝗞𝗨𝗧𝗧𝗜𝗬𝗔 𝗕𝗔𝗡𝗔 𝗞𝗜 𝗖𝗢𝗗𝗨 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗢 🧉❀🐚🐉︎ ࿔*:･ﾟ☾",
    "< {target} > 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗖𝗛𝗢𝗗𝗥𝗔 𝗧𝗛𝗔 𝗙𝗜𝗥 𝗨𝗦𝗡𝗘 𝗣𝗔𝗔𝗗 𝗠𝗔𝗥𝗗𝗜 𝗟𝗨𝗡𝗗 𝗣𝗘 😭💨.:**:.☆*.:｡.✿ --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------< {target} > 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗖𝗛𝗢𝗗𝗥𝗔 𝗧𝗛𝗔 𝗙𝗜𝗥 𝗨𝗦𝗡𝗘 𝗣𝗔𝗔𝗗 𝗠𝗔𝗥𝗗𝗜 𝗟𝗨𝗡𝗗 𝗣𝗘 😭💨.:**:.☆*.:｡.✿",
    "𝗖𝗛𝗟𝗧𝗜 𝗛𝗔𝗜 𝗚𝗔𝗗𝗜 𝗖𝗛𝗟𝗧𝗔 𝗛𝗔𝗜 𝗚𝗛𝗢𝗗𝗔 𝗗𝗔𝗟𝗗𝗨 𝗞𝗬 < {target} > 𝗔𝗣𝗞𝗜 𝗚𝗔𝗡𝗗 𝗠𝗘 𝗟𝗢𝗗𝗔 •°*”˜.•°*”˜🍑🍾 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------𝗖𝗛𝗟𝗧𝗜 𝗛𝗔𝗜 𝗚𝗔𝗗𝗜 𝗖𝗛𝗟𝗧𝗔 𝗛𝗔𝗜 𝗚𝗛𝗢𝗗𝗔 𝗗𝗔𝗟𝗗𝗨 𝗞𝗬 < {target} > 𝗔𝗣𝗞𝗜 𝗚𝗔𝗡𝗗 𝗠𝗘 𝗟𝗢𝗗𝗔 •°*”˜.•°*”˜🍑🍾",
    "< {target} > 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗡𝗘 𝗛𝗔𝗚 𝗗𝗜𝗬𝗔 𝗕𝗔𝗗𝗕𝗨 𝗔𝗥𝗜 𝗕𝗛𝗢𝗧 𝗞𝗛𝗔𝗧𝗔𝗥𝗡𝗔𝗞 💀😵‍💫♡¸.•* --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------< {target} > 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗡𝗘 𝗛𝗔𝗚 𝗗𝗜𝗬𝗔 𝗕𝗔𝗗𝗕𝗨 𝗔𝗥𝗜 𝗕𝗛𝗢𝗧 𝗞𝗛𝗔𝗧𝗔𝗥𝗡𝗔𝗞 💀😵‍💫♡¸.•*",
    "𝗛𝗘𝗟𝗣 𝗛𝗘𝗟𝗣 𝗛𝗘𝗟𝗣 < {target} > 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗠𝗘𝗥𝗔 𝗥𝗔𝗣𝗘 𝗞𝗥 𝗥𝗛𝗜 𝗛𝗔𝗜.𖥔 ݁ ˖ִ🛸༄˖°. --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------𝗛𝗘𝗟𝗣 𝗛𝗘𝗟𝗣 𝗛𝗘𝗟𝗣 < {target} > 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗠𝗘𝗥𝗔 𝗥𝗔𝗣𝗘 𝗞𝗥 𝗥𝗛𝗜 𝗛𝗔𝗜.𖥔 ݁ ˖ִ🛸༄˖°.",
    "< {target} > 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗘 𝗔𝗚𝗘𝗥 10 𝗔𝗦𝗛𝗜𝗤 𝗛𝗔𝗜𝗧𝗢 𝗣𝗛𝗘𝗟𝗔 𝗠𝗘 𝗛𝗘 𝗥𝗔𝗛𝗨𝗡𝗚𝗔 ༄˖°.🍂.ೃ࿔*:･ --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------< {target} > 𝗧𝗘𝗥𝗜 𝗠𝗔𝗔 𝗞𝗘 𝗔𝗚𝗘𝗥 10 𝗔𝗦𝗛𝗜𝗤 𝗛𝗔𝗜𝗧𝗢 𝗣𝗛𝗘𝗟𝗔 𝗠𝗘 𝗛𝗘 𝗥𝗔𝗛𝗨𝗡𝗚𝗔 ༄˖°.🍂.ೃ࿔*:･",
    "𝗠𝗔𝗡𝗘 < {target} > 𝗧𝗘𝗥𝗜 𝗠𝗔𝗞𝗜𝗖𝗛𝗨𝗧 𝗠𝗘 𝗟𝗨𝗡𝗗 𝗗𝗔𝗟𝗔 𝗙𝗜𝗥 𝗕𝗔𝗛𝗔𝗥 𝗛𝗘 𝗡𝗛𝗜 𝗔𝗬𝗔 𝗚𝗟𝗜𝗧𝗖𝗛 𝗛𝗢𝗚𝗬𝗔 ୧ ‧🌀₊˚ 🍮 ⋅ ☆ --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------𝗠𝗔𝗡𝗘 < {target} > 𝗧𝗘𝗥𝗜 𝗠𝗔𝗞𝗜𝗖𝗛𝗨𝗧 𝗠𝗘 𝗟𝗨𝗡𝗗 𝗗𝗔𝗟𝗔 𝗙𝗜𝗥 𝗕𝗔𝗛𝗔𝗥 𝗛𝗘 𝗡𝗛𝗜 𝗔𝗬𝗔 𝗚𝗟𝗜𝗧𝗖𝗛 𝗛𝗢𝗚𝗬𝗔 ୧ ‧🌀₊˚ 🍮 ⋅ ☆",
    "< {target} > 𝗧𝗘𝗥𝗜 𝗠𝗔𝗞𝗜 𝗖𝗛𝗨𝗖𝗛𝗜 𝗠𝗢𝗨𝗡𝗧 𝗘𝗩𝗘𝗥𝗘𝗦𝗧 𝗦𝗘 𝗨𝗖𝗛𝗜 𝗝𝗔𝗛𝗔 𝗗𝗔𝗕𝗔𝗬𝗘 𝗗𝗨𝗗𝗨 𝗪𝗔𝗛𝗜 𝗡𝗜𝗞𝗟𝗘 𝗕𝗨𝗕𝗨 🏞𝄞⨾💿✮˚.⋆ --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------< {target} > 𝗧𝗘𝗥𝗜 𝗠𝗔𝗞𝗜 𝗖𝗛𝗨𝗖𝗛𝗜 𝗠𝗢𝗨𝗡𝗧 𝗘𝗩𝗘𝗥𝗘𝗦𝗧 𝗦𝗘 𝗨𝗖𝗛𝗜 𝗝𝗔𝗛𝗔 𝗗𝗔𝗕𝗔𝗬𝗘 𝗗𝗨𝗗𝗨 𝗪𝗔𝗛𝗜 𝗡𝗜𝗞𝗟𝗘 𝗕𝗨𝗕𝗨 🏞𝄞⨾💿✮˚.⋆"
]

all_commands = [
    "start", "power", "swipe", "swipestop", "cswipe", "dcswipe", "settext", "setspeed",
    "burst", "roast", "setroast", "sudo", "unsudo", "sudolist",
    "chup", "bol", "info", "ping", "status", "tts", "ptst", "raid", "draid"
]

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def is_sudo(user_id):
    return user_id in sudo_users

async def smart_reply(update: Update, text):
    msg = update.message
    if not msg: return
    if msg.reply_to_message:
        return await msg.reply_text(f"<b>{text}</b>", reply_to_message_id=msg.reply_to_message.message_id, parse_mode="HTML")
    else:
        return await msg.reply_text(f"<b>{text}</b>", parse_mode="HTML")

custom_swipe_texts = [
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 DELHI 🏙️",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 UP 🕌",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 BIHAR 🌾",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 RAJASTHAN 👑",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 MAHARASHTRA 🌆",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 GUJARAT 🦁",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 PUNJAB 💪",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 HARYANA 🚜",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 MP 🏞️",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 WB 🌉",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 KARNATAKA 💻",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 TN 🌊",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 KERALA 🌴",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 AP 🌶️",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 TELANGANA 🏰",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 ORISSA ⛩️",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 JHARKHAND 🌳",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 CHHATTISGARH 🍚",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 ASSAM 🍵",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 HP 🏔️",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 UTTARAKHAND 🕉️",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 GOA 🏖️",
]

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in sudo_users and update.effective_user.id != OWNER_ID:
        return
    cmd = update.message.text.split()[0][1:]
    matches = get_close_matches(cmd, all_commands, n=1, cutoff=0.6)
    if matches:
        await smart_reply(update, f"⚠️ 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱\n<b>𝗗𝗶𝗱 𝘆𝗼𝘂 𝗺𝗲𝗮𝗻:</b> /{matches[0]}")
    else:
        await smart_reply(update, f"⚠️ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗰𝗼𝗺𝗮𝗻𝗱: /{cmd}\n<b>𝗨𝘀𝗲:</b> /𝗽𝗼𝘄𝗲𝗿 𝘁𝗼 𝘀𝗲𝗲 𝗮𝗹𝗹 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀")

async def power(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id): return
    keyboard = [
        [InlineKeyboardButton("⚔️ 𝗦𝘄𝗶𝗽𝗲 & 𝗕𝘂𝗿𝘀𝘁", callback_data="module_swipe")],
        [InlineKeyboardButton("⚡ 𝗥𝗮𝗶𝗱", callback_data="module_raid")],
        [InlineKeyboardButton("🔇 𝗠𝘂𝘁𝗲", callback_data="module_mute")],
        [InlineKeyboardButton("📊 𝗜𝗻𝗳𝗼 & 𝗦𝘁𝗮𝘁𝘂𝘀", callback_data="module_info")],
        [InlineKeyboardButton("🛡️ 𝗦𝘂𝗱𝗼 𝗔𝗱𝗺𝗶𝗻", callback_data="module_admin")]
    ]
    await update.message.reply_text(
        f"<b>𝗦𝗜𝗥𝗘𝗡 𝗩𝟯.𝟵.𝟭</b>\n<b>● 𝗦𝘁𝗮𝘁𝘂𝘀 › 𝗢𝗻𝗹𝗶𝗻𝗲</b>\n<b>● 𝗩𝗲𝗿𝘀𝗶𝗼𝗻 › 𝘃𝟯.𝟵.𝟭</b>\n<b>● 𝗠𝗼𝗱𝗲 › 𝗔𝗰𝘁𝗶𝘃𝗲</b>\n\n<b>𝗦𝗲𝗹𝗲𝗰𝘁 𝗮 𝗺𝗼𝗱𝘂𝗹𝗲 𝗯𝗲𝗹𝗼𝘄.</b>",
        reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await power(update, context)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "module_swipe":
        keyboard = [[InlineKeyboardButton("◀️ 𝗕𝗮𝗰𝗸", callback_data="back_main")]]
        await query.edit_message_text(f"<b>𝗦𝗪𝗜𝗣𝗘 & 𝗕𝗨𝗥𝗦𝗧 𝗠𝗢𝗗𝗨𝗟𝗘</b>\n\n<b>/𝘀𝘄𝗶𝗽𝗲</b> - Target user\n<b>/𝗰𝘀𝘄𝗶𝗽𝗲</b> - Custom swipe\n<b>/𝘀𝘄𝗶𝗽𝗲𝘀𝘁𝗼𝗽</b> - Stop swipe\n<b>/𝗱𝗰𝘀𝘄𝗶𝗽𝗲</b> - Stop cswipe\n<b>/𝗯𝘂𝗿𝘀𝘁</b> - Burst mode\n<b>/𝘀𝗲𝘁𝘁𝗲𝘅𝘁</b> - Templates\n<b>/𝘀𝗲𝘁𝘀𝗽𝗲𝗲𝗱</b> - Speed", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    elif query.data == "module_raid":
        keyboard = [[InlineKeyboardButton("◀️ 𝗕𝗮𝗰𝗸", callback_data="back_main")]]
        await query.edit_message_text(f"<b>𝗥𝗔𝗜𝗗 𝗠𝗢𝗗𝗨𝗟𝗘</b>\n\n<b>/𝗿𝗮𝗶𝗱 <target></b> - Start raid flood\n<b>/𝗱𝗿𝗮𝗶𝗱</b> - Stop raid", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    elif query.data == "module_mute":
        keyboard = [[InlineKeyboardButton("◀️ 𝗕𝗮𝗰𝗸", callback_data="back_main")]]
        await query.edit_message_text(f"<b>𝗠𝗨𝗧𝗘 𝗠𝗢𝗗𝗨𝗟𝗘</b>\n\n<b>/𝗰𝗵𝘂𝗽</b> - Mute user\n<b>/𝗯𝗼𝗹</b> - Unmute user", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    elif query.data == "module_info":
        keyboard = [[InlineKeyboardButton("◀️ 𝗕𝗮𝗰𝗸", callback_data="back_main")]]
        await query.edit_message_text(f"<b>𝗜𝗡𝗙𝗢 & 𝗦𝗧𝗔𝗧𝗨𝗦</b>\n\n<b>/𝗶𝗻𝗳𝗼</b> - User info\n<b>/𝘀𝘁𝗮𝘁𝘂𝘀</b> - Bot status\n<b>/𝗽𝗶𝗻𝗴</b> - Latency\n<b>/𝗽𝘁𝘀𝘁</b> - Multi-bot ping\n<b>/𝘁𝘁𝘀</b> - Realistic speech", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    elif query.data == "module_admin":
        keyboard = [[InlineKeyboardButton("◀️ 𝗕𝗮𝗰𝗸", callback_data="back_main")]]
        await query.edit_message_text(f"<b>𝗦𝗨𝗗𝗢 & 𝗔𝗗𝗠𝗜𝗡 𝗣𝗔𝗡𝗘𝗟</b>\n\n<b>/𝘀𝘂𝗱𝗼</b> - Grant access\n<b>/𝘂𝗻𝘀𝘂𝗱𝗼</b> - Revoke access\n<b>/𝘀𝘂𝗱𝗼𝗹𝗶𝘀𝘁</b> - View list\n<b>/𝗿𝗼𝗮𝘀𝘁</b> - Roast user\n<b>/𝘀𝗲𝘁𝗿𝗼𝗮𝘀𝘁</b> - Roast templates", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    elif query.data == "back_main":
        keyboard = [
            [InlineKeyboardButton("⚔️ 𝗦𝘄𝗶𝗽𝗲 & 𝗕𝘂𝗿𝘀𝘁", callback_data="module_swipe")],
            [InlineKeyboardButton("⚡ 𝗥𝗮𝗶𝗱", callback_data="module_raid")],
            [InlineKeyboardButton("🔇 𝗠𝘂𝘁𝗲", callback_data="module_mute")],
            [InlineKeyboardButton("📊 𝗜𝗻𝗳𝗼 & 𝗦𝘁𝗮𝘁𝘂𝘀", callback_data="module_info")],
            [InlineKeyboardButton("🛡️ 𝗦𝘂𝗱𝗼 𝗔𝗱𝗺𝗶𝗻", callback_data="module_admin")]
        ]
        await query.edit_message_text(f"<b>𝗦𝗜𝗥𝗘𝗡 𝗩𝟯.𝟵.𝟭</b>\n<b>● 𝗦𝘁𝗮𝘁𝘂𝘀 › 𝗢𝗻𝗹𝗶𝗻𝗲</b>\n<b>● 𝗩𝗲𝗿𝘀𝗶𝗼𝗻 › 𝘃𝟯.𝟵.𝟭</b>\n<b>● 𝗠𝗼𝗱𝗲 › 𝗔𝗰𝘁𝗶𝘃𝗲</b>\n\n<b>𝗦𝗲𝗹𝗲𝗰𝘁 𝗮 𝗺𝗼𝗱𝘂𝗹𝗲 𝗯𝗲𝗹𝗼𝘄.</b>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

async def swipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id): return await smart_reply(update, "⛔ 𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱")
    if not update.message.reply_to_message: return await smart_reply(update, "⚠️ 𝗨𝘀𝗮𝗴𝗲: Reply to a user with /swipe")
    user = update.message.reply_to_message.from_user
    swipe_targets[user.id] = update.effective_chat.id
    swipe_texts[user.id] = custom_swipe_texts.copy()
    swipe_index[user.id] = 0
    await smart_reply(update, f"✅ 𝗦𝘄𝗶𝗽𝗲 𝗔𝗰𝘁𝗶𝘃𝗮𝘁𝗲𝗱\n<b>𝗧𝗮𝗿𝗴𝗲𝘁:</b> {user.first_name}")

async def swipestop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id): return await smart_reply(update, "⛔ 𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱")
    if not update.message.reply_to_message: return await smart_reply(update, "⚠️ 𝗨𝘀𝗮𝗴𝗲: Reply to a user with /swipestop")
    uid = update.message.reply_to_message.from_user.id
    swipe_targets.pop(uid, None)
    await smart_reply(update, "⛔ 𝗦𝘄𝗶𝗽𝗲 𝗗𝗲𝗮𝗰𝘁𝗶𝘃𝗮𝘁𝗲𝗱")

async def cswipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id): return await smart_reply(update, "⛔ 𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱")
    if not update.message.reply_to_message: return await smart_reply(update, "⚠️ 𝗨𝘀𝗮𝗴𝗲: Reply to a user with /cswipe <text>")
    if not context.args: return await smart_reply(update, "⚠️ 𝗨𝘀𝗮𝗴𝗲: /𝗰𝘀𝘄𝗶𝗽𝗲 <text>")
    user = update.message.reply_to_message.from_user
    custom_text = " ".join(context.args)
    cswipe_targets[user.id] = update.effective_chat.id
    cswipe_texts[user.id] = custom_text
    await smart_reply(update, f"✅ 𝗖𝗦𝘄𝗶𝗽𝗲 𝗔𝗰𝘁𝗶𝘃𝗮𝘁𝗲𝗱\n<b>𝗧𝗮𝗿𝗴𝗲𝘁:</b> {user.first_name}")

async def dcswipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id): return await smart_reply(update, "⛔ 𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱")
    if not update.message.reply_to_message: return await smart_reply(update, "⚠️ 𝗨𝘀𝗮𝗴𝗲: Reply to a user with /dcswipe")
    uid = update.message.reply_to_message.from_user.id
    cswipe_targets.pop(uid, None)
    cswipe_texts.pop(uid, None)
    await smart_reply(update, "⛔ 𝗖𝗦𝘄𝗶𝗽𝗲 𝗗𝗲𝗮𝗰𝘁𝗶𝘃𝗮𝘁𝗲𝗱")

async def raid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id): return await smart_reply(update, "⛔ 𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱")
    if not context.args: return await smart_reply(update, "⚠️ 𝗨𝘀𝗮𝗴𝗲: /𝗿𝗮𝗶𝗱 <target>")
    target_name = " ".join(context.args)
    chat_id = update.effective_chat.id
    raid_targets.add(chat_id)
    await smart_reply(update, f"⚡ 𝗥𝗮𝗶𝗱 𝗜𝗻𝗶𝘁𝗶𝗮𝘁𝗲𝗱 𝗼𝗻: <b>{target_name}</b>")
    while chat_id in raid_targets:
        raw_text = random.choice(raid_texts)
        text = raw_text.replace("{target}", target_name)
        try:
            await context.bot.send_message(chat_id=chat_id, text=f"<b>{text}</b>", parse_mode="HTML")
        except:
            await asyncio.sleep(1.0)
            continue
        await asyncio.sleep(0.2)

async def draid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id): return await smart_reply(update, "⛔ 𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱")
    chat_id = update.effective_chat.id
    if chat_id in raid_targets:
        raid_targets.discard(chat_id)
        await smart_reply(update, "🛑 𝗥𝗮𝗶𝗱 𝗛𝗮𝗹𝘁𝗲𝗱")
    else:
        await smart_reply(update, "⚠️ No active raid")

async def settext(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global custom_swipe_texts
    if not is_sudo(update.effective_user.id): return await smart_reply(update, "⛔ 𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱")
    if not context.args: return await smart_reply(update, "⚠️ 𝗨𝘀𝗮𝗴𝗲: /𝘀𝗲𝘁𝘁𝗲𝘅𝘁 𝘁𝟭 | 𝘁𝟮")
    new_texts = " ".join(context.args).split(" | ")
    custom_swipe_texts = [t.strip() for t in new_texts if t.strip()]
    await smart_reply(update, f"✅ 𝗧𝗲𝘅𝘁 𝗨𝗽𝗱𝗮𝘁𝗲𝗱\n<b>𝗧𝗼𝘁𝗮𝗹:</b> {len(custom_swipe_texts)}")

async def setspeed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global swipe_speed
    if not is_sudo(update.effective_user.id): return await smart_reply(update, "⛔ 𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱")
    if not context.args: return await smart_reply(update, "⚠️ 𝗨𝘀𝗮𝗴𝗲: /𝘀𝗲𝘁𝘀𝗽𝗲𝗲𝗱 𝟬.𝟯")
    try:
        swipe_speed = float(context.args[0])
        await smart_reply(update, f"✅ 𝗦𝗽𝗲𝗲𝗱 𝗦𝗲𝘁: {swipe_speed}𝘀")
    except:
        await smart_reply(update, "⚠️ 𝗨𝘀𝗮𝗴𝗲: /𝘀𝗲𝘁𝘀𝗽𝗲𝗲𝗱 𝟬.𝟯")

async def burst(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BURST_MODE
    if not is_sudo(update.effective_user.id): return await smart_reply(update, "⛔ 𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱")
    if not context.args:
        status = "𝗢𝗡" if BURST_MODE else "𝗢𝗙𝗙"
        return await smart_reply(update, f"⚠️ 𝗨𝘀𝗮𝗴𝗲: /𝗯𝘂𝗿𝘀𝘁 𝗼𝗻 | 𝗼𝗳𝗳\n<b>𝗖𝘂𝗿𝗿𝗲𝗻𝘁:</b> {status}")
    arg = context.args[0].lower()
    if arg == "on":
        BURST_MODE = True
        await smart_reply(update, "✅ 𝗕𝘂𝗿𝘀𝘁 𝗘𝗻𝗮𝗯𝗹𝗲𝗱")
    elif arg == "off":
        BURST_MODE = False
        await smart_reply(update, "✅ 𝗕𝘂𝗿𝘀𝘁 𝗗𝗶𝘀𝗮𝗯𝗹𝗲𝗱")
    else:
        await smart_reply(update, "⚠️ 𝗨𝘀𝗮𝗴𝗲: /𝗯𝘂𝗿𝘀𝘁 𝗼𝗻 | 𝗼𝗳𝗳")

async def roast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return await smart_reply(update, "𝗸𝘆𝗼𝗻 𝗸𝗿𝗲𝘆 😂")
    if not update.message.reply_to_message: return await smart_reply(update, "⚠️ 𝗨𝘀𝗮𝗴𝗲: Reply to user")
    text = random.choice(roast_texts)
    await update.message.reply_to_message.reply_text(f"<b>{text}</b>", parse_mode="HTML")

async def setroast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global roast_texts
    if update.effective_user.id != OWNER_ID: return await smart_reply(update, "𝗸𝘆𝗼𝗻 𝗸𝗿𝗲𝘆 😂")
    if not context.args: return await smart_reply(update, "⚠️ 𝗨𝘀𝗮𝗴𝗲: /𝘀𝗲𝘁𝗿𝗼𝗮𝘀𝘁 𝘁𝟭 | 𝘁𝟮")
    new_texts = " ".join(context.args).split(" | ")
    roast_texts = [t.strip() for t in new_texts if t.strip()]
    await smart_reply(update, f"✅ 𝗥𝗼𝗮𝘀𝘁 𝗨𝗽𝗱𝗮𝘁𝗲𝗱")

async def sudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return await smart_reply(update, "⛔ 𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱")
    if not update.message.reply_to_message: return await smart_reply(update, "⚠️ 𝗨𝘀𝗮𝗴𝗲: Reply to user")
    uid = update.message.reply_to_message.from_user.id
    sudo_users.add(uid)
    await smart_reply(update, f"👑 𝗦𝘂𝗱𝗼 𝗚𝗿𝗮𝗻𝘁𝗲𝗱")

async def unsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return await smart_reply(update, "⛔ 𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱")
    if not update.message.reply_to_message: return await smart_reply(update, "⚠️ 𝗨𝘀𝗮𝗴𝗲: Reply to user")
    uid = update.message.reply_to_message.from_user.id
    sudo_users.discard(uid)
    await smart_reply(update, f"⛔ 𝗦𝘂𝗱𝗼 𝗥𝗲𝘃𝗼𝗸𝗲𝗱")

async def sudolist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return await smart_reply(update, "⛔ 𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱")
    users = "\n".join([f"<b>•</b> <code>{uid}</code>" for uid in sudo_users])
    await smart_reply(update, f"<b>𝗦𝗨𝗗𝗢 𝗟𝗜𝗦𝗧:</b>\n{users}")

async def chup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id): return await smart_reply(update, "⛔ 𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱")
    if not update.message.reply_to_message: return await smart_reply(update, "⚠️ 𝗨𝘀𝗮𝗴𝗲: Reply to user")
    uid = update.message.reply_to_message.from_user.id
    muted_users.add(uid)
    await smart_reply(update, "🔇 𝗠𝘂𝘁𝗲𝗱")

async def bol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id): return await smart_reply(update, "⛔ 𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱")
    if not update.message.reply_to_message: return await smart_reply(update, "⚠️ 𝗨𝘀𝗮𝗴𝗲: Reply to user")
    uid = update.message.reply_to_message.from_user.id
    muted_users.discard(uid)
    await smart_reply(update, "🔊 𝗨𝗻𝗺𝘂𝘁𝗲𝗱")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.message.reply_to_message.from_user if update.message.reply_to_message else update.effective_user
    pfp = await context.bot.get_user_profile_photos(target.id, limit=1)
    pfp_count = pfp.total_count
    if pfp_count > 0:
        photo_file = await context.bot.get_file(pfp.photos[0][0].file_id)
        photo = photo_file.file_id
    else:
        photo = "https://i.imgur.com/8wQhYbQ.jpg"
    caption = f"𝗨𝗦𝗘𝗥 𝗜𝗡𝗙𝗢\n● <b>Name:</b> {target.full_name}\n● <b>Username:</b> @{target.username if target.username else 'None'}\n● <b>ID:</b> <code>{target.id}</code>\n● <b>Chat ID:</b> <code>{update.effective_chat.id}</code>"
    await update.message.reply_photo(photo=photo, caption=caption, parse_mode="HTML")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start = time.time()
    msg = await smart_reply(update, "🏓 𝗣𝗶𝗻𝗴𝗶𝗻𝗴...")
    end = time.time()
    response_time = round((end - start) * 1000, 2)
    await msg.edit_text(f"<b>🏓 𝗣𝗢𝗡𝗚: {response_time}𝗺𝘀</b>", parse_mode="HTML")

async def ptst(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id): return
    res_msg = "<b>📊 MULTI-BOT PING:</b>\n"
    for i, tkn in enumerate(TOKENS, 1):
        try:
            temp_app = Application.builder().token(tkn).build()
            start_t = time.time()
            await temp_app.bot.get_me()
            latency = round((time.time() - start_t) * 1000, 2)
            res_msg += f"<b>Bot {i}:</b> <code>{latency}ms</code> [ONLINE]\n"
        except:
            res_msg += f"<b>Bot {i}:</b> <code>OFFLINE</code>\n"
    await smart_reply(update, res_msg)

async def tts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_sudo(update.effective_user.id): return
    if not context.args: return await smart_reply(update, "⚠️ 𝗨𝘀𝗮𝗴𝗲: /𝘁𝘁𝘀 <text>")
    text_to_speak = " ".join(context.args)
    file_path = "tts_audio.mp3"
    try:
        voice = "hi-IN-SwaraNeural" if any(ord(c) > 127 for c in text_to_speak) else "en-US-AriaNeural"
        communicate = edge_tts.Communicate(text_to_speak, voice)
        await communicate.save(file_path)
        with open(file_path, 'rb') as audio:
            await update.message.reply_audio(audio=audio, caption=f"🎙️ <b>TTS:</b> {text_to_speak}", parse_mode="HTML")
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        await smart_reply(update, f"⚠️ Error: {str(e)}")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uptime = time.time() - START_TIME
    hours, rem = divmod(uptime, 3600)
    minutes, seconds = divmod(rem, 60)
    status_text = (
        f"<b>┌───────────────────────────┐</b>\n"
        f"<b>│  ⚡ {BOT_NAME} // STATUS ⚡  │</b>\n"
        f"<b>└───────────────────────────┘</b>\n"
        f" ├── 🌐 <b>Status:</b> <code>ONLINE [SECURE]</code>\n"
        f" ├── 👑 <b>Owner ID:</b> <code>{OWNER_ID}</code>\n"
        f" ├── ⏱️ <b>Uptime:</b> {int(hours)}𝗵 {int(minutes)}𝗺 {int(seconds)}𝘀\n"
        f" ├── ⚔️ <b>Active Swipes:</b> {len(swipe_targets) + len(cswipe_targets)}\n"
        f" ├── ⚡ <b>Burst Mode:</b> {'ON' if BURST_MODE else 'OFF'}\n"
        f" └── 👥 <b>Total Sudo:</b> {len(sudo_users)}\n"
        f"<b>─────────────────────────────</b>"
    )
    await smart_reply(update, status_text)

async def block(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not update.message or not user: return
    if user.id in muted_users:
        try: await update.message.delete()
        except: pass
        return
        
    if user.id in cswipe_targets:
        c_text = cswipe_texts.get(user.id, "Default Text")
        try: await update.message.reply_text(f"<b>{c_text}</b>", parse_mode="HTML")
        except: pass
        return

    if user.id in swipe_targets:
        texts = swipe_texts.get(user.id, custom_swipe_texts)
        if BURST_MODE:
            for text in texts:
                try: await update.message.reply_text(f"<b>{text}</b>", parse_mode="HTML")
                except: pass
                await asyncio.sleep(0.05)
        else:
            i = swipe_index.get(user.id, 0)
            text = texts[i % len(texts)]
            swipe_index[user.id] = (i + 1) % len(texts)
            await asyncio.sleep(swipe_speed)
            try: await update.message.reply_text(f"<b>{text}</b>", parse_mode="HTML")
            except: pass

def main():
    app = Application.builder().token(MASTER_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("power", power))
    app.add_handler(CommandHandler("swipe", swipe))
    app.add_handler(CommandHandler("swipestop", swipestop))
    app.add_handler(CommandHandler("cswipe", cswipe))
    app.add_handler(CommandHandler("dcswipe", dcswipe))
    app.add_handler(CommandHandler("settext", settext))
    app.add_handler(CommandHandler("setspeed", setspeed))
    app.add_handler(CommandHandler("burst", burst))
    app.add_handler(CommandHandler("roast", roast))
    app.add_handler(CommandHandler("setroast", setroast))
    app.add_handler(CommandHandler("sudo", sudo))
    app.add_handler(CommandHandler("unsudo", unsudo))
    app.add_handler(CommandHandler("sudolist", sudolist))
    app.add_handler(CommandHandler("chup", chup))
    app.add_handler(CommandHandler("bol", bol))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("ptst", ptst))
    app.add_handler(CommandHandler("tts", tts))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("raid", raid))
    app.add_handler(CommandHandler("draid", draid))
    
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, block))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    
    print(f"{BOT_NAME} v3.9.1 is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
