from sports_discord.google_sheet import get_sheet


def update_captain(player_name, match_number, flag=True):
    sheet = get_sheet('Asia Cup 2022', 'Points Worksheet')
    kaptaan_col = sheet.findall('Kaptaan')[match_number - 1].col
    player_row = sheet.find(player_name).row
    sheet.update_cell(player_row, kaptaan_col, flag * 1)
