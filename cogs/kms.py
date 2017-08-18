import discord
import json
import os
import datetime
import discord.utils
import subprocess
import random
from .utils.dataIO import dataIO
from discord.ext import commands

class kms:
	"""My custom cog that does stuff!"""

	global settings
	global file_path
	settings = dataIO.load_json("data/kms/test.json")
	file_path = "data/kms/test.json"

	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def boobs(self, ctx):
		if "nsfw" in ctx.message.channel.name.lower():
			num = random.randrange(10000)
			strNum = str(num)
			if(len(strNum) < 5):
				for i in range(5 - len(strNum)):
					strNum = "0" + strNum
					i += 1
			msg = "http://media.oboobs.ru/boobs_preview/{}.jpg".format(str(strNum))
			await self.bot.say(msg)
		else:
			await self.bot.say("Please mark this channel as nsfw by adding a \"nsfw\" tag")

	@commands.command(pass_context=True)
	async def butts(self, ctx):
		if "nsfw" in ctx.message.channel.name.lower():
			num = random.randrange(4500)
			strNum = str(num)
			if(len(strNum) < 5):
				for i in range(5 - len(strNum)):
					strNum = "0" + strNum
					i += 1
			msg = "http://media.obutts.ru/butts_preview/{}.jpg".format(str(strNum))
			await self.bot.say(msg)
		else:
			await self.bot.say("Please mark this channel as nsfw by adding a \"nsfw\" tag")

	# async def on_server_emojis_update(self, before, after):
	# 	server = self.bot.get_server("298875467916640256")
	# 	channel = server.get_channel("326077398002958337")
	# 	diff = list(set(before) - set(after))
	# 	for emote in diff:
	# 		if diff == []:
	# 			diff = diff = list(set(after) - set(before))
	# 			await self.bot.send_message(channel, "New emote added: " + str(emote))
	# 		else:
	# 			await self.bot.send_message(channel, "Emote removed: " + str(emote))
				
	# async def on_member_update(self, before, after):
	# 	server = self.bot.get_server("298875467916640256")
	# 	serverRoles = server.roles
	# 	channel = server.get_channel("326077398002958337")
	# 	roleUtil = discord.utils.get(serverRoles, name="tst")
	# 	currentRolesBefore = discord.utils.get(before.roles, name="tst")
	# 	member = discord.utils.get(server.members, name="Nimehr✿")

	# 	if before in server.members:
	# 		await self.bot.send_message(channel, str(after.game))
	# 		if str(after.game) == "The Long Dark":
	# 			await self.bot.send_message(channel, str(roleUtil))
	# 			if str(currentRolesBefore) != "tst":
	# 				await self.bot.add_roles(member, roleUtil)
	# 				await self.bot.send_message(channel, "Role added")
		
	@commands.command(pass_context=True)
	async def roleadd(self, ctx):
		server = self.bot.get_server("298875467916640256")
		serverRoles = server.roles
		author = ctx.message.author
		channel = server.get_channel("326077398002958337")
		rolesChannel = discord.utils.get(server.channels, name="roles")
		await self.bot.say(server.channels)
		await self.bot.say(rolesChannel)
		await self.bot.send_message(rolesChannel, "@Rem Farron#4127 ily")

	@commands.group(pass_context=True, no_pm=True)
	async def grouptest(self, ctx):
		await self.bot.say("grouptest")

	# def fetch_joined_at(self, user, server):
	# 		"""Just a special case for someone special :^)"""
	# 		if user.id == "96130341705637888" and server.id == "133049272517001216":
	# 			return datetime.datetime(2016, 1, 10, 6, 8, 4, 443000)
	# 		else:
	# 			return user.joined_at

	# @commands.command(pass_context=True, no_pm=True)
	# async def joindate(self, ctx, *, user: discord.Member=None):
	# 	author = ctx.message.author
	# 	server = ctx.message.server

	# 	if not user:
	# 		user = author

	# 	joined_at = self.fetch_joined_at(user, server)
	# 	since_created = (ctx.message.timestamp - user.created_at).days
	# 	since_joined = (ctx.message.timestamp - joined_at).days
	# 	user_joined = joined_at.strftime("%d %b %Y %H:%M")
	# 	user_created = user.created_at.strftime("%d %b %Y %H:%M")
	# 	global utcDatetime
	# 	utcDatetime = datetime.datetime.utcnow()
	# 	await self.bot.say(str(utcDatetime))

	# 	created_on = "{}\n({} days ago)".format(user_created, since_created)
	# 	joined_on = "{}\n({} days ago)".format(user_joined, since_joined)

	# 	await self.bot.say(created_on)
	# 	await self.bot.say(joined_on)
		
			# else:
			# 	await self.bot.say("This user isn't in the guild")
			# 	break

	@commands.command(pass_context=True)
	async def testmsg(self,context,*,msg:str):
		await self.bot.say(msg)

# 	@commands.command(pass_context=True, name="setchannel")
# 	async def setChannel(self, context):

# 		server = context.message.server
		
# 		currentChannel = context.message.channel.id
# 		await self.bot.say(settings[server.id]["channel"])
# 		settings[server.id]["channel"] = currentChannel
# 		await self.bot.say("I will send role notifications to this channel")
# 		dataIO.save_json(file_path, settings)

# def check_folder():
# 	if not os.path.exists("data/kms"):
# 		print("Creating data/settings folder...")
# 		os.makedirs("data/kms")


# def check_file():
# 	settings = {}

# 	f = "data/kms/settings.json"
# 	if not dataIO.is_valid_json(f):
# 		print("Creating default settings.json...")
# 		dataIO.save_json(f, settings)

	

def setup(bot):
	# check_folder()
	# check_file()
	bot.add_cog(kms(bot))