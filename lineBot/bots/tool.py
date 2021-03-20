from linebot.models.send_messages import QuickReply, QuickReplyButton, TextSendMessage
from linebot.models.actions import PostbackAction

from lineBot.views import line_bot_api, QUICKREPLY_MENU

import requests

def help(event, thisUser):
  return line_bot_api.reply_message(event.reply_token,TextSendMessage(
    text= """bike : 取得校門口Ubike資訊""",
    quick_reply= QUICKREPLY_MENU(event, thisUser)
  ))


def home(event, thisUser, text=None):
  thisUser.where = ""
  thisUser.status = ""
  thisUser.save()

  if text is None:
    return line_bot_api.reply_message(event.reply_token,TextSendMessage(
      text= f"hello, {thisUser.name}.",
      quick_reply= QUICKREPLY_MENU(event, thisUser)
    ))

  return line_bot_api.reply_message(event.reply_token,TextSendMessage(
    text= text,
    quick_reply= QUICKREPLY_MENU(event, thisUser)
  ))



def bike(event, thisUser):
  url = 'https://data.tycg.gov.tw/api/v1/rest/datastore/a1b4714b-3b75-4ff8-a8f2-cc377e4eaa0f?format=json'

  resp = requests.get(url)
  data = resp.json()['result']['records'][1]
  update = data['mday'][8:]

  result = f"""車子數量 : {data['sbi']}
空位 : {data['bemp']}
最後更新時間 : {update[:2]}:{update[2:4]}:{update[4:]}"""

  if event.source.type == 'group':
    return line_bot_api.reply_message(event.reply_token,TextSendMessage(
      text= result
    ))

  return line_bot_api.reply_message(event.reply_token,TextSendMessage(
    text= result,
    quick_reply=QUICKREPLY_MENU(event, thisUser)
  ))
