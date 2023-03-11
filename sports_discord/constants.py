from enum import Enum

DOC_NAME = 'IPL 16 Auction'
BIDDING_SHEET_NAME = 'Bidding Page'
POINTS_SHEET_NAME = 'Points Worksheet'
TEAM_POINTS_SHEET_NAME = 'Team Points'
NOT_ON_A_TEAM = 'Not yet a part of any teams for this auction/draft. Please join a team first.'
NUMBER_OF_FIELDS = 3


class Pool(Enum):
    A = 1
    B = 2
    C = 3


class Position(Enum):
    GK = 1
    DF = 2
    MF = 3
    FW = 4


class SheetCols(Enum):
    POINTS_COL = 5
    OWNER_COL = 9
    ADJUSTED_POINTS_COL = 12
    UPGRADES_COL = 28
    ROLLED_TRANSFERS_COL = 14
