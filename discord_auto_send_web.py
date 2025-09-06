import discord
import asyncio
import threading
from flask import Flask, render_template_string, request

# ======= Template HTML =======
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Discord Auto Sender</title>
    <style>
        body { font-family: Arial; background-color: #222; color: white; text-align: center; }
        form { margin-top: 50px; }
        input, textarea {
            width: 300px; padding: 10px; margin: 10px;
            border: none; border-radius: 5px;
        }
        button {
            padding: 10px 20px; background-color: #5865F2;
            color: white; border: none; border-radius: 5px;
            cursor: pointer;
        }
        button:hover { background-color: #4752C4; }
    </style>
</head>
<body>
    <h1>Discord Auto Sender Bot</h1>
    <form method="POST">
        <input type="text" name="token" placeholder="Masukkan Discord Bot Token" required><br>
        <textarea name="message" placeholder="Pesan yang akan dikirim" required></textarea><br>
        <input type="number" name="delay" placeholder="Delay antar pesan (detik)" value="2" required><br>
        <input type="number" name="max_channels" placeholder="Maksimal channel" value="50" required><br>
        <button type="submit">Start Bot</button>
    </form>
    {% if status %}
    <h3>{{ status }}</h3>
    {% endif %}
</body>
</html>
"""

# ======= Flask App =======
app = Flask(__name__)

def run_bot(token, message, delay, max_channels):
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
                if total_sent >= max_channels:
                    print("⚠️ Batas channel tercapai.")
                    await client.close()
                    return
                try:
                    await channel.send(message)
                    print(f"✅ Berhasil kirim ke: #{channel.name} di {guild.name}")
                    total_sent += 1
                    await asyncio.sleep(delay)
                except Exception as e:
                    print(f"❌ Gagal kirim ke {channel.name}: {e}")
        await client.close()

    client.run(token)

@app.route("/", methods=["GET", "POST"])
def index():
    status = None
    if request.method == "POST":
        token = request.form["token"]
        message = request.form["message"]
        delay = int(request.form["delay"])
        max_channels = int(request.form["max_channels"])

        threading.Thread(target=run_bot, args=(token, message, delay, max_channels)).start()
        status = "🚀 Bot sedang berjalan di background!"
    return render_template_string(HTML, status=status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)client.run(TOKEN)
