from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import asyncio
import os

# ----- CLEARLY SET KAR ------
api_id = 21344128
api_hash = "036b96696609bae556a1baee829d82fe"
target_chats = ["@Alise_xD_bot", "@dopayu_bot"]
forward_channel = "-1002620257061"
time_interval = 15
emoji = "✅"
# ----------------------------

app = Client("session", api_id, api_hash)

@app.on_message(filters.me & filters.regex(r'^\.time (\d+)$'))
async def change_timer(_, message):
    global time_interval
    new_time = int(message.matches[0].group(1))
    time_interval = new_time
    await message.reply(f"⏱ Timer updated: {time_interval} sec")

@app.on_message(filters.me & filters.document & filters.caption)
async def send_cards_from_file(client, message):
    command = message.caption.strip()

    # Download kar file ko
    file_path = await message.download()

    with open(file_path, 'r', encoding='utf-8') as file:
        cards = [line.strip() for line in file if line.strip()]

    if not cards:
        await message.reply("❌ File is empty.")
        os.remove(file_path)
        return

    await message.reply(f"🟢 Sending {len(cards)} cards with '{command}' every {time_interval}s.")

    for idx, card in enumerate(cards, 1):
        text = f"{command} {card}"
        for chat in target_chats:
            try:
                await client.send_message(chat, text)
                print(f"[{idx}/{len(cards)}] Sent to {chat}: {text}")
            except FloodWait as e:
                print(f"⏳ FloodWait: waiting {e.value}s")
                await asyncio.sleep(e.value)
                await client.send_message(chat, text)

        await asyncio.sleep(time_interval)

    await message.reply("✅ **All cards sent successfully!**")
    os.remove(file_path)

# ✅ Forward incoming messages containing ✅
@app.on_message(filters.incoming & filters.text & filters.regex(emoji))
async def forward_live_cards(client, message):
    try:
        await message.forward(forward_channel)
        print(f"🔄 Forwarded: {message.text}")
    except Exception as e:
        print(f"Error: {e}")

print("🚀 Userbot Running with All Features!")
app.run()
