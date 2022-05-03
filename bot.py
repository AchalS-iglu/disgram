import discord
from discord.ext import commands, tasks

import instagrapi

import os
from dotenv import load_dotenv
import aiohttp

load_dotenv()

igclient = instagrapi.Client()
igusername = os.getenv("IG_USER")
igpassword = os.getenv("IG_PASS")
igclient.login(username=igusername, password=igpassword)

intents = discord.Intents.default()
intents.message_content = True
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="ig", intents=intents)
        self.initial_extensions = [
            'cogs.dstories',
        ]
    
    async def setup_hook(self):
        self.background_task.start()
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def close(self):
        await super().close()
        await self.session.close()

    @tasks.loop(minutes=10)
    async def background_task(self):
        print('Running background task...')

    async def on_ready(self):
        print('Ready!')

bot = MyBot()

@bot.command(name='sync', sync='Syncs slash commands!')
async def sync(ctx):
    result = await bot.tree.sync(guild=discord.Object(id=783054832465346591))
    print(result)
    await ctx.reply("Synced")
    
bot.run(os.getenv('BOT_TOKEN'))
