import discord
from discord.ext import commands
from youtube_search import YoutubeSearch
import random
import urllib.parse, urllib.request, re
import youtube_dl
import os

from discord.utils import get

client = commands.Bot(command_prefix="*")


def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()


@client.event
async def on_ready():
    print("bot is ready")


@client.command()
async def showCommands(ctx):
    str = "\n*ping \n*play youtubeURL \n*join \n*leave \n*kissMe"
    await ctx.send(str)


@client.command()
async def ping(ctx):
    await ctx.send(f'Ping is: {round(client.latency*1000)}ms')


@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()


@client.command()
async def leave(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()


@client.command()
async def play(ctx, *, url):
    if not is_connected(ctx):
        channel = ctx.message.author.voice.channel
        await channel.connect()

    if "watch?v" not in url and "https://youtu.be" not in url:
        song_string = urllib.parse.urlencode({'search_query': url})
        htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + song_string)
        print(htm_content.read().decode())
        ex = 'videoId\":\"'
        search_results = re.findall(ex + '(.{11})', htm_content.read().decode())
        #search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
        print(search_results[0] + "/////third")
        url = 'http://www.youtube.com/watch?v=' + search_results[0]

    song_there = os.path.isfile("song1.mp3")
    try:
        if song_there:
            os.remove("song1.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting everything ready now")

    voice = ctx.guild.voice_client

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song1.mp3")

    voice.play(discord.FFmpegPCMAudio("song1.mp3"), after=lambda e: print("Song done!"))

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")

@client.command()
async def kissMe(ctx, *, type = "once"):
    if not is_connected(ctx):
        channel = ctx.message.author.voice.channel
        await channel.connect()

    voice = ctx.guild.voice_client

    if "once" in type:
        voice.play(discord.FFmpegPCMAudio("oneKiss.wav"), after=lambda e: print("Song done!"))
    else:
        voice.play(discord.FFmpegPCMAudio("kissing.wav"), after=lambda e: print("Song done!"))
    print("Currently kissing")

    results = YoutubeSearch("test", max_results=5).to_json()
    print(results)
    results = YoutubeSearch("test", max_results=5).to_dict()
    print(results)


client.run("TOKEN")

