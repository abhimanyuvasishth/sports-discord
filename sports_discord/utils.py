def get_role_id(roles):
    for role in roles:
        if role.name.startswith('team-'):
            role_id = str(role.id)
            return role_id
