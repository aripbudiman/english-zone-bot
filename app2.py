import os
import discord
from discord.ext import commands
from discord.ui import View, Button
from dotenv import load_dotenv
from langdetect import detect, LangDetectException
from googletrans import Translator

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
ENGLISH_CHANNEL_ID = 1457298769313009694
MIN_LENGTH = 1

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
translator = Translator()

class TranslationView(View):
    def __init__(self, original_message, detected_lang, author):
        super().__init__(timeout=60)  # Button aktif 60 detik
        self.original_message = original_message
        self.detected_lang = detected_lang
        self.author = author
        self.translated = False
    
    @discord.ui.button(label="🌐 Translate to English", style=discord.ButtonStyle.primary)
    async def translate_button(self, interaction: discord.Interaction, button: Button):
        # Cek apakah yang klik adalah author pesan
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(
                "❌ Only the message author can use this button!",
                ephemeral=True
            )
            return
        
        try:
            # Translate ke bahasa Inggris
            translation = translator.translate(self.original_message, dest='en')
            
            # Kirim pesan terjemahan
            embed = discord.Embed(
                title="✅ Translated Message",
                description=translation.text,
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Original ({self.detected_lang}): {self.original_message[:100]}...")
            
            await interaction.response.send_message(embed=embed)
            
            # Disable button setelah dipakai
            button.disabled = True
            button.label = "✓ Translated"
            await interaction.message.edit(view=self)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Translation failed: {str(e)}",
                ephemeral=True
            )
    
    @discord.ui.button(label="❌ Delete Message", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button: Button):
        # Cek apakah yang klik adalah author pesan atau moderator
        if interaction.user.id != self.author.id and not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "❌ Only the message author or moderators can delete!",
                ephemeral=True
            )
            return
        
        try:
            # Hapus pesan warning
            await interaction.message.delete()
            await interaction.response.send_message(
                "✅ Message deleted successfully",
                ephemeral=True,
                delete_after=3
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Failed to delete: {str(e)}",
                ephemeral=True
            )
    
    @discord.ui.button(label="✓ Keep Original", style=discord.ButtonStyle.secondary)
    async def keep_button(self, interaction: discord.Interaction, button: Button):
        # Cek apakah yang klik adalah author pesan
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(
                "❌ Only the message author can use this button!",
                ephemeral=True
            )
            return
        
        await interaction.response.send_message(
            "✅ Message kept as is",
            ephemeral=True,
            delete_after=3
        )
        
        # Hapus warning message
        await interaction.message.delete()

@bot.event
async def on_ready():
    print(f'✅ Bot logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == ENGLISH_CHANNEL_ID:
        try:
            content = message.content.strip()
            
            # Skip pesan pendek
            if len(content) < MIN_LENGTH:
                print(f"⏭️ Too short: {content}")
                await bot.process_commands(message)
                return
            
            # Deteksi bahasa
            detected_lang = detect(content)
            print(f"🔍 Detected: {detected_lang} | Message: {message.content}")
            
            if detected_lang != "en":
                # Buat embed warning dengan button
                embed = discord.Embed(
                    title="⚠️ Non-English Message Detected",
                    description=f"{message.author.mention}, this is an English-only channel.\n\n"
                                f"**Detected Language:** `{detected_lang}`\n"
                                f"**Your message:** {content[:200]}{'...' if len(content) > 200 else ''}",
                    color=discord.Color.orange()
                )
                embed.set_footer(text="Choose an action below:")
                
                # Kirim warning dengan buttons
                view = TranslationView(content, detected_lang, message.author)
                warning_msg = await message.channel.send(embed=embed, view=view)
                
                # Tidak langsung delete, biarkan user pilih
                # Atau bisa delete setelah timeout
                
        except LangDetectException:
            print(f"⚠️ Can't detect language: {message.content}")
            pass
        except Exception as e:
            print(f"❌ Error: {e}")

    await bot.process_commands(message)

bot.run(TOKEN)