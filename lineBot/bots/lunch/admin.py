from linebot.models.actions import CameraAction, CameraRollAction, PostbackAction
from linebot.models.send_messages import QuickReply, QuickReplyButton, TextSendMessage
from lineBot.views import line_bot_api

from lineBot.models import LunchMenu

from .. import tool

import environ
env = environ.Env()
environ.Env.read_env()

import pyimgur
import threading
import datetime
today = datetime.datetime.now().date


def update_menu(event, thisUser):
  thisUser.status = 'wfi_update_menu'
  thisUser.save()

  return line_bot_api.reply_message(event.reply_token,TextSendMessage(
    text= "請選擇上傳方式 :",
    quick_reply= QuickReply(items = [
      QuickReplyButton(
        action= CameraAction(label="拍照上傳")
      ),
      QuickReplyButton(
        action= CameraRollAction(label="從相簿選擇")
      ),
      QuickReplyButton(
        action= PostbackAction(label="返回", data="_home")
      ),
    ])
  ))

def update_menu_getImage(event, thisUser):
  image = line_bot_api.get_message_content(event.message.id)

  path = rf"lineBot\bots\lunch\{str(today())}.jpg"

  with open(path, 'wb') as f:
    for chunk in image.iter_content():
      f.write(chunk)

  thread = threading.Thread(target=upload_image, args=(path,))
  thread.start()

  thisUser.status = 'wft_update_price'
  thisUser.save()

  return line_bot_api.reply_message(event.reply_token,TextSendMessage(
    text= "請輸入價格(以空格分隔)"
  ))


def upload_image(path):

  im = pyimgur.Imgur(env('imgurAPI_KEY'))
  uploaded_image = im.upload_image(path, title=str(today()))

  url = uploaded_image.link

  newMenu = LunchMenu(
    photo_url=url,
    date=str(today())
  )
  newMenu.save()

def update_price(event, thisUser):

  test = event.message.text.split()
  if len(test) != 8:
    return line_bot_api.reply_message(event.reply_token,TextSendMessage(
      text= "請重新輸入價格(數量錯誤)"
    ))

  thisMenu = LunchMenu.objects.get(date=str(today()))
  thisMenu.prices = event.message.text
  thisMenu.save()

  return tool.home(event, thisUser, '菜單更新完成 !')
