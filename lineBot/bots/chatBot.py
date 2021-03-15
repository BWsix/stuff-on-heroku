from linebot.models import TextSendMessage

from lineBot.views import line_bot_api, QUICKREPLY_MENU

scripts = {
  'hi': "hi there!",
  'hello': "hello, I'm a bot!",
  'bye': "good bye my friend",
  'oh': "oh?",
  'yeah': "嗚呼~",
  'vflc': "it stands for 'Verified LoliCop'!",
  'camellia': "https://youtu.be/9X7I3bW49S8",
  'fuck': "🤔",
  'shite': "fun fact : shite is actually the name of this web app folder",
  'omg': "slap like now!",
  'k': "k...",
  '收到': "了解!!",
  '好喔': "呵呵你看看你",
  'yo': "battle",
  '地理': "gan",
  'loli': "Lolis are cute, and thus I love lolis.",
  '蘿莉': "很可愛<3",
  'shota': "Shotas are cute, and thus I love lolis.",
  '正太': "很可愛<3",
}

def chat_bot(event, thisUser):

  scripts['gan'] = f"{thisUser.name}不要鬧"

  for kw in scripts:
    if(event.message.text == kw):
      return line_bot_api.reply_message(event.reply_token,TextSendMessage(
        text= scripts[kw],
        quick_reply=QUICKREPLY_MENU
      ))

  return line_bot_api.reply_message(event.reply_token,TextSendMessage(
    text= f"hello, {thisUser.name}.",
    quick_reply=QUICKREPLY_MENU
  ))
