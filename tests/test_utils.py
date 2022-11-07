from sports_discord import utils


def test_emoji_from_number():
    assert utils.get_emoji_from_number(100) == ':one::zero::zero:'
