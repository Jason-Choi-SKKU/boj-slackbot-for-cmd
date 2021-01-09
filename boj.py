import json
import requests
from bs4 import BeautifulSoup
import formattedDate as FormattedDate


class UserData:
    def __init__(self, userID):
        self.userID = userID
        self.userPageAddr = "https://www.acmicpc.net/user/%s" % userID
        self.userPageRequests = requests.get(self.userPageAddr)
        self.userPageHTML = self.userPageRequests.text
        self.userPageSoup = BeautifulSoup(self.userPageHTML, 'html.parser')

    def solvedProblemList(self):
        problemDummy = self.userPageSoup.find(class_="panel-body")
        problems = []
        for tag in problemDummy:
            strTag = str(tag)
            if 'href="/problem' in strTag:
                problems.append(tag.text)
        return problems

    def calcExp(self):
        solvedACAPIURL = "https://api.solved.ac/v2/problems/calculate.json"
        solvedProblem = self.solvedProblemList()
        solvedProblemToString = str(solvedProblem).replace("['", " ").replace("', '", " ").replace("']", " ")
        queryJSON = {"query" : solvedProblemToString}
        responseFromSolvedAc = requests.post(solvedACAPIURL,data=json.dumps(queryJSON)).json()
        return responseFromSolvedAc["result"]["exp"]

    def selectTodaySolvedProblem(self):
        with open("./venv/data/cmdData.json", "r", encoding='UTF8') as json_file:
            cmdData = json.load(json_file)

        return list(
            set(cmdData[self.userID]['bojDataByDate'][FormattedDate.today]["solvedProblem"]) -
            set(cmdData[self.userID]['bojDataByDate'][FormattedDate.yesterday]["solvedProblem"])
        )

    def calcTodayEarnExp(self):
        with open("./venv/data/cmdData.json", "r", encoding='UTF8') as json_file:
            cmdData = json.load(json_file)
        return cmdData[self.userID]['bojDataByDate'][FormattedDate.today]["exp"]-cmdData[self.userID]['bojDataByDate'][FormattedDate.yesterday]["exp"]


def refreshDB():
    with open("./venv/data/cmdData.json", "r", encoding='UTF8') as json_file:
        cmdData = json.load(json_file)

    for userID in cmdData.keys():
        userData = UserData(userID)
        tmpBojDataByDate = {"exp":userData.calcExp(), "solvedProblem" : userData.solvedProblemList()}
        cmdData[userID]['bojDataByDate'][FormattedDate.today] = tmpBojDataByDate

    with open("./venv/data/cmdData.json", "w", encoding='UTF8') as json_file:
        json.dump(cmdData, json_file, ensure_ascii=False, indent=4, sort_keys=True)



