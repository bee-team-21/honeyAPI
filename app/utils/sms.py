import json
import requests
from app.core import configuration
clickatellURL = configuration.APP_CLICKATELL_URL
headerAuthorization = 'Bearer {0}'.format(configuration.APP_CLICKATELL_TOKEN)
class Clickatell(object):
	@staticmethod
	def sendSMS(message,numbers):
		payload = json.dumps({"text": message,"to": numbers})
		headers = {
			"Content-Type": "application/json",
			"X-Version": "1",
			"Authorization": headerAuthorization,
			"Accept": "application/json"
			}
		response = requests.request("POST", clickatellURL, data=payload, headers=headers)
		return response


        
def sendSMSClickatell(text: str,numbers: list):
	try:
		response = Clickatell.sendSMS(text, numbers)
		return response
	except:
		return None