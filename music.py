import discord
import os
import urllib.parse, urllib.request, re
from discord.ext import commands
import youtube_dl
from discord.utils import get


class music(commands.Cog):
  def __init__(self,client):
    self.client = client

  def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()
  # def is_connected(ctx):
  #   voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
  #   return voice_client and voice_client.is_connected()
  
  @commands.command()
  async def join(self,ctx):
    voice_channel = ctx.author.voice.channel
    if ctx.author.voice is None:
      await ctx.send("Nie jestes")
    if ctx.voice_client is None:
      await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)

  @commands.command()
  async def play(self,ctx,url):
    global info
    def is_connected(ctx):
      voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
      return voice_client and voice_client.is_connected()
    voice_channel = ctx.author.voice.channel
    if is_connected(ctx):
      #query_string = urllib.parse.urlencode({'search_query': search})
      #html_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
      #search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
      #await ctx.send('!play' + 'http://www.youtube.com/watch?v=' + search_results[0])
      FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 1000000000000M', 'options': '-vn -probesize 1000000000000M'}
      YDL_OPTIONS = {'default_search': 'auto','format':"bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4+best[height<=480]"}
      global vc
      vc = ctx.voice_client
      with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        global link
        global mus
        link = url
        mus=source
        vc.play(mus)
        
    else:
      await voice_channel.connect()
      #ctx.voice_client.stop()
      FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5  -probesize 1000000000000M', 'options': '-vn -probesize 1000000000000M'}
      YDL_OPTIONS = {'format':"bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4+best[height<=480]"}
      vc = ctx.voice_client
      with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        link = url
        mus=source
        vc.play(mus)

  @commands.command()
  async def loop(self, ctx):
    if not ctx.voice_client.is_playing():
      await ctx.reply("Nie ma czego zloopować")
    ctx.voice_client.loop = not ctx.voice_client.loop
    await ctx.message.add_reaction("👍")
  
  @commands.command()
  async def loop(self, ctx):
    global loop
    if loop:
        await ctx.send('Loop mode is now `False!`')
        loop = False
    else: 
        await ctx.send('Loop mode is now `True!`')
        loop = True
    
  @commands.command()
  async def pause(self,ctx):
      await ctx.voice_client.pause()
      await ctx.send("Paused")

  @commands.command()
  async def resume(self,ctx):
      await ctx.voice_client.resume()
      await ctx.send("Resume")

  @commands.command()
  async def leave(self,ctx):
    await ctx.voice_client.disconnect()
    
  @commands.command()
  async def playingaudio(self,ctx):
    if ctx.voice_client.is_playing():
      await ctx.reply("Playing: " + str(link))
    else:
      await ctx.reply("Nothing is playing")

  @commands.command()
  async def find(self,ctx,*,search):
    global query_string
    global html_content
    global search_results
    query_string = urllib.parse.urlencode({'search_query': search})
    html_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
    await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])
    
  @commands.command()
  async def loop(self,ctx):
    ctx.voice_client = music.get_player(guild_id=ctx.guild.id)
    song = await ctx.voice_client.toggle_song_loop()
    if song.is_looping:
      await ctx.reply("loopujemy")
    else:
      await ctx.reply("nic nie loopuje")

  @commands.command()
  async def search(self,ctx,*,search):
    query_string = urllib.parse.urlencode({'search_query': search})
    html_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
    finder = search_results[0]
    htpfinder = 'http://www.youtube.com/watch?v=' + finder
    #await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])
    def is_connected(ctx):
      voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
      return voice_client and voice_client.is_connected()
    voice_channel = ctx.author.voice.channel
    if is_connected(ctx):
      FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 1000000000000M', 'options': '-vn -probesize 1000000000000M'}
      YDL_OPTIONS = {'default_search': 'auto','format':"bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4+best[height<=480]"}
      vc = ctx.voice_client
      with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(htpfinder, download=False)
        print(htpfinder)
        url2 = info['formats'][0]['url']
        #print(finder)
        #print('siema' + url2)
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        vc.play(source)
        
    else:
      await voice_channel.connect()
      #ctx.voice_client.stop()
      FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5  -probesize 1000000000000M', 'options': '-vn -probesize 1000000000000M'}
      YDL_OPTIONS = {'format':"bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4+best[height<=480]"}
      vc = ctx.voice_client
      with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info2 = ydl.extract_info(htpfinder, download=False)
        url2 = info2['formats'][0]['url']
        print(htpfinder)
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        vc.play(source)
    
def setup(client):
    client.add_cog(music(client))