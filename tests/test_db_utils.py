from sports_discord import db_utils


def test_get_player_in():
    assert db_utils.get_player_in('Mohammad Saleem')
    assert not db_utils.get_player_in('Jos Buttler')
