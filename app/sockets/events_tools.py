import json

general_matches = []

colors = ["EB5757","F2994A","F2C94C","219653","65C3C9","2F80ED"]

def reset_data():
    general_matches.clear()

def set_colors(match_id):
    for general_match in general_matches:
        if(general_match['match_data']['id'] == match_id):
            for color in colors:
                has_color = False

                for match_user in general_match["match_users_data"]:
                    if (match_user['color'] == color):
                        has_color = True
                        break
                if(has_color == False):
                    for match_user in general_match["match_users_data"]:
                        print("user color = " + match_user['color'])
                        if(match_user['color'] == "-"):       
                            match_user['color'] = color
            return general_match

def populate_general_match(data):
    temp_general_match = None
    for general_match in general_matches:
        if(data['match_data']['id'] == general_match['match_data']['id']):
            temp_general_match = general_match
            for data_match_user in data['match_users_data']:
                has_key = False
                for match_user in temp_general_match['match_users_data']:
                    if(match_user['id'] == data_match_user['id']):
                        has_key = True
                        break
                if(has_key == False): temp_general_match['match_users_data'].append(data_match_user)
            temp_general_match['users_data'].append(data['user_data'])
            general_match = temp_general_match
            general_match['match_data']['status'] = "finding_users"
            return temp_general_match
    if(temp_general_match == None):
        temp_general_match = {}
        temp_general_match['match_data'] = data['match_data']
        temp_general_match['users_data'] = []
        temp_general_match['users_data'].append(data['user_data'])
        temp_general_match['match_users_data'] = data['match_users_data']
        general_matches.append(temp_general_match)
        return temp_general_match
    
def user_ready(form):
    data = {}
    for general_match in general_matches:
        if(general_match['match_data']['id'] == form['data']['match_data']['id']):
            starting_game = True
            for match_user_data in general_match['match_users_data']:
                if(match_user_data['id'] == form['data']['match_user_data']['id']):
                    match_user_data['ready'] = form['data']['match_user_data']['ready']
                    data['match_user_data'] = match_user_data
                if(match_user_data['ready'] == False):
                    starting_game = False
            if(starting_game and len(general_match['match_users_data']) > 2):
                general_match['match_data']['status'] = "starting_game"
            else:
                general_match['match_data']['status'] = "finding_users"

            data['match_data'] = general_match['match_data']
            break
    return data
            
def add_character_selection(form):
    print("character selected")
    data = {} 
    return data        


def user_joined(form):
    data = populate_general_match(form)
    return set_colors(data['match_data']['id'])