import datetime
today = datetime.datetime.now().date
temp = str(today())

print(temp)

# from linebot import LineBotApi
# import environ
# env = environ.Env()
# environ.Env.read_env()

# line_bot_api = LineBotApi(env('channel_access_token'))

# # url = 'https://vflc-shite.herokuapp.com/webhook/'
# url = 'https://ca4c531ee119.ngrok.io/webhook/'

# line_bot_api.set_webhook_endpoint(url)


# # webhook = line_bot_api.get_webhook_endpoint()
# # print(webhook.endpoint)
# # print(webhook.active)

