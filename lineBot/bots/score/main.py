from linebot.models.send_messages import TextSendMessage

from lineBot.views import line_bot_api, QUICKREPLY_MENU

import requests

import environ
env = environ.Env()
environ.Env.read_env()

def score_registerJob(event, thisUser):
  thisUser.job = event.message.text
  thisUser.save()
  return line_bot_api.reply_message(event.reply_token,TextSendMessage(
    text= "登記完成 !",
    quick_reply= QUICKREPLY_MENU,
  ))

def score_main(event, thisUser):
  thisUser.where = 'score'
  thisUser.status = 'wfi_testName'
  thisUser.save()

  return line_bot_api.reply_message(event.reply_token,TextSendMessage(
    text= "請輸入考試名稱 :"
  ))


def score_gi_main(event, thisUser):
  if thisUser.status == 'wfi_testName':

    thisUser.status = 'wfi_testScores'
    thisUser.memo = event.message.text
    thisUser.save()

    return line_bot_api.reply_message(event.reply_token,TextSendMessage(
      text= "請輸入成績 :"
    ))

  if thisUser.status == 'wfi_testScores':

    testName = thisUser.memo.split('%')

    thisUser.status = ''
    thisUser.where = ''
    thisUser.memo = ''
    thisUser.save()

    requests.post(
      env('GAS_ENTRY'),
      data = {
        'subj' : thisUser.job if len(testName)==1 else testName[1],
        'name' : testName[0],
        'scores' : string_to_scores_list(event.message.text)
      }
    )

    url = 'https://docs.google.com/spreadsheets/d/1OUR9r-VDK834KXHBubOWS1EqXB3Tre07q7HKXHxSYFE/edit?usp=sharing'

    return line_bot_api.reply_message(event.reply_token,TextSendMessage(
      text= f"成績已送出(表單需要一點時間更新)\n{url}",
      quick_reply= QUICKREPLY_MENU,
    ))

def string_to_scores_list(string):
  scoreTable = dict()

  for segment in string.split('\n'):
    number = int(segment[:2])
    score = ""
    score += segment[2:]

    scoreTable[number] = score

  outputList = list()
  for number in range(1, 43+1):
    outputList.append(str(scoreTable.get(number, "")))

  return outputList
