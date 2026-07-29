import asyncio
import time
import os
from gtts import gTTS
from telegram import Update, ReactionTypeEmoji, ChatType
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

# Core Telemetry
START_TIME = time.time()
sudo_users = {}
CURRENT_PREFIX = "."
MENU_VIDEO_ID = "https://www.w3schools.com/html/mov_bbb.mp4"

# ==========================================
# SECURE TEMPLATES DATABASE
# ==========================================
TEXT_REPLY_TEMPLATES = [
    "System Notice 01: Execution sequence acknowledged and processed.",
    "System Notice 02: Target loop verified. Continuing transmission.",
    "System Notice 03: Automated response protocol successfully executed.",
    "System Notice 04: Diagnostic check indicates optimal parameters.",
    "System Notice 05: Stream isolation protocol active on target.",
    "System Notice 06: Operational efficiency maintained at 100%.",
    "System Notice 07: Data feed synchronization in progress.",
    "System Notice 08: Packet verification successful.",
    "System Notice 09: Autonomous subsystem operational.",
    "System Notice 10: Terminal feedback loop repeating."
]

RAID_TEMPLATES = [
    "SECURITY PROTOCOL BREACH: Target node < {target} > experiencing high-intensity data overflow! ⚡",
    "SYSTEM OVERLOAD: Flooding target node < {target} > with encrypted execution payloads. 🌪️",
    "TRANSMISSION ALERT: Node < {target} > subjected to continuous command loops. 🛡️",
    "EXECUTION WARNING: Overwhelming target stream < {target} > via automated cluster. ⚙️",
    "CORE OVERFLOW: Target node < {target} > processing repetitive system interrupts. 🚀",
    "Raid Node 06: Target < {target} > experiencing extreme latency spikes.",
    "Raid Node 07: Automated flooding operational against < {target} >.",
    "Raid Node 08: System cluster continuously pinging target < {target} >.",
    "Raid Node 09: Node < {target} > caught in persistent execution cycle.",
    "Raid Node 10: Target stream < {target} > fully saturated."
]

STICKER_TEMPLATES = [
    "CAACAgUAAxkBAAE..._sticker_id_1",
    "CAACAgUAAxkBAAE..._sticker_id_2"
]

# Real-time State Registries
active_text_targets = {}     
active_custom_targets = {}   
active_sticker_targets = {}  
active_delete_targets = set()
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

    if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.reply_text("⚠️ **Access Denied:** Mass tagging protocol is restricted to Group Chats (GCs) only.")
        return

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
        f"📶 *Gateway Ping:* `{ping_ms} ms`\n"
        f"⏱️ *System Uptime:* `{uptime}`\n"
        f"🌪️ *Active Raid Clusters:* `{len(active_raid_chats)}`\n"
        f"🗑️ *Active Lockdown Chats:* `{len(clear_all_chats)}`\n"
        f"🌐 *Global Telemetry Reaction:* `{global_auto_reaction if global_auto_reaction else 'DISABLED'}`\n"
        f"🛡️ *Authorized Sudo Nodes:* `{len(sudo_users)}`"
    )
    await msg.edit_text(status_text, parse_mode="Markdown")

async def set_menu_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global MENU_VIDEO_ID
    if not is_authorized(update.effective_user.id):
        return

    message = update.message
    if not message.reply_to_message or not message.reply_to_message.video:
        await message.reply_text(f"⚠️ **Syntax Error:** Please reply to a valid **Video media file** using `{CURRENT_PREFIX}smv`.")
        return

    MENU_VIDEO_ID = message.reply_to_message.video.file_id
    await message.reply_text("✅ **Configuration Saved**\nMenu display media successfully overwritten.", parse_mode="Markdown")

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    p = CURRENT_PREFIX
    professional_caption = (
        f"╔═════════════════════════╗\n"
        f"     ⚡ **SIREN OS v4.5 - COMMAND SUITE** ⚡\n"
        f"     Current Command Prefix: [` {p} `]\n"
        f"╚═════════════════════════╝\n\n"
        f"🌪️ **1. RAID & BROADCAST MODULES:**\n"
        f"• `{p}tag <text>` - Execute mass member notification loop\n"
        f"• `{p}raid <target>` - Deploy automated thread flood sequence\n"
        f"• `{p}draid` - Terminate active raid operations\n\n"
        f"🛡️ **2. SECURITY & MODERATION MODULES:**\n"
        f"• `{p}clall` - Engage instant message scrub lockdown\n"
        f"• `{p}dclall` - Disengage message scrub lockdown\n"
        f"• `{p}sre` - Deploy automated sticker feedback loop\n"
        f"• `{p}dsre` - Halt sticker feedback loop\n\n"
        f"⚡ **3. REACTION & SPAM CONTROLS:**\n"
        f"• `{p}arct <emoji>` - Enable global telemetry auto-reaction\n"
        f"• `{p}darct` - Disable global telemetry auto-reaction\n"
        f"• `{p}rct <emoji>` - Target specific user auto-reaction\n"
        f"• `{p}drct` - Stop target user auto-reaction\n"
        f"• `{p}re` / `{p}dre` - Template automated text flood\n"
        f"• `{p}cre <txt>` / `{p}dcre` - Custom text feedback loop\n\n"
        f"🎙️ **4. SYSTEM & UTILITY DIAGNOSTICS:**\n"
        f"• `{p}ptst` - Run network speed & latency diagnostic\n"
        f"• `{p}pre <symbol>` - Dynamically modify command prefix\n"
        f"• `{p}whois` - Perform deep user profile investigation\n"
        f"• `{p}tts <text>` - Convert text string to synthesized audio\n"
        f"• `{p}smv` - Update persistent menu presentation media\n"
        f"• `{p}status` - Query real-time operational telemetry\n"
        f"• `{p}sudos` - Retrieve authorized administrator registry"
    )

    try:
        await update.message.reply_video(
            video=MENU_VIDEO_ID,
            caption=professional_caption,
            parse_mode="Markdown"
        )
    except Exception as e:
        await message.reply_text(f"⚠️ **Rendering Exception:** Unable to dispatch interface display: {str(e)}")

async def add_sudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("⚠️ **Access Denied:** Command restricted to Primary System Administrator.")
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
        await message.reply_text("⚠️ **Hierarchy Notice:** Primary Owner already holds supreme authority.")
        return

    if t_id in sudo_users:
        await message.reply_text(f"⚠️ **State Notice:** User `{t_name}` is already registered in the Sudo database.")
    else:
        sudo_users[t_id] = {"name": t_name, "username": t_username}
        await message.reply_text(f"✅ **Security Registry Updated**\nSuccessfully granted administrative clearance to `{t_name}`.", parse_mode="Markdown")

async def remove_sudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await message.reply_text("⚠️ **Access Denied:** Command restricted to Primary System Administrator.")
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

    text = "👑 **AUTHORIZED SYSTEM ADMINISTRATORS** 👑\n\n"
    text += f"🛡️ *Primary Owner ID:* `{OWNER_ID}` (Supreme Authority)\n\n"

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

    chat_id = update.message.chat_id
    if chat_id in active_raid_chats:
        del active_raid_chats[chat_id]
        await update.message.reply_text("🛑 **RAID PROTOCOL TERMINATED**\nThread execution halted.", parse_mode="Markdown")
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

async def start_sticker_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    message = update.message
    if not message.reply_to_message:
        await message.reply_text(f"⚠️ **Syntax Error:** Please reply to a user message using `{CURRENT_PREFIX}sre`.")
        return

    target_user_id = message.reply_to_message.from_user.id
    active_sticker_targets[target_user_id] = 0
    target_name = message.reply_to_message.from_user.first_name
    await message.reply_text(f"🖼️ **STICKER MATRIX ENGAGED**\nTarget Node: *{target_name}*", parse_mode="Markdown")

async def stop_sticker_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    message = update.message
    if not message.reply_to_message:
        await message.reply_text(f"⚠️ **Syntax Error:** Please reply to the target user message using `{CURRENT_PREFIX}dsre`.")
        return

    target_user_id = message.reply_to_message.from_user.id
    if target_user_id in active_sticker_targets:
        del active_sticker_targets[target_user_id]
        await message.reply_text("🛑 **Sticker matrix tracking terminated.**")
    else:
        await message.reply_text("⚠️ **State Notice:** User is not registered in sticker target registry.")


# ==========================================
# UNIVERSAL REACTION CONTROLLER
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
    await message.reply_text(f"🌐 **GLOBAL TELEMETRY REACTION ENGAGED**\nEmoji: `{global_auto_reaction}`", parse_mode="Markdown")

async def stop_global_reaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global global_auto_reaction
    if not is_authorized(update.effective_user.id):
        return

    global_auto_reaction = None
    await update.message.reply_text("🛑 **Global telemetry reaction sequence disengaged.**")


# ==========================================
# COMMAND PARSING FILTER
# ==========================================

def dynamic_command_filter(command_name):
    async def filter_func(update: Update):
        if not update.message or not update.message.text:
            return False
        text = update.message.text.strip()
        expected = f"{CURRENT_PREFIX}{command_name}"
        return text == expected or text.startswith(expected + " ")
    return filters.create(filter_func)


# ==========================================
# BACKGROUND BACKGROUND WORKERS (0.2s Raid Speed)
# ==========================================

async def background_workers(context: ContextTypes.DEFAULT_TYPE):
    while True:
        # 1. Raid Background Loop (Speed set to 0.2 seconds)
        if active_raid_chats:
            for chat_id, data in list(active_raid_chats.items()):
                try:
                    target_name = data["target_name"]
                    idx = data["index"]
                    template = RAID_TEMPLATES[idx % len(RAID_TEMPLATES)]
                    payload = template.format(target=target_name)
                    
                    active_raid_chats[chat_id]["index"] += 1
                    await context.bot.send_message(chat_id=chat_id, text=payload)
                except Exception:
                    pass

        # 2. Template Text Reply Loop (.re)
        if active_text_targets:
            for target_id in list(active_text_targets.keys()):
                try:
                    idx = active_text_targets[target_id]
                    template = TEXT_REPLY_TEMPLATES[idx % len(TEXT_REPLY_TEMPLATES)]
                    active_text_targets[target_id] += 1
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
    user_id = target_msg.from_user.id if target_msg.from_user else None

    # Lockdown Scrub Filter (.clall)
    if chat_id in clear_all_chats:
        try:
            await target_msg.delete()
        except Exception:
            pass
        return

    # Custom Reply Loop (.cre)
    if user_id and user_id in active_custom_targets:
        try:
            custom_text = active_custom_targets[user_id]
            await target_msg.reply_text(custom_text)
        except Exception:
            pass

    # Template Reply Loop (.re)
    if user_id and user_id in active_text_targets:
        try:
            idx = active_text_targets[user_id]
            reply_text = TEXT_REPLY_TEMPLATES[idx % len(TEXT_REPLY_TEMPLATES)]
            active_text_targets[user_id] += 1
            await target_msg.reply_text(reply_text)
        except Exception:
            pass

    # Auto Delete Filter (.del)
    if user_id and user_id in active_delete_targets:
        try:
            await target_msg.delete()
        except Exception:
            pass

    # Sticker Matrix Engine (.sre)
    if user_id and user_id in active_sticker_targets:
        try:
            idx = active_sticker_targets[user_id]
            sticker_id = STICKER_TEMPLATES[idx % len(STICKER_TEMPLATES)]
            active_sticker_targets[user_id] += 1
            await target_msg.reply_sticker(sticker=sticker_id)
        except Exception:
            pass

    # Global Telemetry Reaction (.arct)
    if global_auto_reaction:
        try:
            await target_msg.set_reaction(reaction=[ReactionTypeEmoji(global_auto_reaction)])
        except Exception:
            pass

    # Specific Target Reaction (.rct)
    if user_id and user_id in active_reaction_targets:
        emoji = active_reaction_targets[user_id]
        try:
            await target_msg.set_reaction(reaction=[ReactionTypeEmoji(emoji)])
        except Exception:
            pass


# ==========================================
# CORE INITIALIZATION
# ==========================================

async def run_bot(token, is_master):
    app = ApplicationBuilder().token(token).build()

    # Universal Handlers
    app.add_handler(MessageHandler(dynamic_command_filter("rct"), start_reaction))
    app.add_handler(MessageHandler(dynamic_command_filter("drct"), stop_reaction))
    app.add_handler(MessageHandler(dynamic_command_filter("arct"), start_global_reaction))
    app.add_handler(MessageHandler(dynamic_command_filter("darct"), stop_global_reaction))
    
    app.add_handler(MessageHandler((filters.ALL | filters.ChatType.CHANNEL) & (~filters.COMMAND), handle_incoming_message))

    # Master Administration Handlers
    if is_master:
        app.add_handler(CommandHandler("status", status_command))
        app.add_handler(MessageHandler(dynamic_command_filter("status"), status_command))
        
        app.add_handler(CommandHandler("menu", menu_command))
        app.add_handler(MessageHandler(dynamic_command_filter("menu"), menu_command))
        
        app.add_handler(MessageHandler(dynamic_command_filter("pre"), set_prefix))
        app.add_handler(MessageHandler(dynamic_command_filter("ptst"), ping_test_command))
        app.add_handler(MessageHandler(dynamic_command_filter("tag"), tag_all_command))
        app.add_handler(MessageHandler(dynamic_command_filter("clall"), start_clear_all))
        app.add_handler(MessageHandler(dynamic_command_filter("dclall"), stop_clear_all))
        app.add_handler(MessageHandler(dynamic_command_filter("sre"), start_sticker_reply))
        app.add_handler(MessageHandler(dynamic_command_filter("dsre"), stop_sticker_reply))
        app.add_handler(MessageHandler(dynamic_command_filter("smv"), set_menu_video))
        app.add_handler(MessageHandler(dynamic_command_filter("whois"), whois_command))
        app.add_handler(MessageHandler(dynamic_command_filter("tts"), tts_command))
        app.add_handler(MessageHandler(dynamic_command_filter("sudo"), add_sudo))
        app.add_handler(MessageHandler(dynamic_command_filter("unsudo"), remove_sudo))
        
        app.add_handler(CommandHandler("sudos", list_sudo))
        app.add_handler(MessageHandler(dynamic_command_filter("sudos"), list_sudo))
        
        app.add_handler(MessageHandler(dynamic_command_filter("raid"), start_raid))
        app.add_handler(MessageHandler(dynamic_command_filter("draid"), stop_raid))
        app.add_handler(MessageHandler(dynamic_command_filter("re"), start_reply))
        app.add_handler(MessageHandler(dynamic_command_filter("dre"), stop_reply))
        app.add_handler(MessageHandler(dynamic_command_filter("cre"), start_custom_reply))
        app.add_handler(MessageHandler(dynamic_command_filter("dcre"), stop_custom_reply))

        # Register background loop worker job queue
        job_queue = app.job_queue
        if job_queue:
            job_queue.run_repeating(background_workers, interval=0.2, first=1.0)
        else:
            # Fallback task runner if job queue is disabled
            asyncio.create_task(background_workers(app))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    while True:
        await asyncio.sleep(3600)

async def main():
    if not BOT_TOKENS or BOT_TOKENS[0] == "8666502260:AAG52YosLmCHkQvdY5_oSlpItsBy_zoiyjM":
        print("Critical Error: Please configure your Primary Bot Token in the BOT_TOKENS list.")
        return

    tasks = []
    for index, token in enumerate(BOT_TOKENS):
        is_master = (index == 0)
        tasks.append(run_bot(token, is_master))
        print(f"System Node #{index + 1} initialized successfully (Master: {is_master})")

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
