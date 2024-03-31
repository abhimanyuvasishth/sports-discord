def get_role_id(roles):
    for role in roles:
        if role.name.startswith('team-'):
            role_id = str(role.id)
            return role_id


def get_emoji_from_number(number):
    words = 'zero one two three four five six seven eight nine'.split()
    emojis = []
    for letter in str(number):
        emojis.append(f':{words[int(letter)]}:')
    return ''.join(emojis)


def get_rating_emoji(rank, total):
    percentile = 1 - rank / total
    if percentile <= 0.25:
        return ':lemon:'
    elif 0.25 < percentile <= 0.5:
        return ':neutral_face:'
    elif 0.5 < percentile <= 0.75:
        return ':slight_smile:'
    elif 0.75 < percentile <= 0.9:
        return ':grinning:'
    else:
        return ':fire:'


def get_current_points_emoji(current_points):
    if current_points <= 0:
        return ':face_with_symbols_over_mouth:'
    elif 0 < current_points <= 50:
        return ':neutral_face:'
    elif 50 < current_points <= 100:
        return ':grinning:'
    else:
        return ':star_struck:'
