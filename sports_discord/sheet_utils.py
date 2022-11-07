from sports_discord.constants import (BIDDING_SHEET_NAME, DOC_NAME,
                                      POINTS_SHEET_NAME,
                                      TEAM_POINTS_SHEET_NAME, NUMBER_OF_FIELDS, SheetCols)
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
    sheet.update_cell(player_row, SheetCols.OWNER_COL.value, team_name)


def get_points(player_name):
    sheet = get_sheet(DOC_NAME, POINTS_SHEET_NAME)
    player_row = sheet.find(player_name).row
    return int(sheet.cell(player_row, SheetCols.POINTS_COL.value).value or 0)


def get_points_for_match_num(player_name, match_num):
    sheet = get_sheet(DOC_NAME, POINTS_SHEET_NAME)
    player_row = sheet.find(player_name).row
    col = SheetCols.POINTS_COL.value + NUMBER_OF_FIELDS * match_num
    return int(sheet.cell(player_row, col).value or 0)


def get_rank(query_points):
    all_points = []
    for player_row in get_player_rows():
        name, _, _, points = player_row
        if name:
            all_points.append(int(points))
    rank = sorted(all_points, reverse=True).index(query_points) + 1
    total = len(all_points)
    return rank, total


def get_player_rows():
    sheet = get_sheet(DOC_NAME, POINTS_SHEET_NAME)
    return sheet.get('A3:D300')


def get_sorted_players(num_players=10, reverse=False):
    filtered_player_rows = []
    for player_row in get_player_rows():
        if player_row[0]:
            filtered_player_rows.append(player_row)

    return sorted(filtered_player_rows, key=lambda x: int(x[3]), reverse=reverse)[:num_players]


def adjust_transfer_points(team_name, adjusted_points):
    sheet = get_sheet(DOC_NAME, TEAM_POINTS_SHEET_NAME)
    team_row = sheet.find(team_name).row
    adjusted_points_col = SheetCols.ADJUSTED_POINTS_COL.value
    existing_adjusted_points = int(sheet.cell(team_row, adjusted_points_col).value or 0)
    new_adjusted_points = existing_adjusted_points + adjusted_points
    sheet.update_cell(team_row, adjusted_points_col, new_adjusted_points)
