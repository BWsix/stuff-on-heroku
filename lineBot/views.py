from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models.actions import PostbackAction
from linebot.models.events import FollowEvent, PostbackEvent, MessageEvent, TextMessage, UnfollowEvent
from linebot.models.send_messages import QuickReply, QuickReplyButton, TextSendMessage

import environ
env = environ.Env()
environ.Env.read_env()

line_bot_api = LineBotApi(env('channel_access_token'))
handler = WebhookHandler(env('channel_secret'))

@csrf_exempt
@require_POST
def webhook(request: HttpRequest):
  signature = request.headers["X-Line-Signature"]
  body = request.body.decode()

  try:
    handler.handle(body, signature)
  except InvalidSignatureError:
    messages = (
      "Invalid signature. Please check your channel access token/channel secret."
    )
    return HttpResponseBadRequest(messages)
  return HttpResponse("OK")

QUICKREPLY_MENU = QuickReply(items=[
  QuickReplyButton(
    action= PostbackAction(label="登記成績", data="score")
  ),
  QuickReplyButton(
    action= PostbackAction(label="指令列表", data="help")
  ),
])

from lineBot.models import User

from .bots import registeration, tool, chatBot
from .bots.score.main import score_main, score_gi_main, score_registerJob


whereList = {
  'register' : registeration.register,
  'score' : score_gi_main,
}

commandList = {
  'score' : score_main,
  'job' : score_registerJob,
  'help' : tool.help,
  'bike' : tool.bike,
}

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  thisUser = User.objects.get(lineID=event.source.user_id)

  for where in whereList:
    if thisUser.where == where:
      return whereList[where](event, thisUser)

  for command in commandList:
    if event.message.text == command:
      return commandList[command](event, thisUser)

  return chatBot.chat_bot(event, thisUser)


@handler.add(PostbackEvent)
def handle_postback(event):
  thisUser = User.objects.get(lineID=event.source.user_id)

  for command in commandList:
    if event.postback.data == command:
      return commandList[command](event, thisUser)


@handler.add(FollowEvent)
def handle_follow(event):
  newUser = User(
    lineID=event.source.user_id,
    where='register',
    status='wfi',
  )
  newUser.save()

  return line_bot_api.reply_message(event.reply_token,TextSendMessage(
    text= "請輸入 座號 + '空格' + 姓名 : "
  ))


@handler.add(UnfollowEvent)
def handle_unfollow(event):
  User.objects.get(lineID=event.source.user_id).delete()
