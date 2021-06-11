import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

# guild_ids = [840795339723767838, 810011469381894174]
guild_ids = [720566804094648330]


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 延長コマンド
    @cog_ext.cog_slash(
        name='long',
        description='会議時間を60秒延長します',
        guild_ids=guild_ids,
    )
    async def _long(self, ctx: SlashContext):
        self.bot.game.times += 60
        await ctx.send(f'{ctx.author.mention} 会議時間を60秒延長しました')

    # 時短コマンド
    @cog_ext.cog_slash(
        name='short',
        description='会議時間を60秒短縮します',
        guild_ids=guild_ids,
    )
    async def _short(self, ctx: SlashContext):
        self.bot.game.times -= 60
        await ctx.send(f'{ctx.author.mention} 会議時間を60秒短縮しました')

    # 残り時間を見るコマンド
    @cog_ext.cog_slash(
        name='time',
        description='残り時間を表示',
        guild_ids=guild_ids,
    )
    async def _time(self, ctx: SlashContext):
        await ctx.send(f"残り時間は、{self.bot.game.times} 秒です")

def setup(bot):
    bot.add_cog(Commands(bot))
