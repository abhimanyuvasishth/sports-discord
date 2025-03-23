import emoji
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from sports_discord.constants import Pool
from sports_discord.database import Base


class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    nickname = Column(String, nullable=True)
    creation_timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    pool = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)
    team_id = Column(Integer, ForeignKey('team.id'))
    team = relationship('Team')
    tournament_id = Column(Integer, ForeignKey('tournament.id'))
    tournament = relationship('Tournament')
    user_team_id = Column(Integer, ForeignKey('user_team.id'))
    user_team = relationship('UserTeam')

    def __str__(self):
        if self.nickname:
            name_parts = self.name.split(" ", 1)
            if len(name_parts) == 2:
                first, last = name_parts
                full_name = f'{first} "{self.nickname}" {last}'
            else:
                full_name = f'{self.name} "{self.nickname}"'
        else:
            full_name = self.name

        return emoji.emojize(f'{full_name} ({Pool(self.pool).name})', language='alias')
