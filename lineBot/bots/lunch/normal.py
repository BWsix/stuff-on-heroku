from linebot.models.actions import PostbackAction
from linebot.models.send_messages import QuickReply, QuickReplyButton, TextSendMessage

import datetime

from . import lunch
from lineBot.views import line_bot_api
from lineBot.models import LunchOrder, LunchMenu
from lineBot.bots import tool

today = datetime.datetime.now().date

def normal_make_order(event, thisUser):

  menu = LunchMenu.objects.filter(date=str(today())).first()

  if menu is None:
    return lunch.main(event, thisUser, '今日菜單尚未更新 !')
  if not menu.avalible:
    return lunch.main(event, thisUser, '今日菜單已經送出 !')

  thisUser.status = 'wfi_normal_order_index'
  thisUser.save()

  return line_bot_api.reply_message(event.reply_token,TextSendMessage(
    text= "請輸入1~8"
  ))


def get_index(event, thisUser):
  index = event.message.text

  try:
    index = int(index)
    if not 1<= index <= 8:
      raise 'err'
  except Exception:
    return line_bot_api.reply_message(event.reply_token,TextSendMessage(
      text= "請重新輸入(輸入格式有問題 !)"
    ))

  print(LunchMenu.objects.get(date=str(today())).prices.split()[index-1])

  newOrder = LunchOrder(
    orderer = thisUser,
    date = str(today()),
    type = 'normal',
    order = index,
    price = int(LunchMenu.objects.get(date=str(today())).prices.split()[index-1])
  )
  newOrder.save()

  return tool.home(event, thisUser, '訂單已送出')
