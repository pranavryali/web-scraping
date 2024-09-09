import json

def convertListToJson(data, fileName):
    with open (fileName, 'w') as file:
        json.dump(data, file, indent=4)