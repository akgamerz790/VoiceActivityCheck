import os as _System
import dotenv as _ENV
from dotenv import load_dotenv as _Load_ENV
from src.Bot_Setup.Check_Token import _Check_Token
import src.Color_Library.Colors as _Color
import discord as _Discord
from discord.ext import commands as _BotCommandAPI

# Load environment
_Load_ENV()
_TOKEN = _System.getenv("BOT_TOKEN")
if _Check_Token():
    print(_Color._RED + "[!] " + "Bot Token was not Set!" + _Color._RESET)
    _System._exit(5)
else:
    print(_Color._GREEN + "[!] " + "Token Successfully Retrieved..." + _Color._RESET)

# Bot intents
_BOT_INTENT = _Discord.Intents.default()
_BOT_INTENT.message_content = True
_BOT_INTENT.voice_states = True
_BOT = _BotCommandAPI.Bot(command_prefix="!", intents=_BOT_INTENT)

# Path to MP3 and FFmpeg
MP3_PATH = "src/Music/endfield.mp3"
FFMPEG_PATH = "src/AudioAPI/ffmpeg.exe"

@_BOT.event
async def on_message(message):
    if message.author.bot:
        return

    # JOIN VC
    if "join vc" in message.content.lower():
        if message.author.voice:
            channel = message.author.voice.channel

            if message.guild.voice_client is None:
                voice_client = await channel.connect()
                await message.channel.send("Joined your VC!")
            else:
                voice_client = message.guild.voice_client
                await message.channel.send("Already in a VC!")

            # Play MP3 if not playing
            if not voice_client.is_playing():
                audio_source = _Discord.FFmpegPCMAudio(
                    MP3_PATH,
                    executable=FFMPEG_PATH
                )
                voice_client.play(audio_source)
                await message.channel.send(f"Now playing {MP3_PATH}!")
            else:
                await message.channel.send("Audio is already playing!")
        else:
            await message.channel.send("You are not in a voice channel.")

    # LEAVE VC
    if "leave vc" in message.content.lower():
        voice_client = message.guild.voice_client
        if voice_client is not None:
            await voice_client.disconnect()
            await message.channel.send("Sorry youre not a sigma")
        else:
            await message.channel.send("I'm not in a voice channel.")

    await _BOT.process_commands(message)

# Optional: Someone speaking event
@_BOT.event
async def on_voice_state_update(member, before, after):
    if after.self_mute is False or after.self_deaf is False:
        print(f"{member} is speaking or unmuted.")

# Run bot
_BOT.run(_TOKEN)