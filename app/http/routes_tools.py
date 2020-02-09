def check_json(json_data, json_keys):
    try:
        for key in json_keys:
            if(key not in json_data): return False
            else: 
                if(json_data[key] == ""): return False
        return True
    except:
        return False
def check_db_callback(callbackDict, sucess_feedback, error_feedback):
    status_code = 0
    if(callbackDict['query_successful'] == True and callbackDict['data'] != None):
        status_code = 200
        callbackDict['feedback'] = sucess_feedback
    elif(callbackDict['query_successful'] == True and callbackDict['data'] == None):
        status_code = 204
        callbackDict['feedback'] = error_feedback
    else:
        status_code = 200
        callbackDict['feedback'] = error_feedback
    return [status_code, callbackDict]