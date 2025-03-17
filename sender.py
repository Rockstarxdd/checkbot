from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import asyncio

# ---------- CONFIG ----------
api_id = 21344128  # apna API_ID daal
api_hash = "036b96696609bae556a1baee829d82fe"  # apna API_HASH daal
target_chat = "username_or_chat_id"  # target chat ka username ya id
time_interval = 20  # seconds gap
# ----------------------------

app = Client("session", api_id, api_hash)

@app.on_message(filters.me & filters.text)
async def custom_command_sender(client, message):
    lines = message.text.strip().split("\n")
    if len(lines) < 2:
        return  # agar command ke sath cards nahi mile, to kuch nahi karega

    command = lines[0].strip()
    cards = lines[1:]

    await message.reply(f"🟢 **Sending {len(cards)} cards with '{command}' every {time_interval}s.**")

    for idx, card in enumerate(cards, 1):
        text = f"{command} {card.strip()}"
        try:
            await client.send_message(target_chat, text)
            print(f"[{idx}/{len(cards)}] Sent: {text}")
        except FloodWait as e:
            print(f"⏳ FloodWait: waiting {e.value}s")
            await asyncio.sleep(e.value)
            await client.send_message(target_chat, text)

        await asyncio.sleep(time_interval)

    await message.reply("✅ **All cards sent successfully!**")

print("🚀 Userbot chal raha hai...")
app.run()
