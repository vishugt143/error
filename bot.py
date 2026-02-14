# Don't Remove Credit @teacher_slex
# Subscribe YouTube ƈɦǟռռɛʟ For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters, Client, errors
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users
from configs import cfg
import asyncio
import time
import os

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

#━━━━━━━━━━━━━━━━━━━━ HELPER ━━━━━━━━━━━━━━━━━━━━
def parse_post_link(link: str):
    parts = link.split("/")
    chat = parts[-2]
    msg_id = int(parts[-1])
    return chat, msg_id

#━━━━━━━━━━━━━━━━━━━━ JOIN REQUEST (AUTO APPROVE WITH 10s DELAY + LOG) ━━━━━━━━━━━━━━━━━━━━
@app.on_chat_join_request(filters.group | filters.channel)
async def approve(_, m: Message):
    op = m.chat
    user = m.from_user

    try:
        add_group(op.id)
        add_user(user.id)

        # 📝 Save ID + Time in log (one per line: user_id|timestamp)
        request_time = int(time.time())
        try:
            with open("log.txt", "a") as f:
                f.write(f"{user.id}|{request_time}\n")
        except Exception as e:
            print("Log write error:", e)

        # ⏳ Wait 10 seconds before approving
        await asyncio.sleep(10)

        # ✅ Attempt to approve the join request (bot must be admin with right)
        try:
            await app.approve_chat_join_request(op.id, user.id)
        except FloodWait as fw:
            # If flood wait, sleep required seconds then retry
            await asyncio.sleep(fw.value)
            try:
                await app.approve_chat_join_request(op.id, user.id)
            except Exception as e:
                print("Approve retry failed:", e)
        except errors.PeerIdInvalid:
            # invalid peer/user id; can't DM or approve
            print("PeerIdInvalid for user:", user.id)
        except Exception as e:
            print("Approve error:", e)

        # 📩 Send Approved Message (Updated Welcome Post)
        try:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "👉Click & Download Fast👈",
                            url="https://t.me/request_accept0_bot?start=welcome"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "👉 All Game Vip Hack 👈",
                            url="https://t.me/request_accept0_bot?start=welcome"
                        ),
                        InlineKeyboardButton(
                            "Claim ₹500 Gift Code 👈",
                            url="https://t.me/request_accept0_bot?start=welcome"
                        )
                    ]
                ]
            )

            await app.send_photo(
                chat_id=user.id,
                photo="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiv-gguuzwzVlA-vQj5a4fS3GCFZbzhRM3Qxwa20nu7afMl_R5PslCP82GXHJ5WiihJSSa_Xg45rYjB_dvWAb9RnUpbhVrsqdT9O1CkFAXgGRiOsRe2DXh8VcugC6-I-OnZ81wbPHbWCiGzRFvFau8sOFKslG6nPGeo3kqvZdfi__K9AIjhkq018iYbYYBe/s1600/523136.jpg",
                caption=f"Hello {user.mention} Bhai Kasie Ho ?",
                reply_markup=keyboard
            )

        except Exception as e:
            # can't DM user — ignore silently or log
            print("Send DM failed:", e)

        # ✅ Optional: Send configured POSTS to user (same as original behavior)
        for link in getattr(cfg, "POSTS", []):
            try:
                chat_id, msg_id = parse_post_link(link)
                await app.copy_message(
                    chat_id=user.id,
                    from_chat_id=chat_id,
                    message_id=msg_id
                )
                await asyncio.sleep(1)
            except Exception:
                # ignore individual copy errors
                pass

        # 🗑 Remove user from log after approval
        try:
            if os.path.exists("log.txt"):
                with open("log.txt", "r") as f:
                    lines = f.readlines()
                with open("log.txt", "w") as f:
                    for line in lines:
                        if not line.startswith(str(user.id) + "|"):
                            f.write(line)
        except Exception as e:
            print("Log cleanup error:", e)

    except Exception as e:
        # generic catch (keep bot alive)
        print("Join Handler Error:", e)

#━━━━━━━━━━━━━━━━━━━━ START COMMAND ━━━━━━━━━━━━━━━━━━━━
@app.on_message(filters.private & filters.command("start"))
async def start(_, m: Message):
    add_user(m.from_user.id)

    # NORMAL USER
    if m.from_user.id not in cfg.SUDO:
        await m.reply_text(
            "𝐁𝐇𝐀𝐈 𝐇𝐀𝐂𝐊 𝐒𝐄 𝐏𝐋𝐀𝐘 𝐊𝐑𝐎\n\n💸𝐏𝐑𝐎𝐅𝐈𝐓 𝐊𝐑𝐎🍻"
        )

        # send configured posts (same as original)
        for link in getattr(cfg, "POSTS", []):
            try:
                chat_id, msg_id = parse_post_link(link)
                await app.copy_message(
                    chat_id=m.from_user.id,
                    from_chat_id=chat_id,
                    message_id=msg_id
                )
                await asyncio.sleep(1)
            except Exception:
                pass
        return

    # ADMIN HOME (NO JOIN CHECK)
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🗯 ƈɦǟռռɛʟ", url="https://t.me/lnx_store"),
            InlineKeyboardButton("💬 Support", url="https://t.me/teacher_slex")
        ]]
    )

    await m.reply_photo(
        photo="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhsaR6kRdTPF2ZMEgmgSYjjXU6OcsJhkBe1EWtI1nfbOziINTYzxjlGCMSVh-KoH05Z8MpRWhVV9TIX_ykpjdeGqJ1atXy1TUqrVkohUxlykoZyl67EfMQppHoWYrdHmdi6FMcL9v-Vew2VtaWHWY_eGZt-GN057jLGvYj7UV49g0rXVxoDFXQAYxvaX1xP/s1280/75447.jpg",
        caption=(
            f"**🦊 Hello {m.from_user.mention}!**\n\n"
            "I'm an auto approve bot.\n"
            "I handle join requests & DM users.\n\n"
            "📢 Broadcast : /bcast\n"
            "📊 Users : /users\n\n"
            "__Powered By : @teacher_slex__"
        ),
        reply_markup=keyboard
    )

#━━━━━━━━━━━━━━━━━━━━ USERS COUNT ━━━━━━━━━━━━━━━━━━━━
@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def users_count(_, m: Message):
    u = all_users()
    g = all_groups()
    await m.reply_text(f"🙋 Users : `{u}`\n👥 Groups : `{g}`\n📊 Total : `{u+g}`")

#━━━━━━━━━━━━━━━━━━━━ BROADCAST COPY ━━━━━━━━━━━━━━━━━━━━
@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    status = await m.reply("⚡ Broadcasting...")
    ok = fail = 0
    for u in users.find():
        try:
            # will copy the replied message to each user id
            await m.reply_to_message.copy(u["user_id"])
            ok += 1
        except Exception:
            fail += 1
    await status.edit(f"✅ {ok} | ❌ {fail}")

#━━━━━━━━━━━━━━━━━━━━ 🚫 AUTO DELETE ILLEGAL BOT MSG (UNCHANGED) ━━━━━━━━━━━━━━━━━━━━
@app.on_message(filters.me)
async def auto_delete_illegal(_, m: Message):
    try:
        content = ""
        if m.text:
            content = m.text.lower()
        elif m.caption:
            content = m.caption.lower()

        for word in cfg.ILLEGAL_WORDS:
            if word.lower() in content:
                await asyncio.sleep(0.1)
                await m.delete()
                return
    except:
        pass

print("🤖 Bot is Alive!")
app.run()
