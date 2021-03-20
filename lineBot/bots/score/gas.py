import requests

import environ
env = environ.Env()
environ.Env.read_env()

def send_score_to_sheet(event, thisUser):

  #use % to register the subject that doesn't belong to you
  testName = thisUser.memo.split('%')

  thisUser.status = ''
  thisUser.where = ''
  thisUser.memo = ''
  thisUser.save()

  scores = string_to_scores_list(event.message.text)

  return requests.post(
    env('GAS_ENTRY'),
    data = {
      'subj' : thisUser.job if len(testName)==1 else testName[1],
      'name' : testName[0],
      'scores' : scores
    }
  )

def string_to_scores_list(string):
  scoreTable = dict()

  for segment in string.split('\n'):
    try:
      number = int(segment[:2])
      score = ""
      score += segment[2:]

      scoreTable[number] = score
    except Exception:
      pass

  outputList = list()
  for number in range(1, 43+1):
    outputList.append(str(scoreTable.get(number, "")))

  return outputList
