import asyncio
import discord
from discord.ext import commands
import re
import random
import os
import time
from random import shuffle
import sys
import mutagen
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import sqlite3

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!', '!music '), descripton='Shiny School Idol Bot!!')
songList=os.listdir("../Mari/music/")
songList.sort()
if not discord.opus.is_loaded():
	# the 'opus' library here is opus.dll on windows
	# or libopus.so on linux in the current directory
	# you should replace this with the location the
	# opus library is located in and with the proper filename.
	# note that on windows this DLL is automatically provided for you
	discord.opus.load_opus('opus')


songs=['```']

for song in songList:
	if len(songs[-1])>1800:
		songs[-1]+='```'
		songs.append('```')
	if '.mp3' in song:
		songs[-1]+=song.replace('.mp3','')
		songs[-1]+='\n'
songs[-1]+='```'


global emoteList
emoteList=[]
conn=sqlite3.connect('emotes.db')
c=conn.cursor()
emotes=c.execute('SELECT name FROM emotes ORDER BY number')
for emote in emotes:
	emoteList.append(emote[0])
conn.close()

@bot.event
@asyncio.coroutine
def on_ready():
	print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))
	await bot.change_presence(activity=discord.Game(type=1,name='Type \"!help\"'))
	global requests
	requests=[]
	#all=bot.get_all_emojis()
	#emojis=""
	#for emoji in all:
	#	print(str(emoji))
	#	emojis=emojis+"\n"
	#	emojis=emojis+str(emoji)
	#fil=open("emotes.txt","w")
	#fil.write(emojis)

@bot.event
async def on_message(message):
	if "its joke" in message.content.lower() or "it\'s joke" in message.content.lower():
		await message.add_reaction(discord.utils.get(message.server.emojis, name="mariJoke"))
	if "thanks maribot" in message.content.lower():
		await message.channel.send("no problem {}".format(message.author.mention))
	if "maribot" in message.content.lower() and ("ily" in message.content.lower() or "i love you" in message.content.lower()):
		if "dimi" in message.author.display_name.lower():
			await message.add_reaction(discord.utils.get(message.server.emojis, name="mariSuteki"))
			await message.channel.send( "ily too dimi")
		else:
			await message.channel.send("Sorry, I only loves dimi")
	if message.channel.id=="396077247481643028":
		if len(message.attachments)>0 or ".png" in message.content or ".jpg" in message.content or "twitter.com/" in message.content.lower():
			Role=discord.utils.get(message.server.roles,name="Meme Queen")
			await message.author.add_roles(Role)
	if "<:" in message.content and message.author.bot is not True:
		await process(message.content)

	await bot.process_commands(message)


async def process(msg):
	global emoteList
	conn=sqlite3.connect('emotes.db')
	c=conn.cursor()
	for emote in emoteList:
		if emote in msg:
			c.execute("SELECT number FROM emotes WHERE name='"+emote+"'")
			num=c.fetchone()[0]
			c.execute("UPDATE emotes SET number="+str(num+1)+" WHERE  name='"+emote+"'")
	conn.commit()
	conn.close()

@bot.event
async def on_reaction_add(reaction, user):
	print("reaction added")
	global emoteList
	#if reaction in
	print (reaction.name)


@bot.event
async def on_member_join(member):
	for channel in member.server.channels:
		if "welcome" in channel.name:
			welcomech=channel
		elif "awashima" in channel.name:
			defch=channel
		elif "let-me-see-your-voice" in channel.name:
			global voiceCH
			voiceCH=channel
	welcome=open("welcome.txt","r")
	welcomeMessage=welcome.read().format(member.mention,discord.utils.get(member.server.emojis, name="itsjoke"),welcomech.mention)
	#message="Welcome to  {4}, a server all about Ohara Mari!! I can put whatever you want in this, like {0} is the owner of the server, and the person joining is named {1}. Read the rules at {2}. there are currently {3} people in the server".format(member.server.owner.name,member.mention,rules.mention,member.server.member_count,member.server.name)
	bot.loop.create_task(delayMessage(defch,welcomeMessage))


async def delayMessage(defch,welcomeMessage):
	global resetSafe
	resetSafe+=1
	await asyncio.sleep(600)
	await defch.send(welcomeMessage)
	resetSafe-=1

@asyncio.coroutine
def reset(ctx):
	#global voiceCH
	#for channel in ctx.server.channels:
	#	if channel.id.equals("395742882537144320"):
	#		voiceCH=channel
	global resetSafe
	channel=open("channel.txt","r")
	ch=bot.get_channel(channel.read().strip())
	i=0
	while i<60:
		if resetSafe==0 and len(ch.voice_members)<2:
			try:
				await ctx.message.server.get_member("136624816613621761").send("resetting")
			except:
				print("")
			sys.exit(0)
		else:
			print (str(len(ch.voice_members))+" left in vc and "+str(resetSafe)+" welcome messages atm")
			await asyncio.sleep(60)
			i+=1
	print( "we done waiting for VC, there are "+str(resetSafe)+" welcome messages atm")
	while True:
		i+=1
		if i%5==0:
			print(str(resetSafe)+" welcomes left")
		if resetSafe==0:
			try:
				await ctx.message.channel.send("Mari will be right back")
				await ctx.message.server.get_member("136624816613621761").send("resetting")
			except:
				print("")
			sys.exit(0)
		else:
			await asyncio.sleep(20)

@bot.command(hidden=True)
async def restart(ctx):
	"""I will restart once I'm done with my work"""
	print ("attempting to restart")
	bot.loop.create_task(reset(ctx))


@bot.command(no_pm=True)
async def restartNow():
	"""Say this if Mari-chan is being naughty and it can't wait"""
	sys.exit(0)

@bot.command()
async def smug(ctx):
	await ctx.send("<:mariJoke:395760980577091585>")

@bot.command()
async def queue(ctx):
	"""see what SHINY songs Mari has in store for you"""
	global requests
	requestList="```"
	if len(requests)==0:
		requestList=requestList+"Queue is empty"
	else:
		for request in requests:
			requestList=requestList+request
			requestList=requestList+"\n"
	requestList=requestList+"```"
	await ctx.send(requestList)

@bot.command(no_pm=True,pass_context=True)
async def request(ctx,*,message):
	"""Request Mari-San to play a song! If you only know some of the name that's fine, Mari-Nee-san will help"""
	global requests
	potential=[]
	#bot.send_typing(ctx.message.channel)
	if message.lower=="gay":
		ctx.send('adding every love live song ever')
		await ctx.message.add_reaction(discord.utils.get(ctx.message.server.emojis, name="mariYay"))
		await ctx.message.add_reaction(discord.utils.get(ctx.message.server.emojis, name="mariSuperSmug"))
		requests.append("Garasu no Hanazono.mp3")
	else:
		for song in songList:
			if fuzz.ratio(message.lower()+'.mp3',song.lower())>95:
				requests.append(song)
				#yield from bot.say("added")
				await ctx.message.add_reaction(discord.utils.get(ctx.message.server.emojis, name="mariYay"))
				return 0
			elif fuzz.partial_ratio(message.lower(),song.lower())>85:
			potential.append(song)
		if len(potential)==0:
			await ctx.send("Song not found, check your spelling or pm junior mints to add the song.")
		elif len(potential)==1:
			#yield from bot.say("added")
			await ctx.message.add_reaction(discord.utils.get(ctx.message.server.emojis, name="mariYay"))
			requests.append(potential[0])
		else:
			response="```These are potential matches, try being more specific version"
			x=0
			for song in potential:
				response+='\n'
				response+=song
			response+='```'
			await ctx.send(response)

@bot.command(no_pm=True,pass_context=True)
async def playlist(ctx,*,message):
	"""add a SHINY playlist to the queue!"""
	global requests
	if message+".txt" in os.listdir("../Mari/playlists"):
		with open("../Mari/playlists/"+message+".txt") as f:
			songs=f.readlines()
		addedSong=random.choice(songs)
		await ctx.send("added "+addedSong.strip()+" to the queue")
		requests.append(addedSong.strip())



@bot.command(pass_context=True)
async def list(ctx):
	"""I can message you all the songs I know!"""
	for songName in songs:
		await ctx.message.author.send(songName)

@bot.command(pass_context=True)
async def listPL(ctx):
	"""I can message you all playlists!"""

	PLs=['```']
	for song in os.listdir("../Mari/playlists"):
		if len(PLs[-1])>1800:
			PLs[-1]+='```'
			PLs.append('```')
		if '.txt' in song:
			PLs[-1]+=song.replace('.mp3','')
			PLs[-1]+='\n'
	PLs[-1]+='```'

	for PL in PLs:
		async ctx.message.author.send(PL)

@bot.command(pass_context=True)
async def PLContent(ctx,*,message):
	"""Lists all songs in playlist (name is case sensitive, .txt is optional)"""
	with open("../Mari/playlists/"+message.replace('.txt','').strip()+".txt") as f:
		songnames=f.readlines()
	plcontent="```"
	for song in songnames:
		plcontent+=song
	plcontent+="```"
	await ctx.message.author.send(plcontent)

@bot.command(hidden=True)
async def ban(ctx,member : discord.User = bot.user):
	global banCoolDown
	if banCoolDown ==0:
		await ctx.send("{0} is now BANNED".format(member.mention))

@bot.command(hidden=True)
async def update():
	"""Sometimes I forget when I learn new songs~"""
	global songList
	global songs
	songList=os.listdir("../Mari/music/")
	songList.sort()
	songs=['```']
	for song in songList:
		if len(songs[-1])>1800:
			songs[-1]+='```'
			songs.append('```')
		if '.mp3' in song:
			songs[-1]+=song.replace('.mp3','')
			songs[-1]+='\n'
	songs[-1]+='```'

async def status():
	global current
	global mode
	data=mutagen.File(mode+current)
	#if "TIT2" in data.keys():
		#title=str(data["TIT2"])
	#elif "TXXX:title_en" in data.keys():
		#title=str(data["TXXX:title_en"])
	#elif "TXXX:title_jp" in data.keys():
		#title=str(data["TXXX:title_jp"])
	#else:
	title=current
	if "TPE1" in data.keys():
                artist=str(data["TPE1"])
	elif "TXXX:artist_en" in data.keys():
		artist=str(data["TXXX:artist_en"])
	elif "TXXX:artist_jp" in data.keys():
		artist=str(data["TXXX:artist_jp"])
	else:
		artist="artist unknown, pm junior mints to add one"
	await bot.change_presence(activity=discord.Streaming(title+" by "+artist,"https://www.twitch.tv/anthem_osu"))

def get_vc(ctx,channel):
	for ch in ctx.guild.voice_channels:
		if ch.id==channel:
			return ch

async def play(ctx):
	global message
	await bot.wait_until_ready()
	global mode
	global voice
	global sleep
	global current
	global requests
	localmode=mode
	sleep = 0
	channel=open("channel.txt","r")
	ch=get_vc(ctx,int(channel.read().strip()))
	#ch=bot.get_channel(int(channel.read().strip()))
	voice = await ch.connect()
	songs=shuff()
	if len(requests)>0:
		current=requests.pop(0)
	else:
		current=songs.pop(0)
	player=voice.play(discord.FFmpegPCMAudio(mode+current,options="-q:a 9"))
	#yield from bot.change_presence(game=discord.Game(type=2,name=current))
	await status()
	player.start()
	while True:
		if message==-1: #stop command
			#yield from player.stop()
			await voice.disconnect()
			#sys.exit(0)
			break
		elif message==5 or mode!=localmode: #skip song
			message=1
			player.stop()
			if len(songs)<1 or mode!=localmode:
				songs=shuff()
				localmode=mode
			if len(requests)>0:
				current=requests.pop(0)
			else:
				current=songs.pop(0)
				if ".mp3" not in current:
					current=songs.pop(0)
			#yield from bot.change_presence(game=discord.Game(type=2,name=current.replace('.mp3','')))
			await status()
			voice.play(discord.FFmpegPCMAudio(mode+current,options="-q:a 9"))
			player.start()
		elif voice.is_playing():
			await asyncio.sleep(4)
		else:
			if len(songs)<1:
				songs=shuff()
			if len(requests)>0:
				current=requests.pop(0)
			else:
				current=songs.pop(0)
				if ".mp3" not in current:
					current=songs.pop(0)
			#yield from bot.change_presence(game=discord.Game(type=2,name=current))
			await status()
			voice.play(discord.FFmpegPCMAudio(mode+current,options="-q:a 9"))
			#player=voice.create_ffmpeg_player(mode+current,options="-q:a 9")
			player.start()



def shuff():
	global mode
	songList=os.listdir(mode)
	shuffle(songList)
	return songList

@bot.command(no_pm=True)
async def skip(self):
	"""If you want me to play another song"""
	global message
	message=5


@bot.command(pass_context=True, no_pm=True)
async def stop(self):
	"""stops music (for now)"""
	global message
	message=-1
	await bot.change_presence(activity=discord.Game('Type \"!music\" to start music'))

@bot.command(pass_context=True, no_pm=True)
async def music(ctx):
	"""Let's start the music!"""
	global mode
	mode="../Mari/music/"
	global message
	if message!=2:
		message=1
		bot.loop.create_task(play(ctx))

#@bot.command(pass_context=True)
#@asyncio.coroutine
#def mari(self):
#	"""(not working yet) If you only want to hear me singing"""
#	#global mode
#	#mode="./music/rin/"

#@bot.command(pass_context=True)
#@asyncio.coroutine
#def all(self):
#	"""If you like all Love Live Music!"""
#	global mode
#	mode="./music/"

@bot.command()
async def playing(ctx):
	"""I tell you the song I am singing"""
	global current
	global mode
	#id3info=ID3(mode+current)
	#print (id3info['TITLE'])
	#audio=MP3(mode+current+".mp3")
	#current+"\n"+audio.info.Title+" by "+audio.info.Artist
	data=mutagen.File(mode+current)
	title="\n[Title]: "
	if "TIT2" in data.keys():
		title+=str(data["TIT2"])
		title+="\n"
	if "TXXX:title_en" in data.keys():
		title+="\tEN: "
		title+=str(data["TXXX:title_en"])
		title+="\n"
	if "TXXX:title_jp" in data.keys():
		title+="\tJP: "
		title+=str(data["TXXX:title_jp"])
		title+="\n"
	artist="[Artist]: "
	if "TPE1" in data.keys():
		artist+=str(data["TPE1"])
		artist+=" \n"
	if "TXXX:artist_en" in data.keys():
		artist+="\tEN: "
		artist+=str(data["TXXX:artist_en"])
		artist+="\n"
	if "TXXX:artist_jp" in data.keys():
		artist+="\tJP: "
		artist+=str(data["TXXX:artist_jp"])
		artist+="\n"
	if not("TPE1" in data.keys() or "TXXX:artist_en" in data.keys() or "TXXX:artist_jp" in data.keys()):
		artist="\nArtist unknown, pm junior mints to add one"
	await ctx.send("```css\n[File]: "+current+title+artist+"```")

global message
global resetSafe
global banCoolDown
banCoolDown=0
resetSafe=0
message=0
file_object=open("rin.txt","r")
bot.run(file_object.read().strip())
