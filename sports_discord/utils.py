def get_role_id(roles):
    for role in roles:
        if role.name.startswith('team-'):
            role_id = str(role.id)
            return role_id


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
