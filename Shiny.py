import asyncio
import discord
from discord.ext import commands
import re
import random
import os
import time
import datetime
from random import shuffle
import sys
import mutagen
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from paste_bin import PasteBinApi
import sqlite3
import json
import pandas as pd


print("ARE YOU RUNNING YOUR VENV, I BET YOU FORGOT YOU DUMBDUMB")
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
global G_orig,G_repeat,G_max,G_time
G_orig=1
G_repeat=2
G_max=5
G_time=10
songs=['```']
global data
global my_key
global antiSpam,antiSpamCount,enable
enable=True
antiSpamCount={}
antiSpam={}

data=json.load(open('pastebin.json'))
api=PasteBinApi(dev_key=data['key'])
user_key=api.user_key(username=data['username'],password=data['password'])
#my_key = PastebinAPI.generate_user_key(self,data['key'], data['username'], data['password'])
G_suteki="<:mariSuteki:395764874283581442>"
G_smug="<:mariSuperSmug:411516943099494400>"
G_gasm="<:mariGasm:396648817988075521>"

for song in songList:
	if len(songs[-1])>1800:
		songs[-1]+='```'
		songs.append('```')
	if '.mp3' in song:
		songs[-1]+=song.replace('.mp3','')
		songs[-1]+='\n'
songs[-1]+='```'

def isDimi(ctx):
	return ctx.author.id==111459540679024640

async def botOwner(ctx):
	return ctx.author.id==136624816613621761

async def isMod(ctx):
	if ctx.author in discord.utils.find(lambda m: m.name=="Pretty Modder Head",ctx.guild.roles).members:
		return True
	return False

#global G_orig,G_repeat,G_max,G_time
#conn=sqlite3.connect('emotes.db')
#c=conn.cursor()
#emotes=c.execute('SELECT name FROM emotes ORDER BY number')
#for emote in emotes:
#	emoteList.append(emote[0])



@bot.event
async def on_ready():
	print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))
	await bot.change_presence(activity=discord.Game('Type \"!help\"'))
	global requests
	requests=[]
	global emoteList
	maricord=bot.get_guild(175176337185701888)
	emoteList=maricord.emojis
	global filingCH
	for channel in maricord.channels:
		if "filing" in channel.name:
			filingCH=channel
	bot.loop.create_task(noSpam())
	#all=bot.get_all_emojis()
	#emojis=""
	#for emoji in all:
	#	print(str(emoji))
	#	emojis=emojis+"\n"
	#	emojis=emojis+str(emoji)
	#fil=open("emotes.txt","w")
	#fil.write(emojis)

async def noSpam():
	global G_orig,G_repeat,G_max,G_time,antiSpamCount,antiSpam,disable
	while (True):
		try:
			for spammer in antiSpamCount.keys():
				if antiSpamCount[spammer]>=1:
					#antiSpamCount[spammer]
					#del antiSpam[spamm
					if len(antiSpam[spammer])==antiSpamCount[spammer]:
						antiSpam[spammer].pop(0)
					antiSpamCount[spammer]-=1
		except Exception as e:
			print (e)
			#print("clearing queue")
			#antiSpamCount={}
			#antiSpam={}
		await asyncio.sleep(1)

async def Mute(spammer,guild):
	global filingCH
	global resetSafe
	resetSafe+=1
	if discord.utils.get(guild.roles,name="Muted") in spammer.roles:
		return (1)
	await spammer.send("looks like you are not being SHINY right now, you have been temporarily muted, and the mods have been notified. You will automatically be unmuted Please do not ask to be unmuted, and avoid spamming in the future")
	Roles=spammer.roles
	Roles.pop(0)
	#await spammer.remove_roles(roles)
	await spammer.edit(roles=[])
	roleList=""
	for role in Roles:
		roleList=roleList+role.name+", "
	await filingCH.send("{0} has been muted, and will automatically be unmuted in 10 minutes. They had the following roles{1}".format(spammer.name,roleList))
	await spammer.add_roles(discord.utils.get(guild.roles,name="Muted"))
	await asyncio.sleep(600)
	await spammer.edit(roles=Roles)
	await spammer.remove_roles(discord.utils.get(guild.roles,name="Muted"))
	resetSafe-=1
	await filingCH.send("{0} has been unmuted. They have been given their roles back".format(spammer.name))

@bot.event
async def on_message(message):
	try:
		if "Joke" in message.guild.name:
			return (1)
	except:
		print ("")
	#print (message.content)
	global G_orig,G_repeat,G_max,G_time,antiSpamCount,antiSpam,enable
	if message.author.id in antiSpam.keys() and message.channel.id!=410486994699812864:
		if message.author.id==270266799885516801 and message.channel.id==175176485022334976:
			antiSpamCount[message.author.id]+=0
		if message.content in antiSpam[message.author.id]:
			antiSpamCount[message.author.id]+=G_repeat
		else:
			antiSpamCount[message.author.id]+=G_orig
		antiSpam[message.author.id].append(message.content)
	elif message.channel.id!=410486994699812864:
		antiSpam[message.author.id]=[message.content]
		antiSpamCount[message.author.id]=1
	if antiSpamCount[message.author.id]>G_max and enable:
		await Mute(message.author,message.guild)
		return (1)
	if message.channel.id==395743189283241995:
		return (1)
	if ("joke" in message.content.lower() or "it\'s joke" in message.content.lower()) and message.channel.id!=395743189283241995:
		await message.add_reaction(discord.utils.get(message.guild.emojis, name="mariJoke"))
	if "thanks maribot" in message.content.lower():
		await message.channel.send("no problem {}".format(message.author.mention))
	if "nep" == message.content.lower():
		await message.channel.send("nep nep")
	if "nep nep nep" == message.content.lower():
		await message.channel.send("https://www.youtube.com/watch?v=EKxio8HZiNA")
	if message.author.id==111459540679024640 and ("maribot" in message.content.lower() or message.content.startswith("!")):
		await handleDimi(message)
	elif "maribot" in message.content.lower() and ("ily" in message.content.lower() or "i love you" in message.content.lower()):
		if 136624816613621761 == message.author.id:
			await message.channel.send( "ily too dad")
		else:
			await message.channel.send("Sorry, Dimi is my one true love, but I think you're great!")
	if message.channel.id==396077247481643028:
		if len(message.attachments)>0 or ".png" in message.content or ".jpg" in message.content or "twitter.com/" in message.content.lower():
			Role=discord.utils.get(message.guild.roles,name="Ainya's Worshipers")
			await message.author.add_roles(Role)
	if "!ban holo"==message.content.lower():
		await message.channel.send("no")
	#if message.channel.id==439643359745671180:
		#if len(message.attachments)>0 or ".png" in message.content or ".jpg" in message.content or "twitter.com/" in message.content.lower():
		#gRole=discord.utils.get(message.guild.roles,name="Giveaway")
		#await message.author.add_roles(gRole)
	if "<:" in message.content and message.author.bot is not True:
		await process(message)
	await bot.process_commands(message)



#async def send_pastebin(message.
async def handleDimi(message):
	if "ily" in message.content.lower() or "i love you" in message.content.lower():
		async with message.channel.typing():
			await asyncio.sleep(random.randint(2,3))
			await message.add_reaction(discord.utils.get(message.guild.emojis, name="mariSuteki"))
			await asyncio.sleep(random.randint(3,5))
			await message.channel.send("I don't blame you "+G_smug)
	elif "let me " in message.content.lower() or "can i " in message.content.lower():
		async with message.channel.typing():
			await asyncio.sleep(random.randint(5,8))
			await message.channel.send("Shouldn't this be in DMs Dimi? "+G_suteki)
	elif "send " in message.content.lower():
		if "thigh" in message.content.lower():
			await message.channel.send("i'll send them in DMs "+G_suteki)
			async with message.author.typing():
				await message.author.send("one seccond")
				await asyncio.sleep(random.randint(6,15))
				await message.author.send("ok, here they are https://imgur.com/a/5hk7tOU")
				await asyncio.sleep(random.randint(1,5))
				await message.author.send("sorry if they're not thicc enough for you 😳")
		if "nudes" in message.content.lower() or "noods" in message.content.lower():
			async with message.channel.typing():
				await asyncio.sleep(random.randint(4,6))
				await message.channel.send("you first "+G_gasm)
	elif "step on" in message.content.lower():
		async with message.channel.typing():
			await asyncio.sleep(random.randint(3,7))
			await message.channel.send("I didn't know pets could talk "+G_suteki)
	elif "execute order 66" in message.content.lower():
		async with message.channel.typing():
			await asyncio.sleep(random.randint(2,4))
			await message.channel.send("working on it")
			await asyncio.sleep(random.randint(60*3,60*5))
			await message.channel.send("preparations complete")
			await asyncio.sleep(random.randint(5,7))
			await message.channel.send(G_smug)
			spamch=discord.utils.get(message.guild.text_channels,name="lets-emoji-spam")
		async with spamch.typing():
			await message.channel.send("{0}".format(spamch.mention))
			await asyncio.sleep(2)
			await spamch.send("<:McMari:398559387377205248> {0}".format(message.author.mention))
			await asyncio.sleep(4)
			await spamch.send("<:McMari:398559387377205248> <a:zuradance:440368129105985547>")
			await asyncio.sleep(4)
			await spamch.send("<:McMari:398559387377205248> <a:youdance:440537076317028352>")
			await asyncio.sleep(4)
			await spamch.send("<:McMari:398559387377205248> <a:mariDance:397596749101006868>")
			await asyncio.sleep(4)
			await spamch.send("<:McMari:398559387377205248> <a:yohadance:439193900461326347>")
			await asyncio.sleep(4)
			await spamch.send("<:McMari:398559387377205248> <a:rikodance:440537108159922186>")
			await asyncio.sleep(4)
			await spamch.send("<:McMari:398559387377205248> <a:kanandance:439925504137494539>")
	elif "night marib" in message.content.lower():
		async with message.channel.typing():
			await asyncio.sleep(5)
			await message.channel.send("sleep tite dimi")





async def process(msg):
	global emoteList
	emoteList=msg.guild.emojis
	try:
		conn=sqlite3.connect('emotes.db')
		c=conn.cursor()
		for emote in emoteList:
			if emote.name in msg.content:
				c.execute("SELECT number FROM emotes WHERE name=?",(emote.name,))
				num=c.fetchone()[0]
				c.execute("UPDATE emotes SET number="+str(num+1)+" WHERE  name=?",(emote.name,))
		conn.commit()
	except Exception as e:
		print (e)
	conn.close()

@bot.event
async def on_guild_emojis_update(guild,before,after):
	if "Shiny" in guild.name:
		for emote in after:
			if emote not in before:
				conn=sqlite3.connect('emotes.db')
				c=conn.cursor()
				c.execute ("INSERT INTO emotes (name, number) VALUES (?,?)",(emote.name,1))
				conn.commit()
				conn.close()

@bot.event
async def on_reaction_add(reaction, user):
	if "Shiny" in reaction.message.guild.name:
		#print("reaction added")
		global emoteList
		try:
			if reaction.emoji in emoteList:
				#print (str(type(reaction.emoji)))
				#print (str(type(reaction.emoji.name)))
				conn=sqlite3.connect('emotes.db')
				c=conn.cursor()
				#print ("check 1")
				c.execute("SELECT number FROM emotes WHERE name=?",(reaction.emoji.name,))
				num=c.fetchone()[0]
				#print("check 2")
				c.execute("UPDATE emotes SET number="+str(num+1)+" WHERE name=?",(reaction.emoji.name,))
				#print("check 3")
				conn.commit()
				#print ("check 4")
				conn.close()
		except Exception as e:
			print("error on checking reaction "+str(e))

@bot.event
async def on_member_join(member):
	if "Shiny" in member.guild.name:
		for channel in member.guild.channels:
			if "welcome" in channel.name:
				welcomech=channel
			elif "awashima" in channel.name:
				defch=channel
			elif "let-me-see-your-voice" in channel.name:
				global voiceCH
				voiceCH=channel
			elif "filing" in channel.name:
				global logCH
				logCH=channel
		welcome=open("welcome.txt","r")
		welcomeMessage=welcome.read().format(member.mention,discord.utils.get(member.guild.emojis, name="itsjoke"),welcomech.mention)
		#print (str(type (defch)))
		#print (welcomeMessage)
		#message="Welcome to  {4}, a server all about Ohara Mari!! I can put whatever you want in this, like {0} is the owner of the server, and the person joining is named {1}. Read the rules at {2}. there are currently {3} people in the server".format(member.server.owner.name,member.mention,rules.mention,member.server.member_count,member.server.name)
		#bot.loop.create_task(delayMessage(defch,welcomeMessage))
		bot.loop.create_task(delayMessage(defch,welcomeMessage))


async def delayMessage(defch,welcomeMessage):
	global resetSafe
	resetSafe+=1
	#print( "member join")
	await asyncio.sleep(600)
	await defch.send(welcomeMessage)
	resetSafe-=1


async def reset(ctx):
	#global voiceCH
	#for channel in ctx.server.channels:
	#	if channel.id.equals("395742882537144320"):
	#		voiceCH=channel
	try:
		global resetSafe
		channel=open("channel.txt","r")
		ch=discord.utils.find(lambda m:m.id==402987335391772676,ctx.guild.voice_channels)
		i=0
		while i<60:
			if resetSafe==0 and len(ch.members)<2:
				try:
					owner=bot.get_user(136624816613621761)
					await owner.send('resetting')
				except Exception as e:
					print("tried to send message to you, failed with: "+e)
				sys.exit()
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
					await ctx.message.guild.get_member("136624816613621761").send("resetting")
				except:
					print("")
				sys.exit()
			else:
				await asyncio.sleep(20)
	except:
		sys.exit(0)

@bot.command(hidden=True)
@commands.check(isMod)
async def mute(ctx,member : discord.User = bot.user):
	await Mute(ctx.guild.get_member(member.id),ctx.guild)

@bot.command(hidden=True)
@commands.check(isMod)
async def listRole(ctx):
	roleName=ctx.message.content.replace("!listRole ","")
	role=discord.utils.find(lambda m:m.name.lower()==roleName.lower(),ctx.guild.roles)
	await ctx.send(str(random.choice(role.members)))

@bot.command(hidden=True)
@commands.check(isMod)
async def exportEmotes(ctx):
	global data
	global my_key
	conn=sqlite3.connect('emotes.db')
	c=conn.cursor()
	c.execute("SELECT * FROM emotes ORDER BY number DESC")
	results=c.fetchall()
	#results=pd.read_sql_query("SELECT * FROM emotes ORDER BY number DESC",conn)
	result=(pd.DataFrame(results).to_string())
	#api = PastebinAPI()
	#print(api.paste(api_dev_key=data['key'],api_paste_code=result,paste_name="emote usage"))
	link=api.paste(user_key,title='emote usage',raw_code=result,private=None,expire_date=None)
	await ctx.send(link)

@bot.command(hidden=True)
@commands.check(isMod)
async def say(ctx,*,msg):
	if ctx.author.id==111459540679024640:
		await ctx.send("you want me to say what???")
		return 0
	content=ctx.message.content.replace("!say ","")
	await ctx.message.delete()
	await ctx.send(content)

@bot.command(hidden=True)
@commands.check(isMod)
async def disableSpam(ctx):
	global enable
	enable=False

@bot.command(hidden=True)
@commands.check(isMod)
async def enableSpam(ctx):
	global enable
	enable=True

@bot.command()
async def love(ctx,*,msg):
	MSG=msg.strip().lower()
	f=open("love.json","r")
	loveNovel=json.loads(f.read())
	f.close()
	if MSG=="maribot":
		await ctx.send(ctx.message.guild.get_member(111459540679024640).avatar_url_as(format=None, static_format="png"))
	elif MSG in loveNovel.keys():
		await ctx.send(loveNovel[MSG])

@bot.command()
@commands.check(isMod)
async def loveadd(ctx,person,content):
	f=open("love.json","r")
	loveNovel=json.loads(f.read())
	f.close()
	if person.lower() in loveNovel.keys():
		await ctx.send("I already know how {0} is loved".format(person))
	else:
		loveNovel[person.lower()]=content
		f=open("love.json","w")
		f.write(json.dumps(loveNovel))
		f.close()

@bot.command()
@commands.check(isMod)
async def loveremove(ctx,person):
	f=open("love.json","r")
	loveNovel=json.loads(f.read())
	f.close()
	f=open("love.json","w")
	del loveNovel[person]
	f.write(json.dumps(loveNovel))
	f.close()

@bot.command(hidden=True)
@commands.check(botOwner)
async def restart(ctx):
	"""I will restart once I'm done with my work"""
	print ("attempting to restart")
	bot.loop.create_task(reset(ctx))


@bot.command(no_pm=True)
async def restartNow(ctx):
	"""Restarts Mari, only use this if she isn't working right"""
	sys.exit(0)

@bot.command(no_pm=True)
async def iam(ctx,*,role):
	"""Self assign roles (eg. !iam pure, !iam squad)"""
	if "pure" in role.lower():
		Role=discord.utils.get(ctx.message.guild.roles,name="Pure White")
		await ctx.message.author.add_roles(Role)
	elif "squad" in role.lower():
		Role=discord.utils.get(ctx.message.guild.roles,name="Stewshine Squad")
		await ctx.message.author.add_roles(Role)
	elif "mod" in role.lower():
		await ctx.send("<:mariJoke:395760980577091585>")

@bot.command(no_pm=True)
async def iamn(ctx,*,role):
	if "pure" in role.lower():
		Role=discord.utils.get(ctx.message.guild.roles,name="Pure White")
		await ctx.message.author.remove_roles(Role)
	elif "squad" in role.lower():
		Role=discord.utils.get(ctx.message.guild.roles,name="Stewshine Squad")
		await ctx.message.author.remove_roles(Role)


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
	if message.lower()=="gay":
		#ctx.send('adding every love live song ever')
		await ctx.message.add_reaction(discord.utils.get(ctx.message.guild.emojis, name="mariYay"))
		#await ctx.message.add_reaction(discord.utils.get(ctx.message.guild.emojis, name="mariSuperSmug"))
		for song in songList:
			if fuzz.ratio('Garasu no Hanazono'.lower()+'.mp3',song.lower())>95:
				requests.append(song)
				return 0
	elif "lesbian" in message.lower():
		await ctx.message.add_reaction(discord.utils.get(ctx.message.guild.emojis, name="mariYay"))
		for song in songList:
			if fuzz.ratio('Zurui yo Magnetic today.mp3'.lower(),song.lower())>95:
				requests.append(song)
				return 0
	elif "thighs" in message.lower():
		if isDimi(ctx):
			await ctx.send("i'll send them in DMs "+G_suteki)
			async with ctx.author.typing():
				await ctx.author.send("smh, don't you have them saved?")
				await asyncio.sleep(random.randint(3,15))
				await ctx.author.send("ok, here they are! https://imgur.com/a/5hk7tOU")
				await asyncio.sleep(random.randint(3,15))
				await ctx.author.send("sorry if they're not thicc enough for you 😳")
		else:
			await ctx.send("my thighs are only for dimi")
	else:
		for song in songList:
			if fuzz.ratio(message.lower()+'.mp3',song.lower())>95:
				requests.append(song)
				#yield from bot.say("added")
				await ctx.message.add_reaction(discord.utils.get(ctx.message.guild.emojis, name="mariYay"))
				return 0
			elif fuzz.partial_ratio(message.lower(),song.lower())>85:
				potential.append(song)
		if len(potential)==0:
			await ctx.send("Song not found, check your spelling or pm junior mints to add the song.")
		elif len(potential)==1:
			#yield from bot.say("added")
			await ctx.message.add_reaction(discord.utils.get(ctx.message.guild.emojis, name="mariYay"))
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
	if message+".txt" in os.listdir("../Mari/playlist"):
		with open("../Mari/playlist/"+message+".txt") as f:
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
		await ctx.message.author.send(PL)

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
	if member.id==111459540679024640:
		await ctx.send("I could never ban Dimi <:mariSuteki:395764874283581442>")
	else:
		if member.id==136624816613621761:
			await ctx.send("Sorry dad <:mariCry:397609045403369473>")
			await ctx.send("{0} is now BANNED".format(member.mention))
		elif "maribot" in member.name.lower():
			await ctx.send("{0} is now BANNED".format(ctx.message.author.mention))
		else:
			await ctx.send("{0} is now BANNED".format(member.mention))

@bot.command(hidden=True)
async def update(ctx):
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

@bot.command(hidden=True)
@commands.check(botOwner)
async def updateEmojis(ctx):
	conn=sqlite3.connect('emotes.db')
	c=conn.cursor()
	c.execute("DROP TABLE emotes")
	c.execute("""CREATE TABLE emotes(
			name text,
			number integer
			)""")
	conn.commit()
	emoteList=ctx.guild.emojis
	for emote in emoteList:
		c.execute("INSERT INTO emotes (name, number) VALUES (?,0)",(emote.name,))
		conn.commit()
	conn.close()

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
	await bot.change_presence(activity=discord.Streaming(name=title+" by "+artist,url="https://www.twitch.tv/anthemOSU"))

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
	player=voice.play(discord.FFmpegPCMAudio(mode+current,options="-q:a 8"))
	#yield from bot.change_presence(game=discord.Game(type=2,name=current))
	await status()
	#player.start()
	while True:
		if message==-1: #stop command
			#yield from player.stop()
			await voice.disconnect()
			#sys.exit(0)
			break
		elif message==5 or mode!=localmode: #skip song
			message=1
			voice.stop()
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
			voice.play(discord.FFmpegPCMAudio(mode+current,options="-q:a 8"))
			#voice.start()
		elif voice.is_playing():
			#print("is playing")
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
			voice.play(discord.FFmpegPCMAudio(mode+current,options="-q:a 8"))
			#player=voice.create_ffmpeg_player(mode+current,options="-q:a 9")
			#player.start()



def shuff():
	global mode
	global artist
	if artist=="M":
		with open ("playlist/muse.txt") as f:
			songList=f.readlines()
		songList=[x.strip() for x in songList]
	elif artist=="A":
		with open ("playlist/Aqours.txt") as f:
			songList=f.readlines()
		songList=[x.strip() for x in songList]
	else:
		songList=os.listdir(mode)
	artist="none"
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
	msg=ctx.message.content.replace("!music ","")
	global mode
	global artist
	mode="../Mari/music/"
	if msg.lower()=="muse" or msg.lower()=="u\'s" or "μ" in msg.lower():
		artist="M"
	elif msg.lower()=="aqours":
		artist="A"
	else:
		artist="none"
	if msg.lower()=="aquors":
		await ctx.send("never heard of them")
	global message
	if message!=2:
		message=1
		bot.loop.create_task(play(ctx))


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
file_object=open("key.txt","r")
bot.run(file_object.read().strip())
