from sports_discord import sheet_utils
from sports_discord.constants import (BIDDING_SHEET_NAME, DOC_NAME,
                                      POINTS_SHEET_NAME,
                                      TEAM_POINTS_SHEET_NAME)
from sports_discord.google_sheet import get_sheet


def test_sheets():
    assert get_sheet(DOC_NAME, BIDDING_SHEET_NAME)
    assert get_sheet(DOC_NAME, POINTS_SHEET_NAME)
    assert get_sheet(DOC_NAME, TEAM_POINTS_SHEET_NAME)


def test_team_points():
    assert len(sheet_utils.get_team_points()) > 1
