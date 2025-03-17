from pyrogram import Client, filters
import asyncio, os

# 🔥 Tera Mast Config 🔥
api_id = 21344128
api_hash = "036b96696609bae556a1baee829d82fe"
forward_channel = -1002620257061
time_interval = 20

app = Client("session", api_id, api_hash)
is_running = True

# ⏰ Timer Badalne ka jugaad
@app.on_message(filters.me & filters.regex(r'^\.time (\d+)$'))
async def change_timer(_, m):
    global time_interval
    time_interval = int(m.matches[0].group(1))
    await m.reply(f"⏱ Bhai, ab har {time_interval} second mein bhejunga! 🥳")

# 🛑 Sending rokne ka jugaad
@app.on_message(filters.me & filters.command("stop", "."))
async def stop_sending(_, m):
    global is_running
    is_running = False
    await m.reply("✋ Arre bhai ruk gaya mai, shanti rakh! 🥹")

# 📂 File se cards fenkne ka feature
@app.on_message(filters.me & filters.document & filters.caption & filters.regex(r'^/'))
async def file_se_bhejo(c, m):
    global is_running
    cmd = m.caption.strip()
    chat = m.chat.id
    path = await m.download()

    with open(path, 'r', encoding='utf-8') as f:
        cards = [l.strip() for l in f if l.strip()]

    if not cards:
        await m.reply("📂 Bhai empty file kyu de raha hai? 😒")
        os.remove(path)
        return

    is_running = True
    await m.reply(f"🚀 Bhai, '{cmd}' command ke sath {len(cards)} cards ki barish hogi ab! 💸")

    for card in cards:
        if not is_running: break
        await c.send_message(chat, f"{cmd} {card}")
        await asyncio.sleep(time_interval)

    msg = "✅ Kaam khatam bhai jaan! 🎉😎" if is_running else "⛔ Bhai tu ne rok diya beech mein! 🙄"
    await m.reply(msg)
    is_running = True
    os.remove(path)

# 💬 Direct message se cards
@app.on_message(filters.me & filters.text & filters.regex(r'^/'))
async def direct_bhejo(c, m):
    global is_running
    chat = m.chat.id
    lines = m.text.split("\n")
    if len(lines) < 2: return

    cmd, cards = lines[0], lines[1:]
    is_running = True

    await m.reply(f"🚀 Bhai '{cmd}' laga ke {len(cards)} cards udaane wala hu, ready ho ja! 🤩")

    for card in cards:
        if not is_running: break
        await c.send_message(chat, f"{cmd} {card}")
        await asyncio.sleep(time_interval)

    msg = "✅ Kaam ho gaya bhai! 🥳" if is_running else "⛔ Sending rok diya tune, kya yaar! 🤨"
    await m.reply(msg)
    is_running = True

# ✅ Edited Reply wale hits forward
@app.on_edited_message(filters.incoming & filters.text & filters.regex("✅"))
async def forward_hits(c, m):
    if m.reply_to_message and m.reply_to_message.from_user.is_self:
        await m.forward(forward_channel)
        print(f"💰 Hit pakda aur forward kiya: {m.text}")

print("🤖 Userbot ready hai mere bhai! Macha de! 🔥🚀")
app.run()
