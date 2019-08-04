import requests, bs4, sys, re
from twilio.rest import Client

res = requests.get('https://weather.com/weather/today/l/38117:4:US')
try:
    res.raise_for_status()
except Exception as exc:
    print('Could not open that URL due to issue: %s' %(exc))

wS = bs4.BeautifulSoup(res.text)

temps = []
forecasts = []
precips = []


for i in range(0, 5, 2):
    nextTemp = wS.select('#daypart-%d > div > div.today-daypart-temp > span' %(i))
    tempRegex = re.compile(r'>(.*?)<')
    mo = tempRegex.search(str(nextTemp))
    temps.append(mo.group(1))

    forecast = wS.select('#daypart-%d > div > div.today-daypart-top' %(i))
    forecastRegex = re.compile(r'id="dp%d-phrase">(.*?)<' %(i))
    fO = forecastRegex.search(str(forecast))
    forecasts.append(fO.group(1))

    precipitation = wS.select('#daypart-%d > div > div.today-daypart-precip > span.precip-val > span' %(i))
    precRegex = re.compile(r'>(.*?)<')
    pO = precRegex.search(str(precipitation))
    precips.append(pO.group(1))


accountSID = 'ACa5f2bc1e14abad23c2d84662734a5d2a'
authToken = '7defd5f17295a4ed4175df0ec39de40a'
myTwilioNumber = '+19014460679'
myCellPhone ='+17342498014'

twilioCli = Client(accountSID, authToken)

message = 'Todays forecast is ' + forecasts[0] + '. There is a high of ' + temps[0] +\
' degrees and a ' + precips[0] + ' percent chance of rain.\nTomorrows forecast is ' + forecasts[1] +\
'. There is a high of ' + temps[1] +' degrees and a ' + precips[1] +\
' percent chance of rain.\nThe Day After\'s forecast is ' + forecasts[2] + '. There is a high of ' +\
temps[2] + ' degrees and a ' + precips[2] + ' percent chance of rain.\n'

message = twilioCli.messages.create(body=message, from_=myTwilioNumber, to=myCellPhone)

print(message.sid)
