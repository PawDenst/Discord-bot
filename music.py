import discord
import os
from random import choice
import urllib.parse, urllib.request, re
from discord.ext import commands
import youtube_dl
from discord.utils import get
import threading
import asyncio

client = commands.Bot(command_prefix="!", intents = discord.Intents.all())

global queue
queue=[]
loop = False




class music(commands.Cog):
  def __init__(self,client):
    self.client = client



  
  global is_connected
  def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()
    

  global pobieranie0
  def pobieranie0 (url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(pobieranie(url))
    loop.close()

  global check_queue
  def check_queue(vc):
    print('witam')
    if len(queue)>0:
      pobieranie0(queue[0])
      vc.play(source, after=lambda x=0: check_queue(vc))
      print("gram")
      if not loop:
        del queue[0]
      
  global pobieranie
  async def pobieranie(url):
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 1000000000000M', 'options': '-vn -probesize 1000000000000M'}
    YDL_OPTIONS = {'default_search': 'auto','format':"bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4+best[height<=480]"}
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(queue[0], download=False)
      url2 = info['formats'][0]['url']
      global source
      source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)

  @commands.command(help='Bot dołącza do kanału głosowego.')
  async def join(self,ctx):
    voice_channel = ctx.author.voice.channel
    if ctx.author.voice is None:
      await ctx.send("Nie jestes na kanale")
    if ctx.voice_client is None:
      await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
  
  @commands.command(help='Rozłącza bota z kanałem.')
  async def leave(self,ctx):
    await ctx.voice_client.disconnect()

  @commands.command(name='view', help='Wyświetla piosenki w kolejce.')
  async def view(self, ctx):
    await ctx.channel.send(f'Obecna kolejka: `{queue}!`')
 
  @commands.command(name='play', help='Odtwarza muzykę. Po spacji należy podać link do yt z piosenką albo mniej więcej nazwę piosenki.')
  async def play(self,ctx,*,url):
    global info
    global url2
    global vc
    global link
    global htpfinder
    global source
    voice_channel = ctx.author.voice.channel
    if not is_connected(ctx):
      await voice_channel.connect()
    query_string = urllib.parse.urlencode({'search_query': url})
    html_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
    finder = search_results[0]
    htpfinder = 'https://www.youtube.com/watch?v=' + finder
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 1000000000000M', 'options': '-vn -probesize 1000000000000M'}
    YDL_OPTIONS = {'default_search': 'auto','format':"bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4+best[height<=480]"}
    vc = ctx.voice_client
    if not url.startswith('https://www.youtube'):
      url=htpfinder
      await ctx.send("Właśnie odpalam: " + url)
    #await threading.Thread(target = petle0, args=(ctx, url)).start()
    if not ctx.voice_client.is_playing():
      with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        htpfinder = url
        vc.play(source, after=lambda x=0: check_queue(vc))
        #queue.append(url)
    elif ctx.voice_client.is_playing():
      queue.append(url)

      #query_string = urllib.parse.urlencode({'search_query': search})
      #html_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
      #search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
      #await ctx.send('!play' + 'http://www.youtube.com/watch?v=' + search_results[0])
  
  @commands.command(help='Zatrzymuje graną przez bota piosenkę, można ją odpauzować komendą resume.')
  async def pause(self,ctx):
      if queue:
        print("list is not empty")
      else:
        print("list is empty")
      await ctx.voice_client.pause()
      await ctx.send("Paused")

  @commands.command(help='Wznawia zatrzymaną wcześniej piosenkę.')
  async def resume(self,ctx):
    await ctx.voice_client.resume()
    await ctx.send("Resume")

  @commands.command(help='Przerywa obecnie graną piosenkę i odtwarza kolejną z kolejki.')
  async def skip(self,ctx):
    await ctx.voice_client.stop()
    await ctx.send("Stopped")  

  @commands.command(help='Czyści kolejkę z wszystkich piosenek')
  async def clear(self,ctx):
    queue.clear()
    
  @commands.command(help='Pozwala sprawdzić, czy i jaka piosenka jest obecnie odtwarzana.')
  async def playingaudio(self,ctx):
    if ctx.voice_client.is_playing():
      await ctx.reply("Playing: " + str(htpfinder))
    else:
      await ctx.reply("Nothing is playing")

  @commands.command(help='Wyszukuje link do filmu na yt, którego nazwę należy podać po spacji.')
  async def find(self,ctx,*,search):
    global query_string
    global html_content
    global search_results
    query_string = urllib.parse.urlencode({'search_query': search})
    html_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
    await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])

  @commands.command(name = 'loop', help='Zapętla kolejną piosenkę')
  async def loop_(self, ctx):
    global loop
    if loop:
      await ctx.send("Wyłączono zapętlanie")
      loop = False
      if len(queue)>0:
        del queue[0]
    else:
      await ctx.send("Następna piosenka zsotanie zapętlona!")
      loop = True

    
def setup(client):
    client.add_cog(music(client))