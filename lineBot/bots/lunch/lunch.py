from linebot.models.actions import PostbackAction
from linebot.models.send_messages import QuickReply, QuickReplyButton, TextSendMessage
from lineBot.views import line_bot_api

def lunch_main(event, thisUser):
  thisUser.where = 'lunch'
  thisUser.save()

  return line_bot_api.reply_message(event.reply_token,TextSendMessage(
    text= "訂餐選單",
    quick_reply= QuickReply(items = [
      QuickReplyButton(
        action= PostbackAction(label="一般類", data="lunch_normal")
      ),
      QuickReplyButton(
        action= PostbackAction(label="返回", data="home")
      )
    ])
  ))
