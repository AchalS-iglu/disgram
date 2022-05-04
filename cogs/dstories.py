import sqlite3
import discord
from discord import app_commands
from discord.ext import commands

import json, os

class DStories(commands.Cog, name="dstories"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    group = app_commands.Group(name="dstories", description="...")
        
    @group.command(name="test")
    async def my_top_command(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Test", ephemeral=True)
    
    @group.command(name="adduser")
    async def adduser(self, interaction: discord.Interaction, username: str, channel: discord.TextChannel) -> None:
        user_id = self.bot.igclient.user_id_from_username(username)
        guild_id = interaction.guild_id
        
        self.bot.cur.execute(f"""CREATE TABLE IF NOT EXISTS "{guild_id}" (
            "user" INTEGER NOT NULL,
            "channel" INTEGER NOT NULL DEFAULT 0,
            "posts_sent" TEXT NOT NULL DEFAULT '',
            "stories_sent" TEXT NOT NULL DEFAULT '',
            PRIMARY KEY ("user")
            )""")
        self.bot.cur.execute(f"""INSERT INTO """)        
        self.bot.conn.commit()
        self.bot.dblog.write(f'ADDUSER: User {user_id} has been added to {guild_id} with channel set as {channel.id}.')
        # os.mkdir(f'data/{guild_id}')
        # with open(f'data/{guild_id}/users.json', 'a') as f:
        #     data = str(guild_id) + "-" + str(channel.id) + '\n'
        #     f.write(data)            
        # with open(f'data/{guild_id}/users/stories/{user_id}.json', 'w') as f:
        #     pass
        # with open(f'data/{guild_id}/users/posts/{user_id}.json', 'w') as f:
        #     pass
        await interaction.response.send_message(f"User has {username} been added to tracking list.")
    
    @group.command(name='setchannel')
    async def setchannel(self, interaction: discord.Interaction, user: str, channel: discord.TextChannel):
        pass
        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DStories(bot), guild=discord.Object(id=783054832465346591))