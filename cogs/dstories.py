import sqlite3
from ssl import CHANNEL_BINDING_TYPES
import discord
from discord import app_commands
from discord.ext import commands

import datetime

class DStories(commands.Cog, name="dstories"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    group = app_commands.Group(name="dstories", description="...")
        
    @group.command(name="test")
    async def my_top_command(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Test", ephemeral=True)
    
    @group.command(name="adduser")
    async def adduser(self, interaction: discord.Interaction, username: str, channel: discord.TextChannel) -> None:
        await interaction.response.defer(ephemeral=False)
        user_id = self.bot.igclient.user_id_from_username(username)
        guild_id = interaction.guild_id
        
        self.bot.cur.execute(f"""CREATE TABLE IF NOT EXISTS "{guild_id}" (
            "user" INTEGER NOT NULL,
            "channel" INTEGER NOT NULL DEFAULT 0,
            "posts_sent" TEXT NOT NULL DEFAULT '',
            "stories_sent" TEXT NOT NULL DEFAULT '',
            PRIMARY KEY ("user")
            )""")
        self.bot.cur.execute(f"""SELECT "user", "channel"
                                       FROM "{guild_id}"
                                       WHERE "user" = '{user_id}'
                                       """)     
        output = self.bot.cur.fetchall()
      
        if len(output) == 0:
            self.bot.cur.execute(f"""INSERT INTO "{guild_id}" ("user", "channel")
                                 VALUES ('{user_id}', '{channel.id}')
                                 """)
            self.bot.conn.commit()
            self.bot.dblog.write(f'[{datetime.now.strftime("%d/%m/%Y %H:%M:%S")}]: ADDUSER: User {user_id} has been added to {guild_id} with channel set as {channel.id}.\n')
            await interaction.response.send_message(f"User has {username} been added to tracking list.")
        else:
            self.bot.cur.execute(f"""UPDATE "{guild_id}"
                                 SET "channel" = '{channel.id}'
                                 WHERE "user" = '{user_id}'
                                 """)
            self.bot.conn.commit()
            self.bot.dblog.write(f'[{datetime.now.strftime("%d/%m/%Y %H:%M:%S")}]: ADDUSER: User {user_id} of guild {guild_id} channel set to {channel.id}.\n')
            await interaction.response.send_message(f"User {username} was already in database although the channel has been updated")

    
    @group.command(name='updatechannel')
    async def setchannel(self, interaction: discord.Interaction, username: str, channel: discord.TextChannel):
        await interaction.response.defer(ephemeral=False)
        user_id = self.bot.igclient.user_id_from_username(username)
        guild_id = interaction.guild_id
                
        self.bot.cur.execute(f"""SELECT "user", "channel"
                                       FROM "{guild_id}"
                                       WHERE "user" = '{user_id}'
                                       """)     
        output = self.bot.cur.fetchall()

        if len(output) == 0:
            self.bot.cur.execute(f"""INSERT INTO "{guild_id}" ("user", "channel")
                                 VALUES ('{user_id}', '{channel.id}')
                                 """)
            self.bot.conn.commit()
            self.bot.dblog.write(f'[{datetime.now.strftime("%d/%m/%Y %H:%M:%S")}]: ADDUSER: User {user_id} has been added to {guild_id} with channel set as {channel.id}.\n')
            await interaction.response.send_message(f"User {username} was not present in database but has been added.")
        else:
            self.bot.cur.execute(f"""UPDATE "{guild_id}"
                                 SET "channel" = '{channel.id}'
                                 WHERE "user" = '{user_id}'
                                 """)
            self.bot.conn.commit()
            self.bot.dblog.write(f'[{datetime.now.strftime("%d/%m/%Y %H:%M:%S")}]: ADDUSER: User {user_id} of guild {guild_id} channel set to {channel.id}.\n')
            await interaction.response.send_message(f"User {username}'s channel has been updated")
        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DStories(bot), guild=discord.Object(id=783054832465346591))