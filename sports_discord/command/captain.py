from dataclasses import dataclass

from sports_discord.command.command import Command


@dataclass
class Captain(Command):
    @property
    def prefix():
        return '?kaptaan'

    def execute():
        pass
