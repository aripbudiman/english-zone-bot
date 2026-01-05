import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from langdetect import detect, LangDetectException

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
ENGLISH_CHANNEL_ID = 1457298769313009694
MIN_LENGTH = 2  # Minimal 20 karakter baru dicek

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == ENGLISH_CHANNEL_ID:
        try:
            # Skip jika pesan terlalu pendek atau hanya emoji/angka
            if len(message.content.strip()) < MIN_LENGTH:
                print(f"⏭️ Message too short, skipping: {message.content}")
                await bot.process_commands(message)
                return
            
            detected_lang = detect(message.content)
            print(f"Detected: {detected_lang} | Message: {message.content}")
            
            if detected_lang != "en":
                await message.delete()
                await message.channel.send(
                    f"⚠️ {message.author.mention} English only please 🇬🇧",
                    delete_after=5
                )
                return
                
        except LangDetectException as e:
            print(f"⚠️ Can't detect language: {e}")
            pass
        except discord.Forbidden:
            print("❌ No permission to delete messages!")
        except Exception as e:
            print(f"❌ Error: {e}")

    await bot.process_commands(message)

bot.run(TOKEN)