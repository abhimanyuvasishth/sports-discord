from enum import Enum

DOC_NAME = 'Champions Trophy 2025 Auction'
BIDDING_SHEET_NAME = 'Bidding Page'
POINTS_SHEET_NAME = 'Points Worksheet'
TEAM_POINTS_SHEET_NAME = 'Team Points'
NOT_ON_A_TEAM = 'Not yet a part of any teams for this auction/draft. Please join a team first.'
NUMBER_OF_FIELDS = 15
CHANNEL_ID = 1340022095957983313


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
    NAME_COL = 0
    POINTS_COL = 5
    RAW_POINTS_COL = 261
    POINTS_OWNER_COL = 3
    BIDDING_OWNER_COL = 9
    ADJUSTED_POINTS_COL = 22
    UPGRADES_COL = 28
    ROLLED_TRANSFERS_COL = 29
