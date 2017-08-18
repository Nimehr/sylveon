import re
import discord
from .utils import checks
from discord.ext import commands
from __main__ import send_cmd_help


class PARole:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context=True, no_pm=True, name="role")
	async def _role(self, context):
		"""Users with manage roles perms can add roles, users can apply or remove roles."""
		if context.invoked_subcommand is None:
			await send_cmd_help(context)

	@_role.command(pass_context=True, no_pm=True, name="new", aliases=["create"])
	@checks.mod_or_permissions(manage_roles=True)
	async def _newRole(self, context, colour, *role_name):
		"""Create a role
		-role add/new/create D3D3D3 Grey"""
		server = context.message.server
		if re.search(r"^(?:[0-9a-fA-F]{3}){1,2}$", colour):
			name = " ".join(role_name)
			colour = discord.Color(int(colour, 16))
			permissions = discord.Permissions(permissions=0)
			try:
				await self.bot.create_role(server, name=name, color=colour, permissions=permissions, hoist=False, mentionable=True)
				message = "New role created"
			except discord.Forbidden:
				message = "I dont have manage roles perms"
		else:
			message = "`Please input a valid Hex colour`"
		await self.bot.say(message)

	@_role.command(pass_context=True, no_pm=True, name="remove")
	async def _relieve(self, context, *role_name):
		"""Remove one of your roles"""
		server = context.message.server
		author = context.message.author
		name = " ".join(role_name)
		roles = [role.name.lower() for role in server.roles]
		if name.lower() in roles:
			for role in server.roles:
				if role.name.lower() == name.lower():
					try:
						await self.bot.remove_roles(author, role)
						message = "Role `{}` removed from {}".format(role.name, author.display_name)
						break
					except discord.Forbidden:
						message = "I have no permissions to do that. Please give me role managing permissions."
				else:
					message = "`Something went wrong...`"
		else:
			message = "There is no such role on this server"
		await self.bot.say(message)

	@_role.command(pass_context=True, no_pm=True, name="delete")
	@checks.mod_or_permissions(manage_roles=True)
	async def _remove(self, context, *role_name):
		"""Delete a role"""
		server = context.message.server
		name = " ".join(role_name)
		roles = [role.name.lower() for role in server.roles]
		if name.lower() in roles:
			for role in server.roles:
				if role.name.lower() == name.lower():
					if role.permissions.value < 1:
						try:
							await self.bot.delete_role(server, role)
							message = "Role {} removed".format(role.name)
							break
						except discord.Forbidden:
							message = "I dont have manage roles permissions"
					else:
						message = "This role has too many permissions"
				else:
					message = "`This role doesnt exist`"
		else:
			message = "This role doesnt exist"
		await self.bot.say(message)

	@_role.command(pass_context=True, no_pm=True, name="add")
	async def _apply(self, context, *role_name):
		"""Give yourself a role!"""
		server = context.message.server
		author = context.message.author
		name = " ".join(role_name)
		roles = [role.name.lower() for role in server.roles]
		if name.lower() in roles:
			for role in server.roles:
				if role.name.lower() == name.lower():
					if role.permissions.value < 1:
						try:
							await self.bot.add_roles(author, role)
							message = "You will now be pinged about {} notifications".format(role.name)
							break
						except discord.Forbidden:
							message = "I have no Manage Role permissions"
				else:
					message = "This role does not exist"
		else:
			message = "This role doesnt exist"
		await self.bot.say(message)

	@_role.command(pass_context=True, no_pm=True, name="list")
	async def _list(self, context):
		"""List all available roles"""
		server = context.message.server
		message = "```\nAvailable roles:\n"
		for role in server.roles:
			if role.permissions.value < 1:
				message += "\n{} ({})".format(role.name, len([member for member in server.members if ([r for r in member.roles if r.name == role.name])]))
		message += "```"
		await self.bot.say(message)


def setup(bot):
	n = PARole(bot)
	bot.add_cog(n)