from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import asyncio

# ---------CONFIG----------
api_id = 21344128             # api_id yahan
api_hash = "036b96696609bae556a1baee829d82fe"   # api_hash yahan
target_chats = ["@Alise_xD_bot", "@dopayu_bot"]  # multiple chats/usernames
time_interval = 10           # seconds interval
# --------------------------

app = Client("session", api_id, api_hash)

@app.on_message(filters.me & filters.text)
async def custom_command_sender(client, message):
    lines = message.text.strip().split("\n")
    if len(lines) < 2:
        return await message.reply("❌ **Pehli line command aur baaki lines cards honi chahiye!**")

    command = lines[0].strip()
    cards = lines = lines = message.text.strip().split("\n")[1:]

    await message.reply(f"🟢 **Sending kar rha hu beta {len(cards)} cards to {len(target_chats)} chats!**")

    for idx, card in enumerate(cards, 1):
        text = f"{command} {card.strip()}"
        for chat in target_chats:
            try:
                await client.send_message(chat, text)
                print(f"[{idx}/{len(cards)}] Sent to {chat}: {text}")
            except FloodWait as e:
                print(f"⏳ FloodWait detected: waiting {e.value}s")
                await asyncio.sleep(e.value)
                await client.send_message(chat, text)

        await asyncio.sleep(time_interval)

    await message.reply("✅ **All cards sent successfully Chod Diya Hu!**")

print("🚀 Userbot Running...")
app.run()
