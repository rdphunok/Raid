import asyncio
import logging
import random
import time
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from telegram.request import HTTPXRequest

# --- SYSTEM CONFIGURATION ARCHITECTURE ---
MASTER_TOKEN = "8666502260:AAG52YosLmCHkQvdY5_oSlpItsBy_zoiyjM"  # Primary Master Gateway Token[span_1](start_span)[span_1](end_span)
OWNER_ID = 7699820685                        # Root Administrator User ID[span_2](start_span)[span_2](end_span)

# Local Image File Name (script ke sath folder mein menu.jpg honi chahiye)[span_3](start_span)[span_3](end_span)
MENU_IMAGE_PATH = "menu.jpg"  

# 5 Worker Nodes Pool (Background Silent Execution Engines)[span_4](start_span)[span_4](end_span)
SWIPE_BOT_TOKENS = [
    "8613761158:AAFi8xz7IumiRAgMTsRa2iAJAEpqgflY1bQ",
    "8994320628:AAFzf4YQvODJPngEqkPtbSAMIi3tisgE300",
    "8630777697:AAGojTI8wFR-ZONN-jKjjvwtlUepin_J0pk",
    "8616814880:AAEXTAzGoo2y_Nbg5yug7A-lJrXSBWCtxP0",
    "8070259728:AAEfdIZbcF-go6ZF8PC76noj77HjiAcM0Nw"
]

# --- DYNAMIC RANDOMIZED MESSAGE POOLS ---[span_5](start_span)[span_5](end_span)
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
    "ᴛ𝐄ʀ𝐈 𝐌𝐚𝐚 𝘒𝘪 𝘾𝙪#'", # (agar short rakhna ho toh baaki pools same rehne de)
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
    custom_req = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
    for node_token in SWIPE_BOT_TOKENS:
        try:
            worker_application = Application.builder().token(node_token).request(custom_req).build()
            async with worker_application:
                for iteration in range(multiplier):
                    selected_payload = random.choice(textpayload_list)
                    await worker_application.bot.send_message(
                        chat_id=chat_id,
                        text=selected_payload,
                        reply_to_message_id=message_id
                    )
                    await asyncio.sleep(0.3)
        except Exception as system_exception:
            logging.error(f"Cluster node transmission failure encountered: {system_exception}")

# --- MASTER ROUTER FOR SLASH PREFIX (/) ---
async def process_custom_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    text = update.message.text.strip()
    if not text.startswith("/"):
        return await process_incoming_surveillance(update, context)

    parts = text.split()
    cmd = parts[0][1:].lower()
    args = parts[1:]
    
    operator_id = update.effective_user.id

    if cmd == "m":
        if not verify_operator_authorization(operator_id):
            return await update.message.reply_text("⚠️ <b>Access Denied:</b> Insufficient clearance.", parse_mode="HTML")
        
        screenshot_style_menu = (
            "⚡ <b>SIREN v3</b> ⚡\n"
            "» Status: ONLINE\n"
            f"» Units Deployed: {len(SWIPE_BOT_TOKENS)}/5 Workers + 1 Master Gateway\n"
            "» Protocol: ULTRA SPEED (Dynamic Variety)\n"
            "» Prefix: /\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "💀 <b>TACTICAL SWIPE MODULES</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "<code>/sw</code> » Standard Dynamic Dispatch\n"
            "<code>/se</code> » Secondary Dynamic Dispatch\n"
            "<code>/sh</code> » Heavy Mass Saturation\n"
            "<code>/cw [text]</code> » Custom Payload Injection\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "🛑 <b>STOP MODULES (Deactivation)</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "<code>/dsw</code> » Stop Standard Swipe\n"
            "<code>/dse</code> » Stop Secondary Swipe\n"
            "<code>/dsh</code> » Stop Heavy Saturation\n"
            "<code>/dcw</code> » Stop Custom Payload\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "🔒 <b>SURVEILLANCE & UTILITY</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "<code>/shh</code> » Engage Auto-Deletion Lockdown\n"
            "<code>/bol</code> » Lift Auto-Deletion Lockdown\n"
            "<code>/purge</code> » Ledger Scrubbing Utility\n"
            "<code>/info</code> » Target Intelligence Dossier\n"
            "<code>/slist</code> » Detailed Sudo Operators List\n"
            "<code>/status</code> » System Diagnostics\n"
            "<code>/ping</code> » Cluster Latency Benchmark\n"
            "<code>/sudo</code> / <code>/undo</code> » Privilege Controls"
        )
        
        try:
            if os.path.exists(MENU_IMAGE_PATH):
                with open(MENU_IMAGE_PATH, 'rb') as photo_file:
                    await update.message.reply_photo(photo=photo_file, caption=screenshot_style_menu, parse_mode="HTML")
            else:
                await update.message.reply_text(screenshot_style_menu, parse_mode="HTML")
        except Exception:
            await update.message.reply_text(screenshot_style_menu, parse_mode="HTML")

    elif cmd == "status":
        if not verify_operator_authorization(operator_id): return
        uptime = int(time.time() - SYSTEM_INIT_TIMESTAMP)
        d, h, m, s = uptime // 86400, (uptime % 86400) // 3600, (uptime % 3600) // 60, uptime % 60
        await update.message.reply_text(f"📊 <b>SIREN v3.8 Status:</b> Online\n⏱️ <b>Uptime:</b> {d}d {h}h {m}m {s}s", parse_mode="HTML")

    elif cmd == "ping":
        if not verify_operator_authorization(operator_id): return
        msg = await update.message.reply_text("🏓 Measuring cluster latency...", parse_mode="HTML")
        t1 = time.time()
        await context.bot.get_me()
        ml = int((time.time() - t1) * 1000)
        await msg.edit_text(f"🏓 <b>Master Gateway Latency:</b> <code>{ml} ms</code> [Cluster Optimal]", parse_mode="HTML")

    elif cmd == "info":
        if not verify_operator_authorization(operator_id): return
        sub = update.message.reply_to_message.from_user if update.message.reply_to_message else update.effective_user
        photos = await context.bot.get_user_profile_photos(user_id=sub.id, limit=1)
        dossier = f"🔍 <b>DOSSIER:</b> {sub.full_name} (<code>{sub.id}</code>)"
        if photos and photos.total_count > 0:
            await update.message.reply_photo(photo=photos.photos[0][-1].file_id, caption=dossier, parse_mode="HTML")
        else:
            await update.message.reply_text(dossier, parse_mode="HTML")

    elif cmd == "purge":
        if not verify_operator_authorization(operator_id) or not update.message.reply_to_message: return
        chat_id = update.message.chat_id
        start_id = update.message.reply_to_message.message_id
        end_id = update.message.message_id
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

    elif cmd == "slist":
        if not verify_operator_authorization(operator_id): return
        if not sudo_authorized_operators:
            slist_report = f"🛡️ <b>SIREN v3.8 Sudo Registry</b>\nRoot Owner ID: <code>{OWNER_ID}</code>\nNo active sudo users."
        else:
            details_list = []
            for idx, sudo_id in enumerate(sudo_authorized_operators, start=1):
                try:
                    chat_member = await context.bot.get_chat(sudo_id)
                    details_list.append(f"{idx}. <b>{chat_member.full_name}</b> (<code>{sudo_id}</code>)")
                except:
                    details_list.append(f"{idx}. ID: <code>{sudo_id}</code>")
            slist_report = f"🛡️ <b>Sudo Roster:</b>\n" + "\n".join(details_list)
        await update.message.reply_text(slist_report, parse_mode="HTML")

    elif cmd == "sudo":
        if operator_id != OWNER_ID or not update.message.reply_to_message: return
        sub = update.message.reply_to_message.from_user
        sudo_authorized_operators.add(sub.id)
        await update.message.reply_text(f"👑 <b>Access Granted:</b> {sub.full_name}", parse_mode="HTML")

    elif cmd == "undo":
        if operator_id != OWNER_ID or not update.message.reply_to_message: return
        sub = update.message.reply_to_message.from_user
        if sub.id in sudo_authorized_operators:
            sudo_authorized_operators.remove(sub.id)
            await update.message.reply_text(f"🚫 <b>Access Revoked:</b> {sub.full_name}", parse_mode="HTML")

    elif cmd == "sw":
        if not verify_operator_authorization(operator_id) or not update.message.reply_to_message: return
        active_targets_sw.setdefault(operator_id, set()).add(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("🚀 <b>[/sw] Active.</b>", parse_mode="HTML")
        asyncio.create_task(execute_silent_cluster_dispatch(update.message.chat_id, update.message.reply_to_message.message_id, SWIPE_TEMPLATES_SW, 5))

    elif cmd == "dsw":
        if verify_operator_authorization(operator_id):
            active_targets_sw.pop(operator_id, None)
            await update.message.reply_text("🛑 <b>[/dsw] Terminated.</b>", parse_mode="HTML")

    elif cmd == "se":
        if not verify_operator_authorization(operator_id) or not update.message.reply_to_message: return
        active_targets_se.setdefault(operator_id, set()).add(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("🚀 <b>[/se] Active.</b>", parse_mode="HTML")
        asyncio.create_task(execute_silent_cluster_dispatch(update.message.chat_id, update.message.reply_to_message.message_id, SWIPE_TEMPLATES_SE, 5))

    elif cmd == "dse":
        if verify_operator_authorization(operator_id):
            active_targets_se.pop(operator_id, None)
            await update.message.reply_text("🛑 <b>[/dse] Terminated.</b>", parse_mode="HTML")

    elif cmd == "sh":
        if not verify_operator_authorization(operator_id) or not update.message.reply_to_message: return
        active_targets_sh.setdefault(operator_id, set()).add(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("🔥 <b>[/sh] Heavy Saturation Active.</b>", parse_mode="HTML")
        asyncio.create_task(execute_silent_cluster_dispatch(update.message.chat_id, update.message.reply_to_message.message_id, SWIPE_TEMPLATES_SH, 5))

    elif cmd == "dsh":
        if verify_operator_authorization(operator_id):
            active_targets_sh.pop(operator_id, None)
            await update.message.reply_text("🛑 <b>[/dsh] Terminated.</b>", parse_mode="HTML")

    elif cmd == "cw":
        if not verify_operator_authorization(operator_id) or not update.message.reply_to_message or not args: return
        active_targets_cw.setdefault(operator_id, set()).add(update.message.reply_to_message.from_user.id)
        custom_txt = " ".join(args)
        await update.message.reply_text(f"🚀 <b>[/cw] Dispatched:</b> <code>{custom_txt}</code>", parse_mode="HTML")
        asyncio.create_task(execute_silent_cluster_dispatch(update.message.chat_id, update.message.reply_to_message.message_id, [custom_txt], 5))

    elif cmd == "dcw":
        if verify_operator_authorization(operator_id):
            active_targets_cw.pop(operator_id, None)
            await update.message.reply_text("🛑 <b>[/dcw] Terminated.</b>", parse_mode="HTML")

    elif cmd == "shh":
        if not verify_operator_authorization(operator_id) or not update.message.reply_to_message: return
        active_targets_shh.setdefault(operator_id, set()).add(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("🗑️ <b>[/shh] Lockdown Engaged.</b>", parse_mode="HTML")

    elif cmd == "bol":
        if not verify_operator_authorization(operator_id) or not update.message.reply_to_message: return
        target_uid = update.message.reply_to_message.from_user.id
        if operator_id in active_targets_shh and target_uid in active_targets_shh[operator_id]:
            active_targets_shh[operator_id].remove(target_uid)
            await update.message.reply_text("✅ <b>[/bol] Lockdown Lifted.</b>", parse_mode="HTML")

async def process_incoming_surveillance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user: return
    sid, cid, mid = update.message.from_user.id, update.message.chat_id, update.message.message_id

    for _, targets in active_targets_shh.items():
        if sid in targets:
            try: await context.bot.delete_message(chat_id=cid, message_id=mid)
            except: pass
            return

    for _, targets in active_targets_sh.items():
        if sid in targets: asyncio.create_task(execute_silent_cluster_dispatch(cid, mid, SWIPE_TEMPLATES_SH, 5))
    for _, targets in active_targets_sw.items():
        if sid in targets: asyncio.create_task(execute_silent_cluster_dispatch(cid, mid, SWIPE_TEMPLATES_SW, 5))
    for _, targets in active_targets_se.items():
        if sid in targets: asyncio.create_task(execute_silent_cluster_dispatch(cid, mid, SWIPE_TEMPLATES_SE, 5))

def main():
    custom_req = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
    app = Application.builder().token(MASTER_TOKEN).request(custom_req).build()

    # Yahan ~filters.COMMAND ko hata diya hai taaki /m command block na ho
    app.add_handler(MessageHandler(filters.TEXT, process_custom_commands))

    logging.info("SIREN v3.8 Slash Prefix Framework initialized successfully.")
    app.run_polling()

if __name__ == "__main__":
    main()
