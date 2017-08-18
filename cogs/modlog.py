from discord.ext import commands
from cogs.utils import checks
import datetime
from cogs.utils.dataIO import fileIO
import discord
import asyncio
import os
from random import choice, randint

inv_settings = {"embed": False, "Channel": None, "toggleedit": False, "toggledelete": False, "toggleuser": False,
				"toggleroles": False,
				"togglevoice": False,
				"toggleban": False, "togglejoin": False, "toggleleave": False, "togglechannel": False,
				"toggleserver": False}


class ModLog:
	def __init__(self, bot):
		self.bot = bot
		self.direct = "data/modlogset/settings.json"

	global fmt
	fmt = "%H:%M:%S"

	@checks.admin_or_permissions(administrator=True)
	@commands.group(name='modlogtoggle', pass_context=True, no_pm=True)
	async def modlogtoggles(self, ctx):
		"""toggle which server activity to log"""
		if ctx.invoked_subcommand is None:
			db = fileIO(self.direct, "load")
			server = ctx.message.server
			# await self.bot.send_cmd_help(ctx)
			try:
				e = discord.Embed(title="Setting for {}".format(server.name), colour=discord.Colour.blue())
				e.add_field(name="Delete", value=str(db[ctx.message.server.id]['toggledelete']))
				e.add_field(name="Edit", value=str(db[ctx.message.server.id]['toggleedit']))
				e.add_field(name="Roles", value=str(db[ctx.message.server.id]['toggleroles']))
				e.add_field(name="User", value=str(db[ctx.message.server.id]['toggleuser']))
				e.add_field(name="Voice", value=str(db[ctx.message.server.id]['togglevoice']))
				e.add_field(name="Ban", value=str(db[ctx.message.server.id]['toggleban']))
				e.add_field(name="Join", value=str(db[ctx.message.server.id]['togglejoin']))
				e.add_field(name="Leave", value=str(db[ctx.message.server.id]['toggleleave']))
				e.add_field(name="Channel", value=str(db[ctx.message.server.id]['togglechannel']))
				e.add_field(name="Server", value=str(db[ctx.message.server.id]['toggleserver']))
				e.set_thumbnail(url=server.icon_url)
				await self.bot.say(embed=e)
			except KeyError:
				return

	@checks.admin_or_permissions(administrator=True)
	@commands.group(pass_context=True, no_pm=True)
	async def modlogset(self, ctx):
		"""Change modlog settings"""
		if ctx.invoked_subcommand is None:
			await self.bot.send_cmd_help(ctx)

	@modlogset.command(name='channel', pass_context=True, no_pm=True)
	async def _channel(self, ctx):
		"""Set the channel to send notifications too"""
		server = ctx.message.server
		db = fileIO(self.direct, "load")
		if ctx.message.server.me.permissions_in(ctx.message.channel).send_messages:
			if server.id in db:
				db[server.id]['Channel'] = ctx.message.channel.id
				fileIO(self.direct, "save", db)
				await self.bot.say("Channel changed.")
				return
			if not server.id in db:
				db[server.id] = inv_settings
				db[server.id]["Channel"] = ctx.message.channel.id
				fileIO(self.direct, "save", db)
				await self.bot.say("I will now send toggled modlog notifications here")
		else:
			return

	@modlogset.command(pass_context=True, no_pm=True)
	async def embed(self, ctx):
		"""Enables or disables embed modlog."""
		server = ctx.message.server
		db = fileIO(self.direct, "load")
		if db[server.id]["embed"] == False:
			db[server.id]["embed"] = True
			fileIO(self.direct, "save", db)
			await self.bot.say("Enabled embed modlog.")
		elif db[server.id]["embed"] == True:
			db[server.id]["embed"] = False
			fileIO(self.direct, "save", db)
			await self.bot.say("Disabled embed modlog.")

	@modlogset.command(pass_context=True, no_pm=True)
	async def disable(self, ctx):
		"""disables the modlog"""
		server = ctx.message.server
		db = fileIO(self.direct, "load")
		if not server.id in db:
			await self.bot.say("Server not found, use modlogset to set a channnel")
			return
		del db[server.id]
		fileIO(self.direct, "save", db)
		await self.bot.say("I will no longer send modlog notifications here")

	@modlogtoggles.command(pass_context=True, no_pm=True)
	async def edit(self, ctx):
		"""toggle notifications when a member edits theyre message"""
		server = ctx.message.server
		db = fileIO(self.direct, "load")
		if db[server.id]["toggleedit"] == False:
			db[server.id]["toggleedit"] = True
			fileIO(self.direct, "save", db)
			await self.bot.say("Edit messages enabled")
		elif db[server.id]["toggleedit"] == True:
			db[server.id]["toggleedit"] = False
			fileIO(self.direct, "save", db)
			await self.bot.say("Edit messages disabled")

	@modlogtoggles.command(pass_context=True, no_pm=True)
	async def join(self, ctx):
		"""toggles notofications when a member joins the server."""
		server = ctx.message.server
		db = fileIO(self.direct, "load")
		if db[server.id]["togglejoin"] == False:
			db[server.id]["togglejoin"] = True
			fileIO(self.direct, "save", db)
			await self.bot.say("Enabled join logs.")
		elif db[server.id]['togglejoin'] == True:
			db[server.id]['togglejoin'] = False
			fileIO(self.direct, 'save', db)
			await self.bot.say("Disabled join logs.")

	@modlogtoggles.command(pass_context=True, no_pm=True)
	async def server(self, ctx):
		"""toggles notofications when the server updates."""
		server = ctx.message.server
		db = fileIO(self.direct, "load")
		if db[server.id]["toggleserver"] == False:
			db[server.id]["toggleserver"] = True
			fileIO(self.direct, "save", db)
			await self.bot.say("Enabled server logs.")
		elif db[server.id]['toggleserver'] == True:
			db[server.id]['toggleserver'] = False
			fileIO(self.direct, 'save', db)
			await self.bot.say("Disabled server logs.")

	@modlogtoggles.command(pass_context=True, no_pm=True)
	async def channel(self, ctx):
		"""toggles channel update logging for the server."""
		server = ctx.message.server
		db = fileIO(self.direct, "load")
		if db[server.id]["togglechannel"] == False:
			db[server.id]["togglechannel"] = True
			fileIO(self.direct, "save", db)
			await self.bot.say("Enabled channel logs.")
		elif db[server.id]['togglechannel'] == True:
			db[server.id]['togglechannel'] = False
			fileIO(self.direct, 'save', db)
			await self.bot.say("Disabled channel logs.")

	@modlogtoggles.command(pass_context=True, no_pm=True)
	async def leave(self, ctx):
		"""toggles notofications when a member leaves the server."""
		server = ctx.message.server
		db = fileIO(self.direct, "load")
		if db[server.id]["toggleleave"] == False:
			db[server.id]["toggleleave"] = True
			fileIO(self.direct, "save", db)
			await self.bot.say("Enabled leave logs.")
		elif db[server.id]['toggleleave'] == True:
			db[server.id]['toggleleave'] = False
			fileIO(self.direct, 'save', db)
			await self.bot.say("Disabled leave logs.")

	@modlogtoggles.command(pass_context=True, no_pm=True)
	async def delete(self, ctx):
		"""toggle notifications when a member delete theyre message"""
		server = ctx.message.server
		db = fileIO(self.direct, "load")
		if db[server.id]["toggledelete"] == False:
			db[server.id]["toggledelete"] = True
			fileIO(self.direct, "save", db)
			await self.bot.say("Delete messages enabled")
		elif db[server.id]["toggledelete"] == True:
			db[server.id]["toggledelete"] = False
			fileIO(self.direct, "save", db)
			await self.bot.say("Delete messages disabled")

	@modlogtoggles.command(pass_context=True, no_pm=True)
	async def user(self, ctx):
		"""toggle notifications when a user changes his profile"""
		server = ctx.message.server
		db = fileIO(self.direct, "load")
		if db[server.id]["toggleuser"] == False:
			db[server.id]["toggleuser"] = True
			fileIO(self.direct, "save", db)
			await self.bot.say("User messages enabled")
		elif db[server.id]["toggleuser"] == True:
			db[server.id]["toggleuser"] = False
			fileIO(self.direct, "save", db)
			await self.bot.say("User messages disabled")

	@modlogtoggles.command(pass_context=True, no_pm=True)
	async def roles(self, ctx):
		"""toggle notifications when roles change"""
		server = ctx.message.server
		db = fileIO(self.direct, "load")
		if db[server.id]["toggleroles"] == False:
			db[server.id]["toggleroles"] = True
			fileIO(self.direct, "save", db)
			await self.bot.say("Role messages enabled")
		elif db[server.id]["toggleroles"] == True:
			db[server.id]["toggleroles"] = False
			fileIO(self.direct, "save", db)
			await self.bot.say("Role messages disabled")

	@modlogtoggles.command(pass_context=True, no_pm=True)
	async def voice(self, ctx):
		"""toggle notifications when voice status change"""
		server = ctx.message.server
		db = fileIO(self.direct, "load")
		if db[server.id]["togglevoice"] == False:
			db[server.id]["togglevoice"] = True
			fileIO(self.direct, "save", db)
			await self.bot.say("Voice messages enabled")
		elif db[server.id]["togglevoice"] == True:
			db[server.id]["togglevoice"] = False
			fileIO(self.direct, "save", db)
			await self.bot.say("Voice messages disabled")

	@modlogtoggles.command(pass_context=True, no_pm=True)
	async def ban(self, ctx):
		"""toggle notifications when a user is banned"""
		server = ctx.message.server
		db = fileIO(self.direct, "load")
		if db[server.id]["toggleban"] == False:
			db[server.id]["toggleban"] = True
			fileIO(self.direct, "save", db)
			await self.bot.say("Ban messages enabled")
		elif db[server.id]["toggleban"] == True:
			db[server.id]["toggleban"] = False
			fileIO(self.direct, "save", db)
			await self.bot.say("Ban messages disabled")

	@modlogtoggles.command(pass_context=True, no_pm=True)
	async def all(self, ctx):
		"""toggles every notification"""
		server = ctx.message.server
		db = fileIO(self.direct, "load")
		db[server.id]["toggleban"] = True
		db[server.id]["togglechannel"] = True
		db[server.id]["toggledelete"] = True
		db[server.id]["toggleedit"] = True
		db[server.id]["togglejoin"] = True
		db[server.id]["toggleleave"] = True
		db[server.id]["toggleroles"] = True
		db[server.id]["toggleserver"] = True
		db[server.id]["toggleuser"] = True
		db[server.id]["togglevoice"] = True
		fileIO(self.direct, "save", db)
		await self.bot.say("All permissions enabled")

	async def on_message_delete(self, message):
		server = message.server
		db = fileIO(self.direct, "load")
		if not server.id in db:
			return
		if db[server.id]['toggledelete'] == False:
			return
		if message.author is message.author.bot:
			pass
		channel = db[server.id]["Channel"]
		time = datetime.datetime.now()
		cleanmsg = message.content
		for i in message.mentions:
			cleanmsg = cleanmsg.replace(i.mention, str(i))
		msg = "`{}` {}:paintbrush: **{}** *deleted his/her message*\n {}".format(
			time.strftime(fmt), message.channel.mention, message.author, cleanmsg)
		await self.bot.send_message(server.get_channel(channel),
									msg)

	async def on_member_join(self, member):
		server = member.server
		# author = ctx.message.author
		# server = ctx.message.server

		since_created = (datetime.datetime.utcnow() - member.created_at).days
		user_created = member.created_at.strftime("%d %b %Y %H:%M")

		created_on = "{} ({} days ago)".format(user_created, since_created)
		db = fileIO(self.direct, 'load')
		if not server.id in db:
			return
		if db[server.id]['togglejoin'] == False:
			return
		channel = db[server.id]["Channel"]
		time = datetime.datetime.now()
		if since_created < 30:
			msg = "`{}` :white_check_mark: :bangbang: *New account!* __**{}**__ (*{}*) **joined the server** `Account created {}`".format(time.strftime(fmt), member.name, member.id, created_on, users)
			await self.bot.send_message(server.get_channel(channel), msg)
		else:
			msg = "`{}` :white_check_mark: __**{}**__ (*{}*) **joined the server** `Account created {}`".format(time.strftime(fmt), member.name, member.id, created_on)
			await self.bot.send_message(server.get_channel(channel), msg)
		if member.avatar == None:
			await self.bot.send_message(server.get_channel(channel), "The user {} doesn't have an avatar. Please remind them to get one :smile:".format(member.mention))

	async def on_member_remove(self, member):
		server = member.server
		users = len([e.name for e in server.members])
		db = fileIO(self.direct, 'load')
		if not server.id in db:
			return
		if db[server.id]['toggleleave'] == False:
			return
		channel = db[server.id]["Channel"]
		time = datetime.datetime.now()
		users = len([e.name for e in server.members])
		msg = "`{}` :no_entry: __**{}**__ (*{}*) **left the server**".format(time.strftime(fmt), member.name, member.id)
		await self.bot.send_message(server.get_channel(channel), msg)

	async def on_channel_update(self, before, after):
		server = before.server
		db = fileIO(self.direct, 'load')
		if not server.id in db:
			return
		if db[server.id]['togglechannel'] == False:
			return
		channel = db[server.id]["Channel"]
		time = datetime.datetime.now()
		msg = ""
		if before.name != after.name:
			if before.type == discord.ChannelType.voice:
				await self.bot.send_message(server.get_channel(channel),
											"`{}` :loud_sound: Voice channel name update. Before: **{}** After: **{}**.".format(
												time.strftime(fmt), before.name, after.name))
			if before.type == discord.ChannelType.text:
				await self.bot.send_message(server.get_channel(channel),
											"`{}` :page_facing_up: Text channel name update. Before: **{}** After: **{}**.".format(
												time.strftime(fmt), before.name, after.name))
		if before.topic != after.topic:
			await self.bot.send_message(server.get_channel(channel),
										"`{}` :page_facing_up: Channel topic has been updated.\n**Before:** {}\n**After:** {}".format(
											time.strftime(fmt), before.topic, after.topic))
		if before.position != after.position:
			if before.type == discord.ChannelType.voice:
				await self.bot.send_message(server.get_channel(channel),
											"`{}` :loud_sound: Voice channel position update. Channel: **{}** Before: **{}** After: **{}**.".format(
												time.strftime(fmt), before.name, before.position, after.position))
			if before.type == discord.ChannelType.text:
					await self.bot.send_message(server.get_channel(channel),
												"`{}` :page_facing_up: Text channel position update. Channel: **{}** Before: **{}** After: **{}**.".format(
													time.strftime(fmt), before.name, before.position, after.position))
		if before.bitrate != after.bitrate:
			await self.bot.send_message(server.get_channel(channel),
										"`{}` :loud_sound: Channel bitrate update. Before: **{}** After: **{}**.".format(
											time.strftime(fmt), before.bitrate, after.bitrate))

	async def on_message_edit(self, before, after):
		server = before.server
		db = fileIO(self.direct, "load")
		if not server.id in db:
			return
		if db[server.id]['toggleedit'] == False:
			return
		if before.content == after.content:
			return
		if before.author.bot:
			return
		cleanbefore = before.content
		for i in before.mentions:
			cleanbefore = cleanbefore.replace(i.mention, str(i))
		cleanafter = after.content
		for i in after.mentions:
			cleanafter = cleanafter.replace(i.mention, str(i))
		channel = db[server.id]["Channel"]
		time = datetime.datetime.now()
		msg = "`{}` {} :pencil2: **{}** *edited his/her message:* \n**Original:**\n {}\n**Update:**\n {} ".format(
			time.strftime(fmt), before.channel.mention, before.author, cleanbefore, cleanafter)
		await self.bot.send_message(server.get_channel(channel),
									msg)

	async def on_server_update(self, before, after):
		server = before
		db = fileIO(self.direct, "load")
		if not server.id in db:
			return
		if db[server.id]['toggleserver'] == False:
			return
		if before.bot:
			return
		channel = db[server.id]["Channel"]
		time = datetime.datetime.now()
		if before.name != after.name:
			msg = "`{}` :globe_with_meridians: Server name update. Before: **{}** After: **{}**.".format(
				time.strftime(fmt), before.name, after.name)
		if before.region != after.region:
			msg = "`{}` :globe_with_meridians: Server region update. Before: **{}** After: **{}**.".format(
				time.strftime(fmt), before.region, after.region)
		await self.bot.send_message(server.get_channel(channel), msg)

	async def on_voice_state_update(self, before, after):
		server = before.server
		db = fileIO(self.direct, "load")
		if not server.id in db:
			return
		if db[server.id]['togglevoice'] == False:
			return
		if before.bot:
			return
		channel = db[server.id]["Channel"]
		time = datetime.datetime.now()
		await self.bot.send_message(server.get_channel(channel),
									":person_with_pouting_face::skin-tone-3: `{}` **{}'s** voice status has updated. **Channel**: {}\n**Local Mute:** {} **Local Deaf:** {} **Server Mute:** {} **Server Deaf:** {}".format(
										time.strftime(fmt), after.name, after.voice_channel, after.self_mute,
										after.self_deaf, after.mute, after.deaf))

	async def on_member_update(self, before, after):
		server = before.server
		db = fileIO(self.direct, "load")
		if not server.id in db:
			return
		if db[server.id]['toggleuser'] and db[server.id]['toggleroles'] == False:
			return
		channel = db[server.id]["Channel"]
		time = datetime.datetime.now()
		if not before.nick == after.nick:
			await self.bot.send_message(server.get_channel(channel),
										"`{}` :pencil2: **{}** *changed their nickname:*\n**Original:**\n {}\n**Update:**\n {} ".format(
											time.strftime(fmt), before.name, before.kick, after.nick))

	async def on_member_update(self, before, after):
		server = before.server
		db = fileIO(self.direct, "load")
		if not server.id in db:
			return
		if db[server.id]['toggleuser'] and db[server.id]['toggleroles'] == False:
			return
		channel = db[server.id]["Channel"]
		time = datetime.datetime.now()
		beforeRoles = ", ".join([r.name for r in before.roles if r.name != "@everyone"])
		afterRoles = ", ".join([r.name for r in after.roles if r.name != "@everyone"])
		if not before.roles == after.roles:
			msg = "`{}` :label: **{}'s** *roles have changed*\n**Original:** {}\n**Update:** {} ".format(
                    time.strftime(fmt), before.name, beforeRoles, afterRoles)
			await self.bot.send_message(server.get_channel(channel), msg)

	async def on_member_ban(self, member):
		server = member.server
		db = fileIO(self.direct, "load")
		if not server.id in db:
			return
		if db[server.id]['toggleban'] == False:
			return
		channel = db[server.id]["Channel"]
		time = datetime.datetime.now()
		msg = "`{}` :hammer: __**{}**__ (*{}*) has been banned from the server".format(time.strftime(fmt), member, member.id)
		await self.bot.send_message(server.get_channel(channel), msg)


def check_folder():
	if not os.path.exists('data/modlogset'):
		print('Creating data/modlogset folder...')
		os.makedirs('data/modlogset')


def check_file():
	f = 'data/modlogset/settings.json'
	if not fileIO(f, 'check'):
		print('Creating default settings.json...')
		fileIO(f, 'save', {})


def setup(bot):
	check_folder()
	check_file()
	bot.add_cog(ModLog(bot))
