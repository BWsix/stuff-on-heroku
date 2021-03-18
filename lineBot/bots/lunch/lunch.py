from linebot.models.actions import PostbackAction
from linebot.models.send_messages import QuickReply, QuickReplyButton, TextSendMessage

from lineBot.views import line_bot_api
from lineBot.bots import tool

from . import normal

def main(event, thisUser):
  thisUser.where = 'lunch'
  thisUser.status = 'main_menu'
  thisUser.save()

  return line_bot_api.reply_message(event.reply_token,TextSendMessage(
    text= "訂餐選單",
    quick_reply= QuickReply(items = [
      QuickReplyButton(
        action= PostbackAction(label="一般類", data="_lunch_normal")
      ),
      QuickReplyButton(
        action= PostbackAction(label="返回", data="_home")
      )
    ])
  ))

def MSG_handler(event, thisUser):
  if thisUser.status == 'main_menu':
    return main(event, thisUser)


dataList = {
  '_lunch_normal' : normal.normal_create_order,

  '_home' : tool.home,
}

def PB_handler(event, thisUser):
  for data in dataList:
    if event.postback.data == data:
      return dataList[data](event, thisUser)
