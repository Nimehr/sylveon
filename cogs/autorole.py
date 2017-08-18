import discord
import itertools
import os
import operator
from .utils.dataIO import dataIO
from discord.ext import commands
from cogs.utils import checks

class Autorole:
	def __init__(self, bot):
		self.bot = bot

	global mmo
	global fps
	global moba
	global milsim
	global strategy
	global sandbox
	global genres
	mmo = ["Black Desert Online","World of Warcraft","FINAL FANTASY XIV - A Realm Reborn"]
	fps = ["PAYDAY 2","Overwatch","Counter-Strike: Global Offensive","Rainbow Six Siege","Warframe"]
	moba = ["League of Legends","Heroes of the Storm"," DOTA 2"]
	milsim = ["Arma III", "Arma 3","Squad","PUBG"]
	strategy = ["Hearts of Iron IV", "Age of Mythology"]
	sandbox = ["Grand Theft Auto V","ARK"]
	genres = ["mmo", "fps", "moba", "milsim", "strategy", "sandbox"]

	async def on_member_update(self, before, after):
		genreRole = False
		if before.server is "298875467916640256":
			for role in before.roles:
				if role.name.lower() not in genres:
					await self.bot.send_message(before.server.get_channel("298875467916640256"),role.name.lower())
					genreRole = False

			if genreRole == False:
				try:
					await self.bot.send_message(before.server.get_channel("298875467916640256"), "User {} doesn't have a genre role".format(before.mention))
				except Exception:
					pass

	# async def on_member_update(self, before, after):
	# 	async def roleApply(genre):
	# 		member = after
	# 		roleApplied = False
	# 		for role in server.roles:
	# 			if role.name.lower() == genre.lower():
	# 				for userRole in member.roles:
	# 					if str(userRole).lower() == genre.lower():
	# 						roleApplied = True
	# 						break
	# 					else:
	# 						roleApplied = False
	# 				if roleApplied == False:
	# 					await self.bot.add_roles(member, role)
	# 					msg = "Role {} added to {}".format(str(role), str(member))
	# 					await self.bot.send_message(channel, msg)

	# 	server = self.bot.get_server("274162627901521921")
	# 	channel = server.get_channel("325345364364492811")
	# 	if after in server.members:
	# 		# await self.bot.send_message(channel, str(after.game))
	# 		for gameMMO, gameFPS, gameMOBA, gameMilSim, gameStrategy in itertools.zip_longest(mmo, fps, moba, milsim, strategy):
	# 			if after.game.name == gameMMO or before.game.name == gameMMO:
	# 				await roleApply("mmo")
	# 				continue

	# 			elif after.game.name == gameFPS or before.game.name == gameFPS:	
	# 				await roleApply("fps")
	# 				continue

	# 			elif after.game.name == gameMOBA or before.game.name == gameMOBA:
	# 				await roleApply("moba")
	# 				continue

	# 			elif after.game.name == gameMilSim or before.game.name == gameMilSim:
	# 				await roleApply("milsim")
	# 				continue

	# 			elif after.game.name == gameStrategy or before.game.name == gameStrategy:
	# 				await roleApply("strategy")
	# 				continue

				# if str(after.game) == "The Long Dark":
				# 	await self.bot.send_message(channel, str(roleUtil))
				# 	if str(currentRolesBefore) != "tst":
				# 		await self.bot.add_roles(member, roleUtil)
				# 		await self.bot.send_message(channel, "Role added")

	@commands.command(pass_context=True, no_pm=True)
	@checks.admin_or_permissions(manage_roles=True)
	async def autorole(self, ctx):
		async def roleApply(genre):
			roleApplied = False
			for role in server.roles:
				if role.name.lower() == genre.lower():
					for userRole in member.roles:
						if str(userRole).lower() == genre.lower():
							roleApplied = True
							break
						else:
							roleApplied = False
					if roleApplied == False:
						await self.bot.add_roles(member, role)
						msg = "Role {} added to {}".format(str(role), str(member))
						await self.bot.say(msg)

		user = ctx.message.author
		server = ctx.message.server
		members = server.members

		for member in members:
			if not member:
				continue
			if not member.game or not member.game.name:
				continue
			if member.bot:
				continue
			for gameMMO, gameFPS, gameMOBA, gameMilSim, gameStrategy in itertools.zip_longest(mmo, fps, moba, milsim, strategy):

				if member.game.name == gameMMO:
					await roleApply("mmo")
					continue

				elif member.game.name == gameFPS:	
					await roleApply("shooter")
					continue

				elif member.game.name == gameMOBA:
					await roleApply("moba")
					continue

				elif member.game.name == gameMilSim:
					await roleApply("milsim")

				elif member.game.name == gameStrategy:
					await roleApply("strategy")

	# @commands.command(pass_context=True, name="setchannel")
	# @checks.admin_or_permissions(manage_roles=True)
	# async def setChannel(self, context):
	# 	server = context.message.server
	# 	file_path = "data/kms/settings.json"
	# 	currentChannel = context.message.channel.id
	# 	settings = settings[server.id] = {"channel":str(currentChannel)}
	# 	await self.bot.say("I will send role notifications to this channel")
	# 	dataIO.save_json(file_path, settings)

def check_folder():
	if not os.path.exists("data/kms"):
		print("Creating data/settings folder...")
		os.makedirs("data/kms")


def check_file():
	settings = {}

	f = "data/kms/settings.json"
	if not dataIO.is_valid_json(f):
		print("Creating default settings.json...")
		dataIO.save_json(f, settings)

def setup(bot):
	check_folder()
	check_file()
	n = Autorole(bot)
	bot.add_cog(n)