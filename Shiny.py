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
import Music
import MessageHandler
import Management
import Events
import FunPosting


config=json.load(open('config.json'))

cogList=['Music','Management','Events','FunPosting']
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!', 'hey nep, ', 'Hey nep, ', 'Hey maribot, ','hey maribot, ', 'Hey Maribot, '), descripton='Shiny School Idol Bot!!')


bot.config=config
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
G_mentions=1
G_max=6
G_time=10
songs=['```']
global antiSpam,antiSpamCount,enable
enable=True
antiSpamCount={}
antiSpam={}

data=json.load(open('pastebin.json'))
api=PasteBinApi(dev_key=data['key'])
user_key=api.user_key(username=data['username'],password=data['password'])

def isDimi(ctx):
	return ctx.author.id==config["dimiId"]

async def botOwner(ctx):
	return ctx.author.id==config["myId"]

async def isMod(ctx):
	if ctx.author in discord.utils.find(lambda m: m.name=="Pretty Modder Head",ctx.guild.roles).members:
		return True
	return False

@bot.event
async def on_ready():
	print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))
	await bot.change_presence(activity=discord.Game('With KananBot'))
	bot.loop.create_task(noSpam())
	for cog in cogList:
		bot.load_extension(cog)

async def noSpam():
	global G_orig,G_repeat,G_max,G_time,antiSpamCount,antiSpam,disable
	while (True):
		try:
			for spammer in antiSpamCount.keys():
				if antiSpamCount[spammer]>=1:
					if len(antiSpam[spammer])==antiSpamCount[spammer]:
						antiSpam[spammer].pop(0)
					antiSpamCount[spammer]-=1
		except Exception as e:
			print (e)
		await asyncio.sleep(1)


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
		if len(message.mentions)>0:
			print(len(message.mentions))
			antiSpamCount[message.author.id]+=int(((len(message.mentions)+1)/2)*G_mentions)
		else:
			antiSpamCount[message.author.id]+=G_orig
		antiSpam[message.author.id].append(message.content)
	elif message.channel.id!=410486994699812864:
		antiSpam[message.author.id]=[message.content]
		antiSpamCount[message.author.id]=1
	try:
		if antiSpamCount[message.author.id]>G_max and enable:
			management=bot.get_cog("Management")
			await management.Mute(message.author,message.guild,-1)
			return (1)
	except Exception as e:
		print (e)
	if "<:" in message.content and message.author.bot is not True:
		await process(message)
	if message.channel.id==395743189283241995:
		return (1)
	await MessageHandler.handleNormal(message,config)
	if message.author.id==config["dimiId"] and ("maribot" in message.content.lower() or message.content.startswith("!")):
		await MessageHandler.handleDimi(message,config)
	#if message.channel.id==439643359745671180:
		#if len(message.attachments)>0 or ".png" in message.content or ".jpg" in message.content or "twitter.com/" in message.content.lower():
		#gRole=discord.utils.get(message.guild.roles,name="Giveaway")
		#await message.author.add_roles(gRole)
	await bot.process_commands(message)


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
		emoteList=bot.get_guild(175176337185701888).emojis
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


@bot.command(hidden=True)
@commands.check(isMod)
async def mute(ctx,member : discord.User = bot.user, minutes=-1):
	"""format is !mute @user minutes to mute"""
	await bot.get_cog("Management").Mute(ctx.guild.get_member(member.id),ctx.guild,minutes)


@bot.event
async def on_member_join(member):
	if "Shiny" in member.guild.name:
		for channel in member.guild.channels:
			if "welcome" in channel.name:
				welcomech=channel
			elif "awashima" in channel.name:
				defch=channel
		welcome=open("welcome.txt","r")
		welcomeMessage=welcome.read().format(member.mention,discord.utils.get(member.guild.emojis, name="itsjoke"),welcomech.mention)
		bot.loop.create_task(delayMessage(defch,welcomeMessage))


@bot.command(hidden=True)
@commands.check(botOwner)
async def restart(ctx):
	"""I will restart once I'm done with my work"""
	print ("attempting to restart")
	self.bot.loop.create_task(reset(ctx))

async def delayMessage(defch,welcomeMessage):
	global resetSafe
	resetSafe+=1
	#print( "member join")
	await asyncio.sleep(600)
	await defch.send(welcomeMessage)
	resetSafe-=1


async def reset(ctx):
	try:
		global resetSafe
		channel=open("channel.txt","r")
		ch=discord.utils.find(lambda m:m.id==402987335391772676,ctx.guild.voice_channels)
		i=0
		while i<60:
			if resetSafe==0 and len(ch.members)<2:
				try:
					owner=bot.get_user(config["myId"])
					await owner.send('resetting')
				except Exception as e:
					print("tried to send message to you, failed with: "+e)
				sys.exit()
			else:
				print (str(len(ch.members))+" left in vc and "+str(resetSafe)+" welcome messages atm")
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
					await ctx.message.guild.get_member(config["myId"]).send("resetting")
				except:
					""
				sys.exit()
			else:
				await asyncio.sleep(20)
	except:
		sys.exit(0)


@bot.command(hidden=True)
@commands.check(isMod)
async def listRole(ctx):
	roleName=ctx.message.content.replace("!listRole ","")
	role=discord.utils.find(lambda m:m.name.lower()==roleName.lower(),ctx.guild.roles)
	await ctx.send(str(random.choice(role.members)))


global message
global resetSafe
global banCoolDown
banCoolDown=0
resetSafe=0
message=0
file_object=open("key.txt","r")
bot.run(file_object.read().strip())
