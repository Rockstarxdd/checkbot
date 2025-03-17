from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import asyncio, os

# ⚙️ 𝐂𝐨𝐧𝐟𝐢𝐠 𝐚𝐫𝐞𝐚 - यहां अपनी डिटेल डालो 👇
api_id = 1234567  # 📝 API ID
api_hash = "api_hash_here"  # 🔑 API Hash
forward_channel = -1001234567890  # 📢 Channel/User ID जहां ✅ वाले भेजने हैं
time_interval = 20  # ⏳ डिफ़ॉल्ट टाइम इंटरवल (सेकंड्स)

app = Client("session", api_id, api_hash)
sending_active = True  # ✅ Sending state manage karne ke liye

# ⏰ टाइम चेंज करने की कमांड
@app.on_message(filters.me & filters.regex(r'^\.time (\d+)$'))
async def change_timer(_, message):
    global time_interval
    time_interval = int(message.matches[0].group(1))
    await message.reply(f"⏱ टाइम बदल दिया भाई! अब हर कार्ड के बीच {time_interval}s लगेगा। ✅")

# 🛑 रोकने की कमांड
@app.on_message(filters.me & filters.command("stop", prefixes="."))
async def stop_sending(_, message):
    global sending_active
    sending_active = False
    await message.reply("⛔ ठीक है भाई! Sending रोक दी है मैंने। ✋🙂")

# 📁 फाइल से कार्ड्स भेजना
@app.on_message(filters.me & filters.document & filters.caption & filters.regex(r'^/'))
async def send_from_file(client, message):
    global sending_active
    sending_active = True
    command = message.caption.strip()
    file_path = await message.download()
    chat_id = message.chat.id

    with open(file_path, "r", encoding="utf-8") as file:
        cards = [line.strip() for line in file if line.strip()]

    if not cards:
        await message.reply("❌ भाई! ये फ़ाइल तो खाली है। 🤷‍♂️")
        os.remove(file_path)
        return

    await message.reply(f"🚀 भाई, `{command}` कमांड के साथ {len(cards)} कार्ड्स भेज रहा हूं! 🃏🔥 हर {time_interval}s बाद।")

    for card in cards:
        if not sending_active:
            break
        text = f"{command} {card}"
        try:
            await client.send_message(chat_id, text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.send_message(chat_id, text)
        await asyncio.sleep(time_interval)

    final_msg = "✅ सारे कार्ड्स भेज दिए गए भाई! 🎉" if sending_active else "🛑 तूने भेजना रोक दिया था भाई! ✋🙂"
    await message.reply(final_msg)
    os.remove(file_path)
    sending_active = True

# 🃏 टेक्स्ट से कार्ड्स भेजना (only "/" वाली कमांड)
@app.on_message(filters.me & filters.text & filters.regex(r'^/'))
async def send_text_cards(client, message):
    global sending_active
    sending_active = True
    chat_id = message.chat.id
    lines = message.text.strip().split("\n")

    if len(lines) < 2:
        return

    command = lines[0].strip()
    cards = lines[1:]

    await message.reply(f"🚀 भाई, `{command}` के साथ {len(cards)} कार्ड्स भेज रहा हूं! 🎴 हर {time_interval}s बाद।")

    for card in cards:
        if not sending_active:
            break
        text = f"{command} {card}"
        try:
            await client.send_message(chat_id, text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.send_message(chat_id, text)
        await asyncio.sleep(time_interval)

    final_msg = "✅ सारे कार्ड्स भेज दिए गए भाई! 🎉" if sending_active else "🛑 तूने भेजना रोक दिया था भाई! ✋🙂"
    await message.reply(final_msg)
    sending_active = True

# ✅ वाले हिट्स फॉरवर्ड करना
@app.on_message(filters.incoming & filters.text & filters.regex("✅"))
async def forward_hits(client, message):
    try:
        await message.forward(forward_channel)
        print(f"🔄 Forwarded: {message.text}")
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await message.forward(forward_channel)

# 🚀 स्टार्ट मेसेज
print("🤖✨ तेरा मॉडर्न Userbot तैयार है भाई! 🚀")
app.run()
