import requests
import json
import traceback
from app.core.configuration import APP_FB_PAGE, APP_FB_TOKEN

def post_image(text: str, image: str):
    try:
        url = "https://graph.facebook.com/{}/photos?access_token={}".format(APP_FB_PAGE,APP_FB_TOKEN)
        payload = json.dumps({
            "message": text,
            "url": image
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
    except:
        traceback.print_exc