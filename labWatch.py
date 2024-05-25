import datetime
import os
import requests
import json

userDataPath = f"{os.path.expanduser('~')}/.local/labWatch"
userData = '/data.json'
baseURL = "/api/v4/projects/"

def initialize():
    os.makedirs(f"{userDataPath}", exist_ok=True)
    if not os.path.isfile(f"{userDataPath}{userData}"):
        init = getInfo()
        init['lastCheck'] = datetime.datetime.now().isoformat()
        with open(userDataPath+userData, "w") as file:
            json.dump(init, file)

def getInfo():
    namespace = input("Please input your GitLab namespace: Enter for default 'gitlab.wethinkco.de' ")
    if namespace == '':
        namespace = 'gitlab.wethinkco.de'
    token = input("Please enter your personal access token: ")
    strProjects = input("Please enter the project ID's you would like to track as a comma seperated list: ")
    projects = strProjects.split(",")
    return {'namespace': namespace, 'token': token, "projects": projects}

if __name__ == '__main__':
    initialize()