from sports_discord import db_utils


def test_get_player_in():
    assert db_utils.get_player_in('Kinchit Shah')
    assert not db_utils.get_player_in('Virat Kohli')
