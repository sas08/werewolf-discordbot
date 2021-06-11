import discord
from discord.ext import commands
from string import ascii_uppercase

from lib.player import Player


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def debug(self, ctx):
        ids = [
            823890048088932383,
            805479870376968202,
            830778350929838100,
            735722422866542632,
            823857190849871872,
            836979174018514995,
            793214782349115432,
            809760929264828446,
            826152382139203634
        ]
        l = list(ascii_uppercase)
        for i in ids:
            member = ctx.guild.get_member(i)
            player = Player(member)
            player.symbol = l.pop(0)
            player.name = f'市民{player.symbol}'
            self.bot.game.players.append(player)


def setup(bot):
    bot.add_cog(Debug(bot))
