from linebot.models.send_messages import QuickReply, QuickReplyButton, TextSendMessage
from linebot.models.actions import PostbackAction

from lineBot.views import line_bot_api, QUICKREPLY_MENU

def register(event, thisUser):
  try:
    number, name = event.message.text.split()
    number = int(number)

    thisUser.number = number
    thisUser.name = name

  except:
    return line_bot_api.reply_message(event.reply_token,TextSendMessage(
      text= "出現問題, 請重新輸入 :"
    ))

  thisUser.status = ""
  thisUser.where = ""
  thisUser.save()

  return line_bot_api.reply_message(event.reply_token,TextSendMessage(
    text= "已建檔完成 !",
    quick_reply= QUICKREPLY_MENU(event, thisUser),
  ))
