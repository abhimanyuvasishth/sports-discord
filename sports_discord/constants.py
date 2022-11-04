from enum import Enum

DOC_NAME = 'World Cup 2022'
BIDDING_SHEET_NAME = 'Bidding Page'
POINTS_SHEET_NAME = 'Points Worksheet'
TEAM_POINTS_SHEET_NAME = 'Team Points'
NOT_ON_A_TEAM = 'Not yet a part of any teams for this auction/draft. Please join a team first.'
NUMBER_OF_FIELDS = 15


class Pool(Enum):
    A = 1
    B = 2
    C = 3


class SheetCols(Enum):
    OWNER_COL = 9
    POINTS_COL = 4
    ADJUSTED_POINTS_COL = 22
    UPGRADES_COL = 28
    ROLLED_TRANSFERS_COL = 29
