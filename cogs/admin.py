import discord
from discord.ext import commands

from ui.invite import Invite
from ui.rolepanel import Rolepanel


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def max_player(self, ctx, number: int):
        self.bot.game.settings.max_player = number
        await ctx.send(f'ゲームの最大人数を {number} 人に設定しました')

    @commands.command()
    async def custom_role(self, ctx, role_list):
        self.bot.game.settings.custom_role_list = role_list
        await ctx.send(f'ゲームのカスタムロールリストを設定しました')

    @commands.command()
    async def invite(self, ctx):
        await Invite(self.bot, ctx.author.id).start(ctx.channel)

    @commands.command()
    async def rolepanel(self, ctx):
        await Rolepanel(self.bot, ctx.author.id).start(ctx.channel)

    @commands.command()
    async def end(self, ctx):
        items = [
            self.bot.game.channels.alive,
            self.bot.game.channels.dead,
            self.bot.game.channels.audience,
            self.bot.game.channels.wolfs,
            self.bot.game.roles.alive,
            self.bot.game.roles.dead
        ]
        for item in items:
            await item.delete()
        for player in self.bot.game.players:
            member = ctx.guild.get_member(player.id)
            await member.edit(nick=player.nick)
            await player.channel.delete()


def setup(bot):
    bot.add_cog(Admin(bot))
