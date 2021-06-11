import discord


class Player:

    def __init__(self, member: discord.Member):
        self.id = member.id
        self.mention = member.mention
        self.nick = member.nick
        self.name = None
        self.symbol = None
        self.role = '乱'
        self.channel = None
        self.is_dead = False
        self.voted = 0

    @property
    def color(self) -> str:
        if self.role in '村占霊狩狂':
            return '白'
        if self.role in '狼':
            return '黒'

    @property
    def side(self) -> str:
        if self.role in '村占霊狩':
            return '市民陣営'
        if self.role in '狂狼':
            return '人狼陣営'

    @property
    def status(self) -> str:
        if self.is_dead:
            return '死亡者'
        else:
            return '生存者'

    @property
    def role_name(self) -> str:
        if self.role == '村':
            return '市民'
        if self.role == '占':
            return '占い'
        if self.role == '霊':
            return '霊能'
        if self.role == '狩':
            return '狩人'
        if self.role == '狼':
            return '人狼'
        if self.role == '狂':
            return '狂人'

    def die(self):
        self.is_dead = True


class Players(list):

    @property
    def alives(self):
        return Players(p for p in self if not p.is_dead)

    def get(self, player_id) -> Player:
        for p in self:
            if p.id == player_id:
                return p
