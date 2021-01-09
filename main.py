import json
import boj as BOJ
import schedule
import time
import formattedDate as FormattedDate
from slacker import Slacker

with open("./venv/data/slackData.json", "r", encoding='UTF8') as json_file:
    slackData = json.load(json_file)
slackToken = slackData["slackToken"]
channelName = slackData["channelName"]
slackBot = Slacker(slackToken)

def dailyNotice():
    BOJ.refreshDB()
    dailyMessage = "\n\n:tada:  *%s CMD 백준 챌린지 결과*  :tada:\n\n\n\n"%FormattedDate.today
    with open("./venv/data/cmdData.json", "r", encoding='UTF8') as json_file:
        cmdData = json.load(json_file)

    for userID in cmdData.keys():
        userData = BOJ.UserData(userID)
        todaySolvedProblem = userData.selectTodaySolvedProblem()
        if todaySolvedProblem is not []:
            dailyMessage += ">%s\n 오늘 푼 문제 : %s\n획득한 경험치 : %d\n\n"%(cmdData[userID]["name"],todaySolvedProblem,userData.calcTodayEarnExp())
    slackBot.chat.post_message(channelName, dailyMessage, as_user=True)



schedule.every().day.at("11:59").do(dailyNotice)

while True:
    schedule.run_pending()
    time.sleep(10)
