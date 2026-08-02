import asyncio
import logging
import random
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

MASTER_TOKEN = "8666502260:AAG52YosLmCHkQvdY5_oSlpItsBy_zoiyjM"  # 
OWNER_ID = 7699820685                       

MENU_IMAGE_URL = "https://i.ibb.co/105277.jpg"  

SWIPE_BOT_TOKENS = [
    "8613761158:AAFi8xz7IumiRAgMTsRa2iAJAEpqgflY1bQ",
    "8994320628:AAFzf4YQvODJPngEqkPtbSAMIi3tisgE300",
    "8630777697:AAGojTI8wFR-ZONN-jKjjvwtlUepin_J0pk",
    "8616814880:AAEXTAzGoo2y_Nbg5yug7A-lJrXSBWCtxP0",
    "8070259728:AAEfdIZbcF-go6ZF8PC76noj77HjiAcM0Nw"
]

SWIPE_TEMPLATES_SW = [
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


SWIPE_TEMPLATES_SE = [
    "𝑭𝒐𝒐𝒍𝒔 𝒐𝒓 𝒇𝒍𝒂𝒕 𝒂𝒔 𝒑𝒖𝒔𝒔𝒚 𝒘𝒊𝒕𝒉 𝒂 𝒉𝒐𝒍𝒆 ☀️",
    " 𝑨𝒏𝒕𝒔 𝒊𝒏 𝒚𝒐𝒖𝒓 𝒂𝒔𝒔 🦂",
    " 𝑨 𝒑𝒆𝒓𝒔𝒐𝒏 𝒃𝒐𝒓𝒏 𝒇𝒓𝒐𝒎 𝒂 𝒍𝒐𝒔𝒕 𝒗𝒂𝒈𝒊𝒏𝒂 😏",
    " 𝑨 𝒅𝒊𝒓𝒕𝒚 𝒈𝒆𝒓𝒎 𝒐𝒇 𝒂 𝒅𝒊𝒓𝒕𝒚 𝒑𝒖𝒔𝒔𝒚 😂🖕🏻",
    " 𝑺𝒐𝒏 𝒐𝒇 𝒂 𝒉𝒐𝒈 😈",
    " 𝑺𝒘𝒆𝒆𝒕 𝒐𝒇 𝑳𝒊𝒛𝒂𝒓𝒅 𝒄𝒖𝒏𝒕𝒔 😆",
    " 𝑩𝒐𝒓𝒏 𝒃𝒚 𝒍𝒐𝒐𝒔𝒆 𝒅𝒊𝒄𝒌 🤣",
    " 𝑺𝒖𝒄𝒌 𝒎𝒚 𝒅𝒊𝒄𝒌 🖕",
    " 𝑺𝒐𝒏 𝒐𝒇 𝒃𝒊𝒕𝒄𝒉 🥺",
    " 𝒀𝒐𝒖 𝒍𝒐𝒐𝒌 𝒍𝒊𝒌𝒆 𝒎𝒚 𝒅𝒊𝒄𝒌 😢",
    "𝑺𝒐𝒏 𝒐𝒇 𝒃𝒊𝒕𝒄𝒉 🤬✌🏻",
    "𝑭𝒖𝒄𝒌 𝒚𝒐𝒖 𝒃𝒊𝒕𝒄𝒉 🪐",
    "𝑫𝒊𝒓𝒕𝒚 𝒂𝒔𝒔 💢",
    "𝑩𝒍𝒐𝒐𝒅𝒚 𝒘𝒉𝒐𝒓𝒆 ❄️"
]

SWIPE_TEMPLATES_SH = [
    "चलती है गाड़ी 🚔 चलता है घोड़ा 🐴 डाल दु क्या आपके Gand मैं Lowda 😂🖕🏻",
    " खली + आ = खाला 😂 क्या देख रहा 👀 तेरी माँ की चुत में bhala 🖕🏻",
    " प्यार मोहब्बत का खेल मुझे भी खेलना है , तेरी मा को लेटाकर मुझे भी पेल्ना है 😁🤗",
    " हिलाया हुआ सोडा 🍾 और तेरी माँ की चुत में Loडा 🌚",
    " भाग बसंती भाग siren वाले माँ चौदने अरे तेरी 🤣🔥",
    " तेरी माँ की chuchi माउंट everest 🏔️ से ऊँची 💀",
    " तेरी माँ की jhanto में हाथ डालके धीरे से fingering करदु तो रोकलेगा किया? 🤪",
    " सुन अगर तेरी माँ चोदके भाग जाऊंगा तो पकड़ पाएगा क्या ? 😵‍💫🔥",
    " Side हो तेरी maa चौदने Siren वाले अरे है 😁😜😱",
    " Ada पादा कौन पादा teri माँ chodunga सबसे ज्यादा 😅😝"
]

logging.basicConfig(
    format='%(asctime)s | SIREN v3.8 [%(levelname)s] -> %(message)s',
    level=logging.INFO
)

SYSTEM_INIT_TIMESTAMP = time.time()
sudo_authorized_operators = set()

active_targets_sw = {}
active_targets_se = {}
active_targets_sh = {}
active_targets_cw = {}
active_targets_shh = {}

def verify_operator_authorization(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in sudo_authorized_operators

async def execute_silent_cluster_dispatch(chat_id, message_id, textpayload_list, multiplier=5):
    for node_token in SWIPE_BOT_TOKENS:
        try:
            worker_application = Application.builder().token(node_token).build()
            async with worker_application:
                for iteration in range(multiplier):
                    selected_payload = random.choice(textpayload_list)
                    await worker_application.bot.send_message(
                        chat_id=chat_id,
                        text=selected_payload,
                        reply_to_message_id=message_id
                    )
                    await asyncio.sleep(random.uniform(0.15, 0.35))
        except Exception as system_exception:
            logging.error(f"Cluster node transmission failure encountered: {system_exception}")

async def handle_master_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not verify_operator_authorization(update.effective_user.id):
        return await update.message.reply_text("⚠️ <b>Access Denied:</b> Insufficient clearance.", parse_mode="HTML")

    screenshot_style_menu = (
        "⚡ <b>SIREN v3.8</b> ⚡\n"
        "<i>The Ghost in the Group</i>\n\n"
        "» Status: ONLINE\n"
        f"» Units Deployed: {len(SWIPE_BOT_TOKENS)}/5 Workers + 1 Master Gateway\n"
        "» Protocol: ULTRA SPEED (Dynamic Variety)\n"
        "» Prefix: !\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "💀 <b>TACTICAL SWIPE MODULES</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "<code>!sw</code> » Standard Dynamic Dispatch\n"
        "<code>!se</code> » Secondary Dynamic Dispatch\n"
        "<code>!sh</code> » Heavy Mass Saturation\n"
        "<code>!cw [text]</code> » Custom Payload Injection\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "🛑 <b>STOP MODULES (Deactivation)</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "<code>!dsw</code> » Stop Standard Swipe\n"
        "<code>!dse</code> » Stop Secondary Swipe\n"
        "<code>!dsh</code> » Stop Heavy Saturation\n"
        "<code>!dcw</code> » Stop Custom Payload\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "🔒 <b>SURVEILLANCE & UTILITY</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "<code>!shh</code> » Engage Auto-Deletion Lockdown\n"
        "<code>!bol</code> » Lift Auto-Deletion Lockdown\n"
        "<code>!purge</code> » Ledger Scrubbing Utility\n"
        "<code>!info</code> » Target Intelligence Dossier\n"
        "<code>!slist</code> » Detailed Sudo Operators List\n"
        "<code>!status</code> » System Diagnostics\n"
        "<code>!ping</code> » Cluster Latency Benchmark\n"
        "<code>!sudo</code> / <code>!undo</code> » Privilege Controls"
    )

    try:
        await update.message.reply_photo(photo=MENU_IMAGE_URL, caption=screenshot_style_menu, parse_mode="HTML")
    except Exception as e:
        await update.message.reply_text(screenshot_style_menu, parse_mode="HTML")

async def handle_sudo_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not verify_operator_authorization(update.effective_user.id):
        return await update.message.reply_text("⛔ <b>Access Denied:</b> Insufficient clearance.", parse_mode="HTML")

    if not sudo_authorized_operators:
        slist_report = (
            "🛡️ <b>SIREN v3.8 Sudo Operators Registry</b>\n"
            "────────────────────────────────────────\n"
            f"• <b>Root Owner ID:</b> <code>{OWNER_ID}</code>\n"
            "• <b>Delegated Sudo Users:</b> <i>None currently registered.</i>\n"
            "────────────────────────────────────────"
        )
    else:
        details_list = []
        for idx, sudo_id in enumerate(sudo_authorized_operators, start=1):
            try:
                chat_member = await context.bot.get_chat(sudo_id)
                name = chat_member.full_name
                username = f"@{chat_member.username}" if chat_member.username else "No Username"
                details_list.append(f"{idx}. <b>{name}</b> ({username})\n    🆔 ID: <code>{sudo_id}</code>")
            except Exception:
                details_list.append(f"{idx}. <b>Unknown User</b>\n    🆔 ID: <code>{sudo_id}</code>")
        
        formatted_sudo_entries = "\n".join(details_list)
        slist_report = (
            "🛡️ <b>SIREN v3.8 Sudo Operators Registry</b>\n"
            "────────────────────────────────────────\n"
            f"• <b>Root Owner ID:</b> <code>{OWNER_ID}</code>\n"
            f"• <b>Total Sudo Operators:</b> {len(sudo_authorized_operators)}\n\n"
            f"<b>Active Roster Details:</b>\n{formatted_sudo_entries}\n"
            "────────────────────────────────────────"
        )

    await update.message.reply_text(slist_report, parse_mode="HTML")

async def handle_system_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not verify_operator_authorization(update.effective_user.id): return
    uptime = int(time.time() - SYSTEM_INIT_TIMESTAMP)
    d, h, m, s = uptime // 86400, (uptime % 86400) // 3600, (uptime % 3600) // 60, uptime % 60
    await update.message.reply_text(f"📊 <b>SIREN v3.8 Status:</b> Online\n⏱️ <b>Uptime:</b> {d}d {h}h {m}m {s}s", parse_mode="HTML")

async def handle_network_ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not verify_operator_authorization(update.effective_user.id): return
    msg = await update.message.reply_text("🏓 Measuring cluster latency...", parse_mode="HTML")
    t1 = time.time()
    await context.bot.get_me()
    ml = int((time.time() - t1) * 1000)
    await msg.edit_text(f"🏓 <b>Master Gateway Latency:</b> <code>{ml} ms</code> [Cluster Optimal]", parse_mode="HTML")

async def handle_user_intelligence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not verify_operator_authorization(update.effective_user.id): return
    sub = update.message.reply_to_message.from_user if update.message.reply_to_message else update.effective_user
    photos = await context.bot.get_user_profile_photos(user_id=sub.id, limit=1)
    dossier = f"🔍 <b>DOSSIER:</b> {sub.full_name} (<code>{sub.id}</code>)"
    if photos and photos.total_count > 0:
        await update.message.reply_photo(photo=photos.photos[0][-1].file_id, caption=dossier, parse_mode="HTML")
    else:
        await update.message.reply_text(dossier, parse_mode="HTML")

async def handle_chat_purge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not verify_operator_authorization(update.effective_user.id) or not update.message.reply_to_message: return
    chat_id, start_id, end_id = update.message.chat_id, update.message.reply_to_message.message_id, update.message.message_id
    try: await update.message.delete()
    except: pass
    count = 0
    for mid in range(start_id, end_id + 1):
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=mid)
            count += 1
            await asyncio.sleep(0.08)
        except: pass
    noti = await context.bot.send_message(chat_id=chat_id, text=f"🧹 Purged <b>{count}</b> messages.", parse_mode="HTML")
    await asyncio.sleep(3)
    try: await noti.delete()
    except: pass

async def grant_sudo_privileges(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID or not update.message.reply_to_message: return
    sub = update.message.reply_to_message.from_user
    sudo_authorized_operators.add(sub.id)
    await update.message.reply_text(f"👑 <b>Access Granted:</b> {sub.full_name}", parse_mode="HTML")

async def revoke_sudo_privileges(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID or not update.message.reply_to_message: return
    sub = update.message.reply_to_message.from_user
    if sub.id in sudo_authorized_operators:
        sudo_authorized_operators.remove(sub.id)
        await update.message.reply_text(f"🚫 <b>Access Revoked:</b> {sub.full_name}", parse_mode="HTML")

async def dispatch_standard_swipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not verify_operator_authorization(update.effective_user.id) or not update.message.reply_to_message: return
    active_targets_sw.setdefault(update.effective_user.id, set()).add(update.message.reply_to_message.from_user.id)
    await update.message.reply_text("🚀 <b>[!sw] Active (Dynamic Cluster Replies).</b>", parse_mode="HTML")
    asyncio.create_task(execute_silent_cluster_dispatch(update.message.chat_id, update.message.reply_to_message.message_id, SWIPE_TEMPLATES_SW, 5))

async def terminate_standard_swipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if verify_operator_authorization(update.effective_user.id):
        active_targets_sw.pop(update.effective_user.id, None)
        await update.message.reply_text("🛑 <b>[!dsw] Terminated.</b>", parse_mode="HTML")

async def dispatch_secondary_swipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not verify_operator_authorization(update.effective_user.id) or not update.message.reply_to_message: return
    active_targets_se.setdefault(update.effective_user.id, set()).add(update.message.reply_to_message.from_user.id)
    await update.message.reply_text("🚀 <b>[!se] Active (Dynamic Cluster Replies).</b>", parse_mode="HTML")
    asyncio.create_task(execute_silent_cluster_dispatch(update.message.chat_id, update.message.reply_to_message.message_id, SWIPE_TEMPLATES_SE, 5))

async def terminate_secondary_swipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if verify_operator_authorization(update.effective_user.id):
        active_targets_se.pop(update.effective_user.id, None)
        await update.message.reply_text("🛑 <b>[!dse] Terminated.</b>", parse_mode="HTML")

async def dispatch_heavy_swipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not verify_operator_authorization(update.effective_user.id) or not update.message.reply_to_message: return
    active_targets_sh.setdefault(update.effective_user.id, set()).add(update.message.reply_to_message.from_user.id)
    await update.message.reply_text("🔥 <b>[!sh] Heavy Saturation Active.</b>", parse_mode="HTML")
    asyncio.create_task(execute_silent_cluster_dispatch(update.message.chat_id, update.message.reply_to_message.message_id, SWIPE_TEMPLATES_SH, 5))

async def terminate_heavy_swipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if verify_operator_authorization(update.effective_user.id):
        active_targets_sh.pop(update.effective_user.id, None)
        await update.message.reply_text("🛑 <b>[!dsh] Terminated.</b>", parse_mode="HTML")

async def dispatch_custom_swipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not verify_operator_authorization(update.effective_user.id) or not update.message.reply_to_message or not context.args: return
    active_targets_cw.setdefault(update.effective_user.id, set()).add(update.message.reply_to_message.from_user.id)
    txt = " ".join(context.args)
    await update.message.reply_text(f"🚀 <b>[!cw] Dispatched:</b> <code>{txt}</code>", parse_mode="HTML")
    asyncio.create_task(execute_silent_cluster_dispatch(update.message.chat_id, update.message.reply_to_message.message_id, [txt], 5))

async def terminate_custom_swipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if verify_operator_authorization(update.effective_user.id):
        active_targets_cw.pop(update.effective_user.id, None)
        await update.message.reply_text("🛑 <b>[!dcw] Terminated.</b>", parse_mode="HTML")

async def engage_autodelete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not verify_operator_authorization(update.effective_user.id) or not update.message.reply_to_message: return
    active_targets_shh.setdefault(update.effective_user.id, set()).add(update.message.reply_to_message.from_user.id)
    await update.message.reply_text("🗑️ <b>[!shh] Lockdown Engaged.</b>", parse_mode="HTML")

async def disengage_autodelete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not verify_operator_authorization(update.effective_user.id) or not update.message.reply_to_message: return
    op, target = update.effective_user.id, update.message.reply_to_message.from_user.id
    if op in active_targets_shh and target in active_targets_shh[op]:
        active_targets_shh[op].remove(target)
        await update.message.reply_text("✅ <b>[!bol] Lockdown Lifted.</b>", parse_mode="HTML")

async def process_incoming_surveillance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user: return
    sid, cid, mid = update.message.from_user.id, update.message.chat_id, update.message.message_id

    for op, targets in active_targets_shh.items():
        if sid in targets:
            try: await context.bot.delete_message(chat_id=cid, message_id=mid)
            except: pass
            return

    for op, targets in active_targets_sh.items():
        if sid in targets: asyncio.create_task(execute_silent_cluster_dispatch(cid, mid, SWIPE_TEMPLATES_SH, 5))
    for op, targets in active_targets_sw.items():
        if sid in targets: asyncio.create_task(execute_silent_cluster_dispatch(cid, mid, SWIPE_TEMPLATES_SW, 5))
    for op, targets in active_targets_se.items():
        if sid in targets: asyncio.create_task(execute_silent_cluster_dispatch(cid, mid, SWIPE_TEMPLATES_SE, 5))

def main():
    app = Application.builder().token(MASTER_TOKEN).build()

    app.add_handler(CommandHandler("m", handle_master_menu))
    app.add_handler(CommandHandler("status", handle_system_status))
    app.add_handler(CommandHandler("ping", handle_network_ping))
    app.add_handler(CommandHandler("info", handle_user_intelligence))
    app.add_handler(CommandHandler("purge", handle_chat_purge))
    app.add_handler(CommandHandler("slist", handle_sudo_list))
    
    app.add_handler(CommandHandler("sudo", grant_sudo_privileges))
    app.add_handler(CommandHandler("undo", revoke_sudo_privileges))
    
    app.add_handler(CommandHandler("sw", dispatch_standard_swipe))
    app.add_handler(CommandHandler("dsw", terminate_standard_swipe))
    app.add_handler(CommandHandler("se", dispatch_secondary_swipe))
    app.add_handler(CommandHandler("dse", terminate_secondary_swipe))
    app.add_handler(CommandHandler("sh", dispatch_heavy_swipe))
    app.add_handler(CommandHandler("dsh", terminate_heavy_swipe))
    app.add_handler(CommandHandler("cw", dispatch_custom_swipe))
    app.add_handler(CommandHandler("dcw", terminate_custom_swipe))
    
    app.add_handler(CommandHandler("shh", engage_autodelete))
    app.add_handler(CommandHandler("bol", disengage_autodelete))
    
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, process_incoming_surveillance))

    logging.info("SIREN v3.8 Master & Worker Framework initialized successfully.")
    app.run_polling()

if __name__ == "__main__":
    main()
