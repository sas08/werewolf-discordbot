from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

guild_ids = [840795339723767838, 810011469381894174]

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

    # カミングアウトコマンド
    @cog_ext.cog_slash(
        name='co',
        description='カミングアウトする',
        guild_ids=guild_ids,
        options=[
            create_option(
                name="role",
                description="カミングアウトする役職",
                option_type=3,
                required=True,
                choices=[
                    create_choice(
                        name="市民",
                        value="市民"
                    ),
                    create_choice(
                        name="占い",
                        value="占い"
                    ),
                    create_choice(
                        name="霊能",
                        value="霊能"
                    ),
                    create_choice(
                        name="狩人",
                        value="狩人"
                    ),
                    create_choice(
                        name="人狼",
                        value="人狼"
                    ),
                    create_choice(
                        name="狂人",
                        value="狂人"
                    ),
                ]
            )
        ]
    )
    async def _co(self, ctx: SlashContext, role):
        playersMention = self.bot.game.roles.alive
        await ctx.send(f"{playersMention}\n{ctx.author.name}が自分の役職を明かしました\n役職： __**{role}**__")

def setup(bot):
    bot.add_cog(Commands(bot))
