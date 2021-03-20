from linebot.models.actions import PostbackAction
from linebot.models.send_messages import QuickReply, QuickReplyButton, TextSendMessage

from lineBot.views import line_bot_api
from lineBot.bots import tool

from . import normal, admin

def main(event, thisUser, text=None):
  thisUser.where = 'lunch'
  thisUser.status = 'main_menu'
  thisUser.save()

  items = [
    QuickReplyButton(
      action= PostbackAction(label="一般類", data="_lunch_normal")
    ),
    QuickReplyButton(
      action= PostbackAction(label="返回", data="_home")
    )
  ]
  if thisUser.job == 'lunch_admin':
    items += [
      QuickReplyButton(
      action= PostbackAction(label="更新菜單", data="_update_menu")
    )]


  return line_bot_api.reply_message(event.reply_token,TextSendMessage(
    text= text if text else "訂餐選單",
    quick_reply= QuickReply(items=items)
  ))

textList = {
  'main_menu' : main,

  'wft_update_price' : admin.update_price,

  'wfi_normal_order_index' : normal.get_index,

}

def MSG_handler(event, thisUser):
  for text in textList:
    if thisUser.status == text:
      return textList[text](event, thisUser)


dataList = {
  '_update_menu' : admin.update_menu,
  '_lunch_normal' : normal.normal_make_order,

  '_home' : tool.home,
}

def PB_handler(event, thisUser):
  for data in dataList:
    if event.postback.data == data:
      return dataList[data](event, thisUser)
