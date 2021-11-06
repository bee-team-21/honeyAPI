import ast
import os
import traceback
import json
from app.models.result import Result
from app.core import configuration

LANG = configuration.APP_LANG
dirpath = os.path.dirname(__file__)
path = os.path.join(dirpath, "..", "lang", LANG)
dictionary = dict()
with open(path, encoding="utf-8") as fh:
    dictionary = json.load(fh)


def get_error_message(key="default"):
    message = get_message(type="error", key=key)
    return Result(code=0, message=message)


def get_success_message(key="default"):
    message = get_message(type="success", key=key)
    return Result(code=1, message=message)


def get_message(type="success", key="default"):
    try:
        message = dictionary[type][key]
        return message
    except:
        try:
            traceback.print_exc()
            return dictionary[type]["default"]
        except:
            traceback.print_exc()
            return 'Something went wrong with the dictionary "{0}"'.format(LANG)


class KEYS_SUCCESS:
    default = "default"
    object_inserted = "object_inserted"
    notify_in_backgroud = "notify_in_backgroud"


class KEYS_ERROR:
    default = "default"
    object_not_found = "object_not_found"
    id_not_found = "id_not_found"
    name_already_exist = "name_already_exist"
    segment_not_found = "segment_not_found"
    token_no_valid = "token_no_valid"
    cant_download_image_slack = "cant_download_image_slack"
    cant_upload_image_slack = "cant_upload_image_slack"
    cant_download_image_whatsapp = "cant_download_image_whatsapp"
    cant_download_image_telegram = "cant_download_image_telegram"
