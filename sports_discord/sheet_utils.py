from sports_discord.constants import (BIDDING_SHEET_NAME, DOC_NAME, POINTS_SHEET_NAME,
                                      TEAM_POINTS_SHEET_NAME)
from sports_discord.google_sheet import get_sheet


def update_captain(player_name, match_number, flag=True):
    sheet = get_sheet(DOC_NAME, POINTS_SHEET_NAME)
    kaptaan_col = sheet.findall('Kaptaan')[match_number - 1].col
    player_row = sheet.find(player_name).row
    sheet.update_cell(player_row, kaptaan_col, flag * 1)


def get_team_points():
    rank_order = []
    sheet = get_sheet(DOC_NAME, TEAM_POINTS_SHEET_NAME)
    values = sheet.get('A1:C10')
    for row in values[1:]:
        try:
            name, points, rank = row
        except ValueError:
            continue
        rank_order.append({
            'name': name,
            'points': int(points),
            'rank': int(rank),
        })
    return sorted(rank_order, key=lambda e: e['rank'])


def update_owner(player_name, team_name, index=0):
    sheet = get_sheet(DOC_NAME, BIDDING_SHEET_NAME)
    player_row = sheet.findall(player_name)[index].row
    owner_col = 9
    sheet.update_cell(player_row, owner_col, team_name)


def get_points(player_name):
    sheet = get_sheet(DOC_NAME, POINTS_SHEET_NAME)
    player_row = sheet.find(player_name).row
    points_col = 4
    return int(sheet.cell(player_row, points_col).value or 0)


def adjust_transfer_points(team_name, adjusted_points):
    sheet = get_sheet(DOC_NAME, TEAM_POINTS_SHEET_NAME)
    team_row = sheet.find(team_name).row
    adjusted_points_col = 22
    existing_adjusted_points = int(sheet.cell(team_row, adjusted_points_col).value or 0)
    new_adjusted_points = existing_adjusted_points + adjusted_points
    sheet.update_cell(team_row, adjusted_points_col, new_adjusted_points)
