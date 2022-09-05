from enum import Enum

DOC_NAME = 'Asia Cup 2022'
BIDDING_SHEET_NAME = 'Bidding Page'
POINTS_SHEET_NAME = 'Points Worksheet'
TEAM_POINTS_SHEET_NAME = 'Team Points'
NOT_ON_A_TEAM = 'Not yet a part of any teams for this auction/draft. Please join a team first.'


class SheetCols(Enum):
    OWNER_COL = 9
    POINTS_COL = 4
    ADJUSTED_POINTS_COL = 22
