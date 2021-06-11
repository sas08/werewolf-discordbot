from discord import Embed, Colour, PermissionOverwrite
from discord.ext import commands
from asyncio import sleep
from random import choice

from ui.fortune import Fortune
from ui.escort import Escort
from ui.raid import Raid
from ui.vote import Vote

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gamestart(self, ctx):

        # 環境変数の準備
        guild = ctx.guild
        category = ctx.channel.category
        everyone = guild.default_role

        game = self.bot.game
        players = game.players
        channels = game.channels
        roles = game.roles

        # ゲームチャンネル作成
        channels.alive = await category.create_text_channel(name='生存者')
        channels.dead = await category.create_text_channel(name='死亡者')
        channels.audience = await category.create_text_channel(name='観戦者')
        channels.wolfs = await category.create_text_channel(name='人狼部屋')

        roles.alive = await guild.create_role(name='生存者', colour=Colour.blue())
        roles.dead = await guild.create_role(name='死亡者', colour=Colour.red())

        # 生存者用チャンネル 権限設定
        await channels.alive.set_permissions(everyone, send_messages=False)
        await channels.alive.send(f'{roles.alive.mention}\nここは生存者が集まって討論する場所です\nこのチャンネルは全員が見ることができますが、生存者しか書き込むことはできません')

        # 志望者用チャンネル 権限設定
        await channels.dead.set_permissions(roles.alive, read_messages=False)
        await channels.dead.set_permissions(everyone, send_messages=False)
        await channels.dead.set_permissions(roles.dead, send_messages=True)
        await channels.dead.send('ここは死亡者が集まって雑談する場所です\nこのチャンネルは死亡者・観戦者が見ることができますが、死亡者しか書き込むことはできません')

        # 観戦者用チャンネル 権限設定
        await channels.audience.set_permissions(roles.alive, read_messages=False)
        await channels.audience.send('ここは観戦者が集まって雑談する場所です\nこのチャンネルは死亡者・観戦者が見る・書き込むことができます')

        # 人狼会議所 権限設定
        await channels.wolfs.set_permissions(everyone, read_messages=False)
        # await channels.wolfs.send('ここは人狼が集まって会議する場所です\nこのチャンネルは人狼にしか見えません')

        wolf = ""
        for player in players:
            member = guild.get_member(player.id)
            await member.edit(nick=f'{player.name}｜{player.status}')
            await member.add_roles(roles.alive)
            player.channel = await category.create_text_channel(
                name=f'{player.side}｜{player.role_name}',
                overwrites={
                    everyone: PermissionOverwrite(read_messages=False),
                    member: PermissionOverwrite(read_messages=True)
                }
            )
            # 役職伝達
            await player.channel.send(f'{player.mention} {player.side}｜{player.role_name}\nこのチャンネルはあなたにしか見えません')
            if player.role == '狼':
                wolf += f"{player.mention} "
                await channels.wolfs.set_permissions(member, overwrite=PermissionOverwrite(read_messages=True))

        await channels.wolfs.send(f"{wolf}\nここは人狼が集まって会議する場所です\nこのチャンネルは人狼にしか見えません")
        wolfTime = 60
        await channels.wolfs.send(f"ゲーム開始前の会議の時間を開始します。\n制限時間は、{wolfTime}秒です")

        # 人狼会議時間
        while wolfTime > 0:
            wolfTime -= 1
            await sleep(0.9)

        # 人狼ゲーム | メイン部分
        while True:
            # 夜開始
            embed = Embed(
                description=f'{game.days}日目夜｜{roles.alive.mention} {len(players.alives)}人',
                colour=Colour.blue()
            )
            await channels.alive.send(embed=embed)
            await channels.alive.send('個人のチャンネルに移動してください')
            await channels.alive.set_permissions(roles.alive, send_messages=False)

            # 夜の行動
            for player in players.alives:
                # 占い乱白
                if game.days == 1:
                    if player.role == '占':
                        p = choice([p for p in players if p.color == '白' and p != player])
                        await player.channel.send(f'{p.mention} は {p.color} でした')
                # 占い・霊能・狩人の行動
                if game.days != 1:
                    if player.role == '占':
                        await Fortune(self.bot).start(player.channel)
                    if player.role == '霊':
                        await player.channel.send(f'{game.vote_target.mention} は {game.vote_target.color} でした')
                    if player.role == '狩':
                        await Escort(self.bot).start(player.channel)
            # 人狼の行動
            if game.days != 1:
                await Raid(self.bot).start(channels.wolfs)

            # 全タスクが終了するまで待つ
            while game.tasks > 0:
                await sleep(1)

            # 人狼の行動を処理
            if game.raid_target != game.escort_target:
                player = game.raid_target
                player.die()
                embed = Embed(
                    description=f'{player.mention} が殺害されました',
                    colour=Colour.red()
                )
                await channels.alive.send(embed=embed)
                member = guild.get_member(player.id)
                await member.edit(nick=f'{player.name}｜{player.status}')
                await member.remove_roles(roles.alive)
                await member.add_roles(roles.dead)
            else:
                embed = Embed(
                    description='誰も殺害されませんでした',
                    colour=Colour.green()
                )
                await channels.alive.send(embed=embed)

            # 人狼が勝利してるか確認
            if game.is_werewolf_win():
                await channels.alive.send('ゲーム終了｜人狼陣営の勝利です')
                await ctx.channel.send(game.role_table)
                break

            # 朝の行動開始
            embed = Embed(
                description=f'{game.days}日目朝｜{roles.alive.mention} {len(players.alives)}人',
                colour=Colour.blue()
            )
            await channels.alive.send(embed=embed)
            await channels.alive.send('処刑する人を話し合ってください')
            await channels.alive.set_permissions(roles.alive, send_messages=True)

            # ゲーム時間制限の処理 | 600秒
            game.times = 600
            while game.times > 0:
                game.times -= 1
                # 60秒ごとに通知する
                if game.times % 60 == 0:
                    await channels.alive.send(f'会議時間残り{game.times}秒です')
                await sleep(0.9)

            # 投票フェーズ
            embed = Embed(
                description=f'{game.days}日目夕｜{roles.alive.mention} {len(players.alives)}人',
                colour=Colour.blue()
            )
            await channels.alive.send(embed=embed)
            await channels.alive.send('個人チャンネルで投票をしてください')

            # それぞれの役職チャンネルに投票箱を設置
            for player in players.alives:
                await Vote(self.bot).start(player.channel)

            # 全員投票し終わるまで待つ
            while game.tasks > 0:
                await sleep(1)

            # 処刑判定
            maximum = max([p.voted for p in players.alives])
            for player in players.alives:
                if player.voted == maximum:
                    player.die()
                    member = guild.get_member(player.id)
                    if player.role == '狼':
                        await channels.wolfs.set_permissions(
                            member,
                            overwrite=PermissionOverwrite(read_messages=False)
                        )
                    embed = Embed(
                        description=f'{player.mention} が処刑されました',
                        colour=Colour.red()
                    )
                    await channels.alive.send(embed=embed)
                    await member.edit(nick=f'{player.name}｜{player.status}')
                    await member.remove_roles(roles.alive)
                    await member.add_roles(roles.dead)
                    game.vote_target = player
                    break

            for player in players.alives:
                player.voted = 0

            # 勝敗判定
            if game.is_werewolf_win():
                await channels.alive.send('ゲーム終了｜人狼陣営の勝利です')
                await ctx.channel.send(game.role_list)
                break
            if game.is_village_win():
                await channels.alive.send('ゲーム終了｜市民陣営の勝利です')
                await ctx.channel.send(game.role_list)
                break

            game.days += 1

def setup(bot):
    bot.add_cog(Main(bot))

