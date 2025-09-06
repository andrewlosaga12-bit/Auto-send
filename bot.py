import discord
import asyncio

# === KONFIGURASI ===
TOKEN = "ISI_TOKEN_DISCORD_BOT"
MESSAGE = "Halo semua! 🎉 Pesan otomatis dari bot."
DELAY = 2  # Detik antar-pesan
MAX_CHANNELS = 50  # Maksimal jumlah channel

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot {client.user} sudah online!")
    total_sent = 0
    for guild in client.guilds:
        for channel in guild.text_channels:
            if total_sent >= MAX_CHANNELS:
                print("⚠️ Batas 50 channel tercapai.")
                await client.close()
                return
            try:
                await channel.send(MESSAGE)
                print(f"✅ Berhasil kirim ke: #{channel.name} di {guild.name}")
                total_sent += 1
                await asyncio.sleep(DELAY)  # Anti-limit
            except Exception as e:
                print(f"❌ Gagal kirim ke {channel.name}: {e}")
    print("🎉 Semua pesan terkirim!")
    await client.close()

client.run(TOKEN)
