import discord
import os
import aiohttp
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

#when bots online
@bot.event
async def on_ready():
	print(f'Bot: {bot.user} I am down for you!')

#when someone texts "!hello"
@bot.command()
async def hello(ctx):
	await ctx.send(f"Whats dawg? {ctx.author.name}! I am your servant.")

@bot.command()
async def bothelp(ctx):
	await ctx.send(f"""**List of commands:**
		`!fortune`:    Random quotes
		`!literature`: Literature quotes
		`!riddle`:     Random riddles
		`!weather` [city]: Check weather in your location
		`!define`: [word]: Give definition of your words
		""")

@bot.command()
async def fortune(ctx):
	import subprocess
	try:
		answer = subprocess.check_output("fortune", shell=True, text=True)
		await ctx.send(f"--->{answer}")
	except:
		await ctx.send("Something ain't right.")

@bot.command()
async def literature(ctx):
	import subprocess
	try:
		answer = subprocess.check_output("fortune literature", shell=True, text=True)
		await ctx.send(f"--->{answer}")
	except:
		await ctx.send("Something ain't right.")

@bot.command()
async def riddle(ctx):
	import subprocess
	try:
		answer = subprocess.check_output("fortune riddles", shell=True, text=True)
		await ctx.send(f"--->{answer}")
	except:
		await ctx.send("Something ain't right.")

@bot.command()
async def wiki(ctx, *, text: str):
	import subprocess
	try:
		answer = subprocess.check_output("wikit {text}", shell=True).decode()
		await ctx.send(f"--->{answer}")
	except:
		await ctx.send("Something ain't right.")

@bot.command()
async def weather(ctx, *, location=""):
	import subprocess
	if location == "":
		await ctx.send("!!!Add location. For example, '!weather hochiminh'")
		return
	try:
		location = ''.join(word.capitalize() for word in location.split())
		answer=subprocess.check_output(f"curl -s wttr.in/{location}?format=3", shell=True).decode().strip()
		embed = discord.Embed(
			title = f"🌦️ Weather Forecast",
			description=answer,
			color =discord.Color.blue()
			)
		embed.set_footer(text=f"Requested by {ctx.author.name}")
		await ctx.send(embed=embed)
	except Exception as e:
		# await ctx.send(f"❌ Error: {str(e)}")
		await ctx.send(f"❌ Disconnected, try again!")

@bot.command()
async def whatis(ctx, *, word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()

                entry = data[0]
                word_text = entry['word'].capitalize()
                phonetic = entry.get('phonetic', 'No IPA available.')
                meanings = entry['meanings']

                embed = discord.Embed(
                    title=f"📚 Definition of {word_text}",
                    description=f"**Pronunciation:** {phonetic}",
                    color=discord.Color.green()
                )

                for meaning in meanings[:2]:  # Only show first 2 types to avoid overload
                    part_of_speech = meaning['partOfSpeech'].capitalize()
                    definition = meaning['definitions'][0]['definition']
                    example = meaning['definitions'][0].get('example', 'No example available.')
                    synonyms = meaning['definitions'][0].get('synonyms', [])

                    field_value = f"**Meaning:** {definition}\n**Example:** {example}"

                    if synonyms:
                        syn_list = ', '.join(synonyms[:5])  # show max 5 synonyms
                        field_value += f"\n**Synonyms:** {syn_list}"

                    embed.add_field(
                        name=f"__{part_of_speech}__",
                        value=field_value,
                        inline=False
                    )

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Sorry, I couldn't find the word `{word}`.")

#initate the bot
load.dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
