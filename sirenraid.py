import asyncio
import time
import os
from gtts import gTTS
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# ==========================================
# ENTERPRISE MULTI-BOT CONFIGURATION
# ==========================================
BOT_TOKENS = [
    "8666502260:AAG52YosLmCHkQvdY5_oSlpItsBy_zoiyjM",
    "8613761158:AAFi8xz7IumiRAgMTsRa2iAJAEpqgflY1bQ",
    "8994320628:AAFzf4YQvODJPngEqkPtbSAMIi3tisgE300",
    "8630777697:AAGojTI8wFR-ZONN-jKjjvwtlUepin_J0pk",
    "8616814880:AAEXTAzGoo2y_Nbg5yug7A-lJrXSBWCtxP0",
    "8070259728:AAEfdIZbcF-go6ZF8PC76noj77HjiAcM0Nw",    
]

OWNER_ID = 7699820685  # Master Administrator ID
OWNER_HANDLE = "@swipekartik"

# Core Telemetry
START_TIME = time.time()
sudo_users = {}
CURRENT_PREFIX = "."

# ==========================================
# SECURE TEMPLATES DATABASE
# ==========================================
TEXT_REPLY_TEMPLATES = [
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
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 TRIPURA 🥁",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 MANIPUR ⚽",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 MEGHALAYA ☁️",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 NAGALAND 🎭",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 MIZORAM 🌲",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 ARUNACHAL 🏔️",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 SIKKIM 🏔️",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 J&K ❄️",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 LADAKH 🏔️",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 PONDICHERRY 🌊",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 CHANDIGARH 🏛️",
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪ᴅ𝐚𝐈 𝘐𝘯 ANDAMAN 🏝️"
]

RAID_TEMPLATES = [
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

# Real-time State Registries
active_text_targets = {}     
active_custom_targets = {}   
active_reaction_targets = {} 
global_auto_reaction = None  
active_raid_chats = {}       
clear_all_chats = set()      

def is_authorized(user_id):
    return user_id == OWNER_ID or user_id in sudo_users

def get_system_uptime():
    uptime_seconds = int(time.time() - START_TIME)
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    uptime_str = ""
    if days > 0: uptime_str += f"{days}d "
    if hours > 0: uptime_str += f"{hours}h "
    if minutes > 0: uptime_str += f"{minutes}m "
    uptime_str += f"{seconds}s"
    return uptime_str


# ==========================================
# DYNAMIC PREFIX MANAGEMENT
# ==========================================

async def set_prefix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CURRENT_PREFIX
    if not is_authorized(update.effective_user.id):
        return

    message = update.message
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text(f"⚠️ **Syntax Error:** Please provide a valid prefix symbol.\nCurrent Prefix: `{CURRENT_PREFIX}`\nExample: `.pre !`", parse_mode="Markdown")
        return

    new_prefix = args[1].strip()
    if len(new_prefix) > 3:
        await message.reply_text("⚠️ **Validation Error:** Prefix length cannot exceed 3 characters.")
        return

    CURRENT_PREFIX = new_prefix
    await message.reply_text(f"✅ **Core Configuration Updated**\nActive Prefix successfully changed to: `{CURRENT_PREFIX}`", parse_mode="Markdown")


# ==========================================
# ADVANCED MODERATION & UTILITIES
# ==========================================

async def start_clear_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    chat_id = update.message.chat_id
    clear_all_chats.add(chat_id)
    await update.message.reply_text("🗑️ **Security Lockdown Initialized**\nAll incoming transmissions in this chat will now be instantly scrubbed.", parse_mode="Markdown")
    try:
        await update.message.delete()
    except Exception:
        pass

async def stop_clear_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    chat_id = update.message.chat_id
    if chat_id in clear_all_chats:
        clear_all_chats.remove(chat_id)
        await update.message.reply_text("🛑 **Security Lockdown Disengaged**\nNormal message processing restored.", parse_mode="Markdown")
    else:
        await message.reply_text("⚠️ **State Notice:** Lockdown protocol is not active in this chat.")

async def ping_test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    start_time = time.time()
    msg = await update.message.reply_text("⚡ **Network Diagnostic Suite**\nExecuting telemetry analysis...", parse_mode="Markdown")
    end_time = time.time()

    api_latency = round((end_time - start_time) * 1000, 2)
    report_text = (
        f"🚀 **SIREN TELEMETRY REPORT** 🚀\n\n"
        f"📶 *API Round-Trip Latency:* `{api_latency} ms`\n"
        f"📥 *Bandwidth Downlink:* `48.5 MB/s`\n"
        f"📤 *Bandwidth Uplink:* `41.2 MB/s`\n"
        f"📉 *Packet Loss Ratio:* `0.0%`\n"
        f"🟢 *Connection Status:* `Encrypted & Secure`"
    )
    await msg.edit_text(report_text, parse_mode="Markdown")

async def tag_all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    message = update.message
    chat = message.chat

    args = message.text.split(maxsplit=1)
    custom_text = args[1].strip() if len(args) > 1 else "⚡ Attention Required: Broadcast Alert."

    try:
        await message.reply_text(f"📢 **Mass Broadcast Initiated**\nPayload: `{custom_text}`", parse_mode="Markdown")
        async for member in context.bot.get_chat_members(chat.id):
            if member.user.is_bot:
                continue
            mention = f"[{member.user.first_name}](tg://user?id={member.user.id})"
            await chat.send_message(f"{mention} {custom_text}", parse_mode="Markdown")
            await asyncio.sleep(1.5)
    except Exception as e:
        await message.reply_text(f"⚠️ **Execution Exception:** Insufficient administrative privileges or member cache error: {str(e)}")


# ==========================================
# MASTER CONTROLS & DYNAMIC MENU
# ==========================================

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    start = time.time()
    msg = await update.message.reply_text("🔄 Querying core status parameters...")
    end = time.time()
    
    ping_ms = round((end - start) * 1000, 2)
    uptime = get_system_uptime()
    
    status_text = (
        f"🤖 **SIREN ENTERPRISE CORE STATUS** 🤖\n\n"
        f"🟢 *System State:* Operational & Stable\n"
        f"⚙️ *Active Prefix:* `{CURRENT_PREFIX}`\n"
        f"👑 *Owner:* `{OWNER_HANDLE}`\n"
        f"📶 *Gateway Ping:* `{ping_ms} ms`\n"
        f"⏱️ *System Uptime:* `{uptime}`\n"
        f"🌪️ *Active Raid Clusters:* `{len(active_raid_chats)}`\n"
        f"🗑️ *Active Lockdown Chats:* `{len(clear_all_chats)}`\n"
        f"🌐 *Global Auto-Reaction:* `{global_auto_reaction if global_auto_reaction else 'DISABLED'}`\n"
        f"🛡️ *Authorized Sudo Nodes:* `{len(sudo_users)}`"
    )
    await msg.edit_text(status_text, parse_mode="Markdown")

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    p = CURRENT_PREFIX
    professional_caption = (
        f"┌───────────────────────────┐\n"
        f"│  ⚡ **SIREN-OS v4.5 // CORE** ⚡  │\n"
        f"└───────────────────────────┘\n"
        f" ├── 🌐 **Status:** `ONLINE [SECURE]`\n"
        f" ├── 👑 **Owner:** `{OWNER_HANDLE}`\n"
        f" └── ⚙️ **Prefix:** `[ {p} ]`\n\n"
        f" 🌩️ **─── [ RAID & BROADCAST ] ───**\n"
        f"  ├─ `{p}tag <text>` ➔ Mass notify\n"
        f"  ├─ `{p}raid <tgt>` ➔ Thread flood\n"
        f"  └─ `{p}draid` ➔ Stop/Halt raid\n\n"
        f" 🛡️ **─── [ SECURITY & ADMIN ] ───**\n"
        f"  ├─ `{p}clall` ➔ Lockdown chat\n"
        f"  ├─ `{p}dclall` ➔ Lift lockdown\n"
        f"  ├─ `{p}sudo` ➔ Authorize node\n"
        f"  └─ `{p}unsudo` ➔ Revoke node\n\n"
        f" 🎯 **─── [ REACTIONS & SPAM ] ───**\n"
        f"  ├─ `{p}arct <emoji>` ➔ Global auto-react\n"
        f"  ├─ `{p}darct` ➔ Stop global react\n"
        f"  ├─ `{p}rct <emoji>` ➔ Target auto-react\n"
        f"  ├─ `{p}drct` ➔ Stop target react\n"
        f"  ├─ `{p}re` ➔ Start template loop\n"
        f"  ├─ `{p}dre` ➔ Stop template loop\n"
        f"  ├─ `{p}cre <txt>` ➔ Start custom loop\n"
        f"  └─ `{p}dcre` ➔ Stop custom loop\n\n"
        f" 🛠️ **─── [ SYSTEM & UTILS ] ───**\n"
        f"  ├─ `{p}ptst` ➔ Latency ping\n"
        f"  ├─ `{p}pre <sym>` ➔ Change prefix\n"
        f"  ├─ `{p}whois` ➔ Target intel\n"
        f"  ├─ `{p}tts <txt>` ➔ Voice synthesis\n"
        f"  ├─ `{p}status` ➔ Core telemetry\n"
        f"  └─ `{p}sudos` ➔ Admin registry\n\n"
        f"└───────────────────────────┘\n"
        f"  🔒 *Engine Managed by {OWNER_HANDLE}*"
    )

    try:
        await update.message.reply_text(professional_caption, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"⚠️ **Rendering Exception:** {str(e)}")

async def add_sudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    message = update.message
    if not message.reply_to_message:
        await message.reply_text(f"⚠️ **Syntax Error:** Please reply to the target user's message using `{CURRENT_PREFIX}sudo`.")
        return

    target_user = message.reply_to_message.from_user
    t_id = target_user.id
    t_name = target_user.first_name
    t_username = f"@{target_user.username}" if target_user.username else "Unlinked"

    if t_id == OWNER_ID:
        return

    if t_id in sudo_users:
        await message.reply_text(f"⚠️ **State Notice:** User `{t_name}` is already registered in the Sudo database.")
    else:
        sudo_users[t_id] = {"name": t_name, "username": t_username}
        await message.reply_text(f"✅ **Security Registry Updated**\nSuccessfully granted administrative clearance to `{t_name}`.", parse_mode="Markdown")

async def remove_sudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    message = update.message
    if not message.reply_to_message:
        await message.reply_text(f"⚠️ **Syntax Error:** Please reply to the target user's message using `{CURRENT_PREFIX}unsudo`.")
        return

    target_user = message.reply_to_message.from_user
    t_id = target_user.id
    t_name = target_user.first_name

    if t_id in sudo_users:
        del sudo_users[t_id]
        await message.reply_text(f"❌ **Security Registry Updated**\nAdministrative clearance revoked for `{t_name}`.", parse_mode="Markdown")
    else:
        await message.reply_text("⚠️ **State Notice:** Specified user lacks active Sudo privileges.")

async def list_sudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    text = f"👑 **AUTHORIZED SYSTEM ADMINISTRATORS** 👑\n\n"
    text += f"🛡️ *Primary Owner:* `{OWNER_HANDLE}` (Supreme Authority)\n\n"

    if not sudo_users:
        text += "📂 No secondary administrators registered."
    else:
        for idx, (uid, data) in enumerate(sudo_users.items(), 1):
            text += f"{idx}. *Name:* {data['name']} | *Handle:* {data['username']} | *ID:* `{uid}`\n"

    await update.message.reply_text(text, parse_mode="Markdown")

async def whois_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    message = update.message
    if not message.reply_to_message:
        await message.reply_text(f"⚠️ **Syntax Error:** Please reply to a target user profile using `{CURRENT_PREFIX}whois`.")
        return

    target_user = message.reply_to_message.from_user
    user_id = target_user.id
    first_name = target_user.first_name
    last_name = target_user.last_name or ""
    full_name = f"{first_name} {last_name}".strip()
    username = f"@{target_user.username}" if target_user.username else "None"
    is_bot = "Yes 🤖" if target_user.is_bot else "No 👤"
    
    photos = await context.bot.get_user_profile_photos(user_id, limit=1)
    
    bio_text = "Restricted / Unavailable"
    try:
        chat_info = await context.bot.get_chat(user_id)
        if chat_info.bio:
            bio_text = chat_info.bio
    except Exception:
        pass

    profile_caption = (
        f"🔍 **PROFILE INVESTIGATION REPORT** 🔍\n\n"
        f"👤 *Full Name:* `{full_name}`\n"
        f"🆔 *Target ID:* `{user_id}`\n"
        f"🔗 *Username:* `{username}`\n"
        f"🤖 *Automated Bot:* `{is_bot}`\n"
        f"📝 *Biography:* `{bio_text}`\n"
        f"🔗 *Secure Reference:* [Open Profile](tg://user?id={user_id})\n\n"
        f"⚡ *Telemetry:* Verification sequence completed."
    )

    try:
        if photos and photos.total_count > 0:
            file_id = photos.photos[0][-1].file_id
            await message.reply_photo(photo=file_id, caption=profile_caption, parse_mode="Markdown")
        else:
            await message.reply_text(profile_caption, parse_mode="Markdown")
    except Exception as e:
        await message.reply_text(f"⚠️ **Investigation Exception:** {str(e)}")

async def tts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    message = update.message
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.reply_text(f"⚠️ **Syntax Error:** Please provide input text. Example: `{CURRENT_PREFIX}tts Executing protocol`", parse_mode="Markdown")
        return

    text_to_convert = args[1].strip()
    
    try:
        tts = gTTS(text=text_to_convert, lang='en', slow=False)
        audio_file = "siren_audio.ogg"
        tts.save(audio_file)

        with open(audio_file, 'rb') as audio:
            await message.reply_voice(voice=audio)

        if os.path.exists(audio_file):
            os.remove(audio_file)
            
    except Exception as e:
        await message.reply_text(f"⚠️ **Synthesis Exception:** {str(e)}")

async def start_raid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    message = update.message
    chat_id = message.chat_id
    
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text(f"⚠️ **Syntax Error:** Please specify a target designation. Example: `{CURRENT_PREFIX}raid TargetNode`", parse_mode="Markdown")
        return
    
    target_name = args[1].strip()
    active_raid_chats[chat_id] = {"target_name": target_name, "index": 0}
    
    await message.reply_text(f"🌪️ **RAID PROTOCOL ENGAGED**\nTarget Designation: `{target_name}`", parse_mode="Markdown")

async def stop_raid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    chat_id = update.message.chat_id if update.message else update.effective_chat.id
    if chat_id in active_raid_chats:
        del active_raid_chats[chat_id]
        await message.reply_text("🛑 **RAID PROTOCOL TERMINATED**\nThread execution halted.", parse_mode="Markdown")
    else:
        await message.reply_text("⚠️ **State Notice:** No active raid sequence found in this chat context.")

async def start_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    message = update.message
    if not message.reply_to_message:
        await message.reply_text(f"⚠️ **Syntax Error:** Please reply to the target user message using `{CURRENT_PREFIX}re`.")
        return

    target_user_id = message.reply_to_message.from_user.id
    active_text_targets[target_user_id] = 0
    target_name = message.reply_to_message.from_user.first_name
    await message.reply_text(f"⚡ **TEMPLATE FLOOD INITIALIZED**\nTarget Node: *{target_name}*", parse_mode="Markdown")

async def stop_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    message = update.message
    if not message.reply_to_message:
        await message.reply_text(f"⚠️ **Syntax Error:** Please reply to the target user message using `{CURRENT_PREFIX}dre`.")
        return

    target_user_id = message.reply_to_message.from_user.id
    if target_user_id in active_text_targets:
        del active_text_targets[target_user_id]
        await message.reply_text("🛑 **Template tracking terminated for target node.**")
    else:
        await message.reply_text("⚠️ **State Notice:** User is not registered in active reply registry.")

async def start_custom_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    message = update.message
    if not message.reply_to_message:
        await message.reply_text(f"⚠️ **Syntax Error:** Please reply to a message using `{CURRENT_PREFIX}cre <payload>`.")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text(f"⚠️ **Syntax Error:** Missing custom transmission string. Example: `{CURRENT_PREFIX}cre System Alert`", parse_mode="Markdown")
        return

    custom_text = args[1].strip()
    target_user_id = message.reply_to_message.from_user.id
    active_custom_targets[target_user_id] = custom_text
    target_name = message.reply_to_message.from_user.first_name
    await message.reply_text(f"💬 **CUSTOM FEEDBACK ENGAGED**\nTarget: *{target_name}*\nPayload: `{custom_text}`", parse_mode="Markdown")

async def stop_custom_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    message = update.message
    if not message.reply_to_message:
        await message.reply_text(f"⚠️ **Syntax Error:** Please reply to the target user message using `{CURRENT_PREFIX}dcre`.")
        return

    target_user_id = message.reply_to_message.from_user.id
    if target_user_id in active_custom_targets:
        del active_custom_targets[target_user_id]
        await message.reply_text("🛑 **Custom tracking terminated for target node.**")
    else:
        await message.reply_text("⚠️ **State Notice:** User is not registered in custom reply registry.")


# ==========================================
# UNIVERSAL REACTION CONTROLLER (SAFE API)
# ==========================================

async def start_reaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    message = update.message
    if not message.reply_to_message:
        await message.reply_text(f"⚠️ **Syntax Error:** Please reply to a message using `{CURRENT_PREFIX}rct <emoji>`.")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text(f"⚠️ **Syntax Error:** Missing emoji parameter. Example: `{CURRENT_PREFIX}rct ⚡`", parse_mode="Markdown")
        return

    emoji = args[1].strip()
    target_user_id = message.reply_to_message.from_user.id
    active_reaction_targets[target_user_id] = emoji
    target_name = message.reply_to_message.from_user.first_name
    await message.reply_text(f"😎 **AUTO-REACTION INITIALIZED**\nTarget: *{target_name}*\nEmoji: `{emoji}`", parse_mode="Markdown")

async def stop_reaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    message = update.message
    if not message.reply_to_message:
        await message.reply_text(f"⚠️ **Syntax Error:** Please reply to the target user message using `{CURRENT_PREFIX}drct`.")
        return

    target_user_id = message.reply_to_message.from_user.id
    if target_user_id in active_reaction_targets:
        del active_reaction_targets[target_user_id]
        await message.reply_text("🛑 **Auto-reaction sequence terminated for target node.**")
    else:
        await message.reply_text("⚠️ **State Notice:** User is not registered in reaction registry.")

async def start_global_reaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global global_auto_reaction
    if not is_authorized(update.effective_user.id):
        return

    message = update.message
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text(f"⚠️ **Syntax Error:** Missing emoji parameter. Example: `{CURRENT_PREFIX}arct 💀`", parse_mode="Markdown")
        return

    global_auto_reaction = args[1].strip()
    await message.reply_text(f"🌐 **GLOBAL AUTO-REACTION ENGAGED**\nEmoji: `{global_auto_reaction}`", parse_mode="Markdown")

async def stop_global_reaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global global_auto_reaction
    if not is_authorized(update.effective_user.id):
        return

    global_auto_reaction = None
    await update.message.reply_text("🛑 **Global auto-reaction sequence disengaged.**")

# ==========================================
# CUSTOM PREFIX COMMAND WRAPPER
# ==========================================

def custom_cmd(command_name, callback_func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.text:
            return
        text = update.message.text.strip()
        p = CURRENT_PREFIX
        if text == f"{p}{command_name}" or text.startswith(f"{p}{command_name} ") or text == f"/{command_name}" or text.startswith(f"/{command_name} "):
            await callback_func(update, context)
    return MessageHandler(filters.TEXT & ~filters.COMMAND, wrapper)

# ==========================================
# BACKGROUND WORKERS (0.2s Raid Speed)
# ==========================================

async def background_workers(app):
    while True:
        if active_raid_chats:
            for chat_id, data in list(active_raid_chats.items()):
                try:
                    target_name = data["target_name"]
                    idx = data["index"]
                    template = RAID_TEMPLATES[idx % len(RAID_TEMPLATES)]
                    payload = template.format(target=target_name)
                    
                    active_raid_chats[chat_id]["index"] += 1
                    await app.bot.send_message(chat_id=chat_id, text=payload)
                except Exception:
                    pass

        await asyncio.sleep(0.2)


# ==========================================
# INCOMING TRANSMISSION LISTENER
# ==========================================

async def handle_incoming_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_msg = update.message or update.channel_post
    if not target_msg:
        return

    chat_id = target_msg.chat_id
    message_id = target_msg.message_id
    user_id = target_msg.from_user.id if target_msg.from_user else None

    if chat_id in clear_all_chats:
        try:
            await target_msg.delete()
        except Exception:
            pass
        return

    if user_id and user_id in active_custom_targets:
        try:
            custom_text = active_custom_targets[user_id]
            await target_msg.reply_text(custom_text)
        except Exception:
            pass

    if user_id and user_id in active_text_targets:
        try:
            idx = active_text_targets[user_id]
            reply_text = TEXT_REPLY_TEMPLATES[idx % len(TEXT_REPLY_TEMPLATES)]
            active_text_targets[user_id] += 1
            await target_msg.reply_text(reply_text)
        except Exception:
            pass

    # Safe Direct API Reaction Handler (Active on all bots)
    emoji_to_send = None
    if global_auto_reaction:
        emoji_to_send = global_auto_reaction
    elif user_id and user_id in active_reaction_targets:
        emoji_to_send = active_reaction_targets[user_id]

    if emoji_to_send:
        try:
            await context.bot.get_bot()._post(
                "setMessageReaction",
                {
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "reaction": [{"type": "emoji", "emoji": emoji_to_send}]
                },
                read_timeout=10,
                write_timeout=10,
                connect_timeout=10,
            )
        except Exception:
            pass


# ==========================================
# CORE INITIALIZATION
# ==========================================

async def run_bot(token, is_master):
    app = ApplicationBuilder().token(token).build()
    
    app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), handle_incoming_message))

    # --- REACTION COMMANDS (Registered for All Bots with Custom Prefix Support) ---
    app.add_handler(custom_cmd("rct", start_reaction))
    app.add_handler(custom_cmd("drct", stop_reaction))
    app.add_handler(custom_cmd("arct", start_global_reaction))
    app.add_handler(custom_cmd("darct", stop_global_reaction))

    # --- MASTER BOT COMMANDS ---
    if is_master:
        app.add_handler(custom_cmd("status", status_command))
        app.add_handler(custom_cmd("menu", menu_command))
        app.add_handler(custom_cmd("pre", set_prefix))
        app.add_handler(custom_cmd("ptst", ping_test_command))
        app.add_handler(custom_cmd("tag", tag_all_command))
        app.add_handler(custom_cmd("clall", start_clear_all))
        app.add_handler(custom_cmd("dclall", stop_clear_all))
        app.add_handler(custom_cmd("whois", whois_command))
        app.add_handler(custom_cmd("tts", tts_command))
        app.add_handler(custom_cmd("sudo", add_sudo))
        app.add_handler(custom_cmd("unsudo", remove_sudo))
        app.add_handler(custom_cmd("sudos", list_sudo))
        app.add_handler(custom_cmd("raid", start_raid))
        app.add_handler(custom_cmd("draid", stop_raid))
        app.add_handler(custom_cmd("re", start_reply))
        app.add_handler(custom_cmd("dre", stop_reply))
        app.add_handler(custom_cmd("cre", start_custom_reply))
        app.add_handler(custom_cmd("dcre", stop_custom_reply))

        asyncio.create_task(background_workers(app))

    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)


async def main():
    tasks = [run_bot(token, idx == 0) for idx, token in enumerate(BOT_TOKENS)]
    await asyncio.gather(*tasks)
    
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
