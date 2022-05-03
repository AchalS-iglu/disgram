import discord
from discord import app_commands
from discord.ext import commands

class DStories(commands.Cog, name="dstories"):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        
    @app_commands.command(name="test")
    async def my_top_command(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Test", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(DStories(bot), guild=discord.Object(id=783054832465346591))