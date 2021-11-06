import time
import requests
import mimetypes
def send_message(webhook: str, text: str, file: bytes= None, content_type: str = None, filename: str = None):
    
    if file is None:
        payload={'content': text}
        response = requests.request("POST", webhook, data=payload)
    else:
        
        file_data={
            'content': (None, text),
            'file':(filename,file) }
        response = requests.request("POST", webhook, files=file_data)
    return response
