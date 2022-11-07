from sports_discord import utils


def test_get_emoji_from_number():
    assert utils.get_emoji_from_number(100) == ':one::zero::zero:'


def test_get_rating_emoji():
    assert utils.get_rating_emoji(1, 100) == ':fire:'
    assert utils.get_rating_emoji(23, 100) == ':grinning:'
    assert utils.get_rating_emoji(34, 100) == ':slight_smile:'
    assert utils.get_rating_emoji(59, 100) == ':neutral_face:'
    assert utils.get_rating_emoji(95, 100) == ':lemon:'
