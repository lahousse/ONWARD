# QXYGI9IWD2OYC2AR read key
import requests
#msg=requests.get("https://api.thingspeak.com/channels/1704831/feeds.json?results=2")
msg=requests.get("https://api.thingspeak.com/channels/1704831/feeds.json?results=2")
msg=msg.json()['feeds'][-1]
#print(msg[1:])
print(msg)
#print("\nThe Message sent was: \n\n"+str(msg))

