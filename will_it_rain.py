import requests
import os
from twilio.rest import Client

#MY_LAT = -46.24 # Rainy test co-ords
#MY_LON = 168.20
MY_LAT = os.environ.get("MY_LAT")
MY_LON = os.environ.get("MY_LON")
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
API_Key = os.environ.get("OWM_API_KEY")

account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("AUTH_TOKEN")
twilio_num = os.environ.get("twilio_num")

params = {
    "lat": MY_LAT,
    "lon": MY_LON,
    "appid": API_Key,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_Endpoint, params=params)
response.raise_for_status()
data = response.json()

will_rain = False
twelve_hr_section = data["hourly"][:12]
for hour in twelve_hr_section:
    code = hour["weather"][0]["id"]
    if code < 700:
        will_rain = True
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It might rain today. Remember your ☂ ",
        from_=twilio_num,
        to="+447999050569"
    )

    print(message.status)
