import discord
import lichess.api
import requests

from discord.ext import commands
from discord import Color as color

DISCORD_TOKEN = "DISCORD AUTH TOKEN HERE"

users = {}
timeControls = ['bullet','blitz','rapid','classical']

#Accessing ratings
def getLichessRatings(userDiscordTag, lichessUser):
  #Creates list to store users discord tag, lichess username, and ratings
  userInfo = [] #Example used in images: ['(discord tag)', 'sonderliam', '2002', '2003','2019','1813','1945']
  userInfo.append(userDiscordTag)
  userInfo.append(lichessUser)

  #Uses lichess api to access the profile and retrieve ratings
  userProfile = lichess.api.user(lichessUser);

  #A '?' denotes the user hasn't played enough  to even have a provisional rating, playing 3-4 games is often enough to remove the '?'
  for timeControl in timeControls:
    userInfo.append('?') if userProfile['perfs'][timeControl]['rd'] > 230 else userInfo.append(str(userProfile['perfs'][timeControl]['rating']))
    
  userInfo.append('?') if userProfile['perfs']['puzzle']['games'] == 0  else userInfo.append(str(userProfile['perfs']['puzzle']['rating']))

  return userInfo

#Creating the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

#Sets lichess username/ratings to the current user
@bot.command(name="set")
async def set(ctx, lichessUsername):
  user = await bot.fetch_user(ctx.message.author.id)
  userDiscordTag = user.name + "#" + ctx.author.discriminator

  if userDiscordTag in users:
    del users[userDiscordTag]
    
  users[userDiscordTag] = lichessUsername
  
  await ctx.channel.send("Your profile has been set")

#See current list of all discord tags and their lichess usernames
@bot.command(name="usernames")
async def usernames(ctx):
  embed=discord.Embed(
    title = "Member list",
    color = color.dark_green()
  )
  
  embed.add_field(name = "Discord", value = "\n".join(list(users.keys())),inline = True)
  embed.add_field(name = "Lichess", value = "\n".join(list(users.values())),inline = True)

  await ctx.channel.send(embed=embed)

#Allows user to access their ratings via embed
@bot.command(name="ratings")
async def ratings(ctx, lichessUsername):
  user = await bot.fetch_user(ctx.message.author.id)
  userDiscordTag = user.name + "#" + ctx.author.discriminator
  
  lichessRatings = getLichessRatings(userDiscordTag, lichessUsername)
  
  embed=discord.Embed(
    title = "Ratings for " + userDiscordTag[:-5] + "\n" + "https://lichess.org/@/" + lichessRatings[1],
    color = color.dark_green()
  )
  
  embed.add_field(name = "Time Control", value = "\n".join(timeControls)+ "\npuzzles", inline = True)
  embed.add_field(name = "Ratings", value = "\n".join(lichessRatings[2:]), inline = True)
  
  await ctx.channel.send(embed=embed)

#Allows for an open ended challenge
@bot.command(name="challenge")
async def challenge(ctx, variant, initialTime, increment):
  params = {
    "variant": variant, 
    "clock.limit": int(initialTime) * 60,
    "clock.increment": int(increment), 
  }

  response = requests.post('https://lichess.org/api/challenge/open', data=params)

  link = response.json()['challenge']['url'];

  embed=discord.Embed(
    title = "Challenge link: " + link,
    color = color.dark_green()
  )

  await ctx.channel.send(embed=embed)
  
#Runs the bot
bot.run(DISCORD_TOKEN)
