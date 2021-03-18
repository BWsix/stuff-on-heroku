from linebot.models.actions import PostbackAction
from linebot.models.send_messages import QuickReply, QuickReplyButton, TextSendMessage

import datetime

from . import lunch
from lineBot.views import line_bot_api
from lineBot.models import LunchOrder, LunchMenu

today = datetime.datetime.now().date

def normal_create_order(event, thisUser):

  menu = LunchMenu.objects.filter(date=str(today())).first()

  if menu is None:

    return line_bot_api.reply_message(event.reply_token,TextSendMessage(
      text= "今日菜單尚未更新",
      quick_reply= QuickReply(items = [
        QuickReplyButton(
          action= PostbackAction(label="一般類", data="_lunch_normal")
        ),
        QuickReplyButton(
          action= PostbackAction(label="返回", data="_home")
        )
      ])
    ))


