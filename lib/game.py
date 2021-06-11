import discord
from dataclasses import dataclass

from lib.player import Players


class Game:

    def __init__(self):
        self.players = Players()
        self.settings = Settings
        self.channels = Channels
        self.roles = Roles
        self.days = 1
        self.tasks = 0
        self.times = 0
        self.vote_target = None
        self.raid_target = None
        self.escort_target = None

    @property
    def role_table(self) -> str:
        msg = ''
        for p in self.players:
            msg += f'\n{p.role_name} {p.mention}'
        return msg

    def role_list(self, number: int) -> str:
        if number == 5:
            return '村村村占狼'
        if number == 6:
            return '村村村村占狼'
        if number == 7:
            return '村村占霊狩狼狼'
        if number == 8:
            return '村村村占霊狩狼狼'
        if number == 9:
            return '村村村占霊狩狂狼狼'

    def increase_task(self):
        self.tasks += 1

    def decrease_task(self):
        self.tasks -= 1

    def is_village_win(self) -> bool:
        for p in self.players.alives:
            if p.role == "狼":
                return False
        return True

    def is_werewolf_win(self) -> bool:
        village_count = 0
        werewolf_count = 0
        for p in self.players.alives:
            if p.role == "狼":
                werewolf_count += 1
            else:
                village_count += 1
        return village_count <= werewolf_count


@dataclass
class Settings:
    max_player: int = 9
    times: int = 120
    custom_role_list: str = None


@dataclass
class Channels:
    alive: discord.TextChannel = None
    dead: discord.TextChannel = None
    audience: discord.TextChannel = None
    wolfs: discord.TextChannel = None


@dataclass
class Roles:
    alive: discord.Role = None
    dead: discord.Role = None
