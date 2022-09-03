from abc import ABC, abstractmethod
from typing import Optional

from discord.ext.commands import Context


class Command(ABC):
    context: Context
    args: Optional[tuple]

    @property
    def prefix() -> str:
        ...

    @abstractmethod
    def execute(self):
        ...
