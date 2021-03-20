from linebot.models.send_messages import TextSendMessage

from lineBot.views import line_bot_api, QUICKREPLY_MENU
from .gas import send_score_to_sheet

import threading

import environ
env = environ.Env()
environ.Env.read_env()

def registerJob(event, thisUser):
  thisUser.where = 'score'
  thisUser.status = 'wfi_job'
  thisUser.save()

  return line_bot_api.reply_message(event.reply_token,TextSendMessage(
    text= "請輸入科目 :"
  ))
def applyJob(event, thisUser):
  thisUser.where = ''
  thisUser.status = ''
  thisUser.job = event.message.text
  thisUser.save()

  return line_bot_api.reply_message(event.reply_token,TextSendMessage(
    text= "登記完成 !",
    quick_reply= QUICKREPLY_MENU(event, thisUser),
  ))


def main(event, thisUser):
  thisUser.where = 'score'
  thisUser.status = 'wfi_testName'
  thisUser.save()

  return line_bot_api.reply_message(event.reply_token,TextSendMessage(
    text= "請輸入考試名稱 :"
  ))


# def PB_handler(event, thisUser):
#   pass

def get_input_main(event, thisUser):
  if thisUser.status == 'wfi_testName':

    thisUser.status = 'wfi_testScores'
    thisUser.memo = event.message.text
    thisUser.save()

    return line_bot_api.reply_message(event.reply_token,TextSendMessage(
      text= "請輸入成績 :"
    ))

  if thisUser.status == 'wfi_testScores':

    thread = threading.Thread(target=send_score_to_sheet, args=(event, thisUser))
    thread.start()

    url = 'https://docs.google.com/spreadsheets/d/1OUR9r-VDK834KXHBubOWS1EqXB3Tre07q7HKXHxSYFE/edit?usp=sharing'

    return line_bot_api.reply_message(event.reply_token,TextSendMessage(
      text= f"成績已送出(表單需要一點時間更新)\n{url}",
      quick_reply= QUICKREPLY_MENU(event, thisUser),
    ))

  if thisUser.status == 'wfi_job':
    return applyJob(event, thisUser)

