import discord
import time
import datetime
from discord.ext import commands
from apscheduler.schedulers.background import BackgroundScheduler

class opAlert:

	# global utcDatetime
	# utcDatetime = datetime.datetime.utcnow()
	# utcDatetime.strftime("%Y-%m-%d %H:%M:%S")
	# global opHour
	# opHour = 19
	# global now
	# now = {
	# "day" : utcDatetime.strftime("%a"),
	# "hour" : utcDatetime.strftime("%H"),
	# "minute" : utcDatetime.strftime("%M"),
	# "hourInt" : int(utcDatetime.strftime("%H"))+1,
	# "minuteInt" : int(utcDatetime.strftime("%M"))
	# }

	# def __init__(self, bot):
	# 	self.bot = bot

	# async def opAuto(self):
	# 	nowHour = int(utcDatetime.strftime("%H"))
	# 	nowMinute = int(utcDatetime.strftime("%M"))
	# 	nowSecond = utcDatetime.strftime("%S")
	# 	starttime=time.time()
	# 	await self.bot.say("Hello World")
	# 	while True:
			# if nowHour == 10 and nowMinute == nowMinute+1:
			# 	await self.bot.say("Hello World 1")
			# 	time.sleep(30.0 - ((time.time() - starttime) % 30.0))
			# if nowHour == 10 and nowMinute == nowMinute+2:
			# 	await self.bot.say("Hello World 2")
			# 	time.sleep(30.0 - ((time.time() - starttime) % 30.0))
			# if nowHour == 10 and nowMinute == nowMinute+3:
			# 	await self.bot.say("Hello World 3")
			# 	time.sleep(30.0 - ((time.time() - starttime) % 30.0))
		# await self.bot.say(str(nowHour) + ":" + str(nowMinute))
		# if nowHour == 20 and nowMinute == 19:
		# 	await self.bot.say("1")
		# 	await time.sleep(60)
		# 	await self.bot.say("2")
		# 	await time.sleep(60)
			# await self.bot.say("3")
			# if nowHour == 19 and nowMinute == 10:
			# 	await self.bot.say("48")
			# 	# time.sleep(1.0 - ((time.time() - starttime) % 1.0))
			# if nowHour == 20 and nowMinute == 11:
			# 	await self.bot.say("49")
			# 	# time.sleep(1.0 - ((time.time() - starttime) % 1.0))

	# @commands.command(name="op")
	# async def op(self):
	# 	# if str(now["day"]) is "Sun":
	# 	hourOP = opHour - now["hourInt"]
	# 	minuteOP = 60 - now["minuteInt"]
	# 	msg = "The OP is in {} hours and {} minutes".format(str(hourOP), str(minuteOP))
	# 	await self.bot.say(msg)

def setup(bot):
	bot.add_cog(opAlert(bot))
