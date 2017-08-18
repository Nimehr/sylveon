import discord
import time
from discord.ext import commands

class cooldown:
	global min_call_freq
	global used
	min_call_freq = 3600
	used = {}

	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def cmd(self, ctx, command):
		if (command not in used or time.time() - used[command] > min_call_freq):
			used[command] = time.time()
			await self.bot.say('Calling command `%s`.' % command)
		else:
			await self.bot.say(str(used[command]) + "\n" + str(min_call_freq))
			timeTilUseSeconds = used[command] - min_call_freq
			timeTilUseMinutes = timeTilUseSeconds
			await self.bot.say("The command can be used in {}".format("%.0f" % timeTilUseMinutes))#('You have used command `%s` in the last %u seconds.' % (command, min_call_freq/60/60))

def setup(bot):
	bot.add_cog(cooldown(bot))