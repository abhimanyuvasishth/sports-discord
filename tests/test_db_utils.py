from sports_discord import db_utils


def test_get_player_in():
    assert db_utils.get_player_in('Inaki Williams')
    assert not db_utils.get_player_in('Lionel Messi')


def test_get_player_owner():
    assert db_utils.get_player_owner('Lionel Messi')
    assert not db_utils.get_player_owner('asdfghjkl')


def test_user_team():
    assert db_utils.get_user_team_by_name('a')


def test_squad():
    assert db_utils.get_squad(1)
