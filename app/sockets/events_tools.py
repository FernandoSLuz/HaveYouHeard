import json

matches = []
users = []
match_users = []


def populate_match(new_match):
    for match in matches:
        if(match['id'] == new_match['id']):
            return
    matches.append(new_match)

def populate_match_users(new_match_users):
    temp_match_users = match_users
    for new_match_user in new_match_users:
        has_key = False
        for match_user in match_users:
            if(match_user['id'] == new_match_user['id']):
                has_key = True
                break
        if(has_key == False): temp_match_users.append(new_match_user)

def user_joined(form):
    populate_match(form['match_data'])
    users.append(form['user_data'])
    populate_match_users(form['match_users_data'])

def get_match_info(match_id):
    data = {}
    temp_match_users = []
    temp_users = []
    for match in matches:
        if(match['id'] == match_id): data['match_data'] = match
        break
    for match_user in match_users:
        if(match_user['id_match'] == match_id):
            temp_match_users.append(match_user)
            break
    data['match_users_data'] = temp_match_users
    for user in users:
        for match_user in temp_match_users:
            if(user['id'] == match_user['id_user']):
                temp_users.append(user)
                break
    data['users_data'] = temp_users
    return data