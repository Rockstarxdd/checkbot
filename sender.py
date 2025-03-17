from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import asyncio
import os

# --------- CONFIG CLEARLY SET KAR ----------
api_id = 21344128
api_hash = "036b96696609bae556a1baee829d82fe"
target_chats = ["@Alise_xD_bot", "@dopayu_bot"]
forward_channel = "@vvgccdd345s566fmjh787g"
time_interval = 20
emoji = "✅"
# --------------------------------------------

app = Client("session", api_id, api_hash)

@app.on_message(filters.me & filters.regex(r'^\.time (\d+)$'))
async def change_timer(_, message):
    global time_interval
    time_interval = int(message.matches[0].group(1))
    await message.reply(f"⏱ Timer set to {time_interval} seconds.")

@app.on_message(filters.me & filters.document & filters.caption)
async def send_from_file(client, message):
    command = message.caption.strip()
    file_path = await message.download()

    with open(file_path, "r", encoding="utf-8") as f:
        cards = [line.strip() for line in f if line.strip()]

    if not cards:
        await message.reply("❌ File me koi cards nahi mile.")
        os.remove(file_path)
        return

    await message.reply(f"🟢 **Sending {len(cards)} cards with command '{command}' every {time_interval}s.**")

    for card in cards:
        text = f"{command} {card}"
        for chat in target_chats:
            try:
                await client.send_message(chat, text)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await client.send_message(chat, text)
        await asyncio.sleep(time_interval)

    await message.reply("✅ **Cards sending completed.**")
    os.remove(file_path)

@app.on_message(filters.me & filters.text & ~filters.regex(r'^\.time (\d+)$'))
async def custom_command_send(client, message):
    lines = message.text.split("\n")
    if len(lines) < 2:
        return

    cmd = lines[0].strip()
    cards = lines[1:]

    await message.reply(f"🟢 Sending {len(cards)} cards with '{cmd}' every {time_interval}s.")

    for card in cards:
        text = f"{cmd} {card.strip()}"
        for chat in target_chats:
            try:
                await client.send_message(chat, text)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await client.send_message(chat, text)
        await asyncio.sleep(time_interval)

    await message.reply("✅ **Cards sending completed.**")

@app.on_message(filters.incoming & filters.text & filters.regex(emoji))
async def auto_forward(client, message):
    try:
        await message.forward(forward_channel)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await message.forward(forward_channel)

print("🚀 Userbot Fully Running...")
app.run()
