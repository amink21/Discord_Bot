from nextcord import Intents, Embed, Color, ButtonStyle, Interaction, SlashOption
from nextcord.ui import Button, View
from nextcord.ext import commands
import datetime, asyncio
 
intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='', intents=intents)


@bot.slash_command()
async def speak(interaction: Interaction, msg:str, size: int = SlashOption(
	name ="pick",
	choices={"30px","50px", "70px"},
)):
	await interaction.response.send_message("hi")

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command(name="hi")
async def SendMessage(ctx):
    await ctx.send('Hello Amin!')
	
@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command(name= "thanks")
async def SendMessage2(ctx):
	await ctx.send("You're Welcome!")

@commands.cooldown(1, 5, commands.BucketType.user)
async def schedule_daily_message(h, m, s, msg, channelid):
	while True:
		now = datetime.datetime.now()
		# then = now+datetime.timedelta(days=1)
		then = now.replace(hour=h, minute=m, second=s)
		if then < now:
			then += datetime.timedelta(days=1)
		wait_time = (then-now).total_seconds()
		await asyncio.sleep(wait_time)

		channel = bot.get_channel(channelid)

		await channel.send(msg)
		await asyncio.sleep(1)
		
@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command(name="daily")
async def daily(ctx, mystr:str, hour:int, minute:int, second:int):
	print(mystr, hour, minute)

	if not (0 < hour < 24 and 0 <= minute <= 60 and 0 <= second < 60):
		raise commands.BadArgument()

	time = datetime.time(hour, minute, second)
	timestr = time.strftime("%I:%M:%S %p")
	await ctx.send(f"A daily message will be sent at {timestr} everyday in this channel.\nDaily message: \"{mystr}\"\nConfirm by simply saying: `yes`")
	try:
		msg = await bot.wait_for("message", timeout = 20, check = lambda message: message.author == ctx.author) 
	except asyncio.TimeoutError:
		await ctx.send("You took too long.")
		return 
	if msg.content == "yes":
		await ctx.send("Daily message started :)")
		await schedule_daily_message(hour, minute, second, mystr, ctx.channel.id)
	else:
		await ctx.send("Daily message cancelled :(")
		
@commands.cooldown(1, 5, commands.BucketType.user)		
@bot.command(name="portfolio")
async def portfolio(ctx):
	portBtn = Button(label = "Portfolio", url="https://aminkadawala.com/")
	async def portBtn_callback(interaction):
		await interaction.response.send_message()
	portBtn.callback = portBtn_callback
	myView = View(timeout=180)
	myView.add_item(portBtn)
	await ctx.send("Here is your portfolio: ", view=myView)

@commands.cooldown(1, 5, commands.BucketType.user)	
@bot.command(name="linkedln")
async def linkedln(ctx):
	linkedlnBtn = Button(label = "Linkedln", url="https://www.linkedin.com/in/amin-kadawala/")
	async def linkedlnBtn_callback(interaction):
		await interaction.response.send_message()
	linkedlnBtn.callback = linkedlnBtn_callback
	myView = View(timeout=180)
	myView.add_item(linkedlnBtn)
	await ctx.send("Here is your Linkedln profile: ", view=myView)

@commands.cooldown(1, 5, commands.BucketType.user)	
@bot.command(name="github")
async def github(ctx):
	githubBtn = Button(label = "Github", url="https://github.com/amink21")
	async def githubBtn_callback(interaction):
		await interaction.response.send_message()
	githubBtn.callback = githubBtn_callback
	myView = View(timeout=180)
	myView.add_item(githubBtn)
	await ctx.send("Here is your Github profile: ", view=myView)
		

@daily.error
async def daily_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await ctx.send("""Incorrect format. Use the command this way: `daily "message" hour minute second`.
For example: `daily "good morning" 10 30 0` for a message to be sent at 10:30 everyday""")

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		em = Embed(title=f"Slow it down!", description=f"Try Again in {error.retry_after:.2f}s.", color=Color.red())
		await ctx.send(embed=em)
		
@bot.event
async def on_ready():
    print(f"Logged in as: : {bot.user.name}")
    await schedule_daily_message(10, 00, 00, "Good Morning Amin! :)", 1187148206526709802)
    await schedule_daily_message(11, 59, 55, "Good Night Amin! :)", 1187148206526709802)

if __name__ == '__main__':
    bot.run("")
    
