import datetime
import os
import json
import requests
import subprocess



userDataPath = f"{os.path.expanduser('~')}/.local/labWatch"
userDataFile = '/data.json'
baseURL = "/api/v4/projects"
userData = {}


def initialize():
    os.makedirs(f"{userDataPath}", exist_ok=True)
    if not os.path.isfile(userDataPath+userDataFile):
        init = getInfo()
        init['lastCheck'] = getFormattedTimeNow()
        with open(userDataPath+userDataFile, "w") as file:
            json.dump(init, file)


def getInfo():
    namespace = input("Please input your GitLab namespace: Enter for default 'gitlab.wethinkco.de' ")
    if namespace == '':
        namespace = 'gitlab.wethinkco.de'
    token = input("Please enter your personal access token: ")
    strProjects = input("Please enter the project ID's you would like to track as a comma seperated list: ")
    projects = strProjects.split(",")
    return {'namespace': namespace, 'token': token, "projects": projects}


def checkNewRequests():
    message = ""
    updatedProjects = 0
    for project in userData["projects"]:
        response = requests.get(f"https://{userData["namespace"]}{baseURL}/{project}/repository/commits?since={userData["lastCheck"]}&all=true",
                                 headers={"PRIVATE-TOKEN": f"{userData["token"]}"})
        if len(response.json()) > 0:
            updatedProjects += 1
            message += formatCommitMessage(response.json(), project)
    userData["lastCheck"] = getFormattedTimeNow()
    updateUserData()
    subprocess.call(['notify-send', 'labWatch', message])



def formatCommitMessage(jsonResponse, projectId):
    nameResponse = requests.get(f"https://{userData["namespace"]}{baseURL}/{projectId}", 
                                headers={"PRIVATE-TOKEN": f"{userData["token"]}"})
    name = nameResponse.json()["name"]
    if len(jsonResponse) == 1:
        return f"{jsonResponse[0]["committer_name"]} pushed a commit to {name}."
    else:
        return f"Multiple commits to {name}."


def getUserData():
    global userData
    with open(userDataPath+userDataFile, 'r') as file:
        userData = json.load(file)


def updateUserData():
    global userData
    with open(userDataPath+userDataFile, "w") as file:
        json.dump(userData, file)


def getFormattedTimeNow():
    now = datetime.datetime.now(datetime.UTC)
    return now.isoformat()


if __name__ == '__main__':
    initialize()
    getUserData()
    checkNewRequests()