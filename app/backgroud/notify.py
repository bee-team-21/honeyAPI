# import json
# import dateutil.parser
# import traceback
# from datetime import timedelta
# from dateutil import tz
# from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError

# from app.core import configuration
# from app.models.history import History, Plataform
# from app.models.notify import NotifyPrometheus
# from app.models.prometheus import Alertmanager, AlertmanagerInDB
# from app.services import (
#     slack_service,
#     history_service,
#     phone_service,
#     whatsapp_service,
#     image_service,
#     telegram_service,
#     prometheus_service,
# )
# from app.models.slack_card import (
#     TypeText,
#     SectionText,
#     SectionDivider,
# )
# from app.models.whatsapp import WhatsApp
# from app.models.phone import Phone
# from app.models.slack import Slack
# from app.models.telegram import Telegram
# from app.models.image import Image

# from app.utils import telegram_bot_api, whatsapp_chat_api
# from app.utils.downloadImage import downloadImage
# from app.utils.responses import KEYS_ERROR, get_message
# from app.utils.sms import sendSMSClickatell
# from app.utils import currentmillis


# OFFSET_FIRING = configuration.APP_TIME_OFFSET_FIRING
# OFFSET_RESOLVED = configuration.APP_TIME_OFFSET_RESOLVED
# SAVE_IMAGES = configuration.APP_ENABLE_SAVE_IMAGES


# def write_notification_prometheus(item: Alertmanager, segments: list, user: str):
#     current = currentmillis.current()
#     print("Notificacion start in background {0}".format(current))
#     alert_db = AlertmanagerInDB(alert=item,start=current)
#     prometheus_service.create(alert_db)
#     i = 0
#     # Obtain slack channels
#     # Obtain sms
#     # Obtain wp
#     # Obtain telegram
#     items_slack = []
#     items_sms = []
#     items_wp = []
#     items_telegram = []
#     for i_segment in segments:
#         items_slack.extend(
#             slack_service.get_by_segment(
#                 Slack(segment=i_segment.name, token="", channel="")
#             )
#         )
#         items_sms.extend(
#             phone_service.get_by_segment(
#                 Phone(name="", number="", segment=i_segment.name)
#             )
#         )
#         items_wp.extend(
#             whatsapp_service.get_by_segment(
#                 WhatsApp(segment=i_segment.name, name="", group_id="")
#             )
#         )
#         items_telegram.extend(
#             telegram_service.get_by_segment(
#                 Telegram(segment=i_segment.name, name="", chat_id="")
#             )
#         )

#     if items_slack != [] or items_sms != [] or items_wp != [] or items_telegram != []:
#         # Exist channel to send  get data
#         alertObjects = []
#         for alert in item.alerts:
#             i += 1
#             text_message_wp = ""
#             text_message_telegram = ""
#             text_message_sms = ""
#             text_message_slack = []
#             text_message_slack_only = ""
#             initDate = dateutil.parser.parse(alert.startsAt)
#             try:
#                 initDateLocal = initDate.astimezone(tz=tz.tzlocal())
#             except:
#                 initDateLocal = initDate
#             initDateFormat = initDateLocal.strftime("%Y-%m-%d %H:%M:%S %z")
#             endDate = dateutil.parser.parse(alert.endsAt)
#             try:
#                 endDateLocal = endDate.astimezone(tz=tz.tzlocal())
#             except:
#                 endDateLocal = endDate
#             endDateFormat = endDateLocal.strftime("%Y-%m-%d %H:%M:%S %z")

#             # Block 1
#             text_message_wp += "*{0}. {1}*\nStart ⏰ {2}\nEnd ⏰ {3}\n".format(
#                 str(i), alert.status, initDateFormat, endDateFormat
#             )
#             text_message_telegram += "{0}. {1}\nStart ⏰ {2}\nEnd ⏰ {3}\n".format(
#                 str(i), alert.status, initDateFormat, endDateFormat
#             )
#             text_message_sms += "{0}-Name:{1} ".format(
#                 alert.status, alert.labels.alertname
#             )
#             text_message_slack_only += "*{0}. {1}*\nStart :alarm_clock: {2}\nEnd :alarm_clock: {3}\n".format(
#                 str(i), alert.status, initDateFormat, endDateFormat
#             )
#             text_message_slack.append(
#                 SectionText(
#                     typeText=TypeText.markdown,
#                     text="*{0}. {1}*\nStart :alarm_clock: {2}\nEnd :alarm_clock: {3}".format(
#                         str(i), alert.status, initDateFormat, endDateFormat
#                     ),
#                 ).to_json()
#             )

#             image = None
#             imageAnotationCopy = ""
#             imageName = ""
#             if alert.annotations.text is not None:
#                 imageAnotation = alert.annotations.text
#                 if alert.status == "resolved":
#                     toDate = int(round(endDate.timestamp() * 1000))
#                     restFromDate = endDate - timedelta(minutes=OFFSET_RESOLVED)
#                 else:
#                     toDate = int(round(initDate.timestamp() * 1000))
#                     restFromDate = initDate - timedelta(minutes=OFFSET_FIRING)

#                 fromDate = int(round(restFromDate.timestamp() * 1000))
#                 imageAnotationCopy = imageAnotation.replace(
#                     "&from=now", "&from={0}".format(str(fromDate)), 1
#                 )
#                 imageAnotationCopy = imageAnotationCopy.replace(
#                     "&to=now", "&to={0}".format(str(toDate)), 1
#                 )
#                 imageName = "{0}_{1}-{2}".format(str(i),str(fromDate), str(toDate), )
#                 try:
#                     image = downloadImage(imageAnotationCopy)  # class bytes
#                     if SAVE_IMAGES == True:
#                         image_service.create(Image(image=image))  # Save Images on Mongo
#                 except:
#                     traceback.print_exc()
#                     image = None
#                     text_message_telegram += get_message(
#                         type="error",
#                         key=KEYS_ERROR.cant_download_image_telegram,
#                     )
#                     text_message_wp += get_message(
#                         type="error",
#                         key=KEYS_ERROR.cant_download_image_whatsapp,
#                     )
#                     text_message_slack_only += get_message(
#                         type="error",
#                         key=KEYS_ERROR.cant_download_image_slack,
#                     )
#                     text_message_slack.append(
#                         SectionText(
#                             typeText=TypeText.markdown,
#                             text=get_message(
#                                 type="error",
#                                 key=KEYS_ERROR.cant_download_image_slack,
#                             ),
#                         ).to_json()
#                     )

#             # Block 2
#             annotation_wp = ""
#             annotation_telegram = ""
#             annotation_sms = ""
#             annotation_slack_only = ""
#             annotation_slack = []
#             for key in alert.annotations.__dict__.keys():
#                 content = alert.annotations.__dict__[key]
#                 if str(key).lower() == ("text").lower():
#                     content = imageAnotationCopy

#                 annotation_wp += "\n- {0}: {1}".format(str(key).upper(), str(content))
#                 annotation_slack_only += "\n- *{0}:* {1}".format(str(key).upper(), str(content))
#                 annotation_telegram += "\n- {0}: {1}".format(
#                     str(key).upper(), str(content)
#                 )
#                 if str(key).lower() != ("text").lower():
#                     annotation_sms += "-{0}:{1} ".format(str(key).upper(), str(content))
#                 annotation_slack.append(
#                     SectionText(
#                         typeText=TypeText.markdown,
#                         text="- *{0}*: {1}".format(str(key).upper(), str(content)),
#                     ).to_json()
#                 )

#             text_message_telegram += "\nAnnotation:" + annotation_telegram
#             text_message_wp += "\n_Annotation:_" + annotation_wp
#             text_message_slack_only += "\n_Annotation:_" + annotation_slack_only
#             text_message_sms += annotation_sms
#             text_message_slack.append(
#                     SectionText(
#                         typeText=TypeText.markdown,
#                         text="_Annotation:_",
#                     ).to_json()
#                 )
#             text_message_slack.extend(annotation_slack)
#             # Block 3
#             text_message_wp += "\n\n_Label:_\n- *Alertname*: {0}\n- *Instance*: {1}\n- *Job*: {2}\n- *Severity*: {3}\n- *Service*: {4}".format(
#                 alert.labels.alertname,
#                 alert.labels.instance,
#                 alert.labels.job,
#                 alert.labels.severity,
#                 alert.labels.service,
#             )
#             text_message_telegram += "\n\nLabel:\n- Alertname: {0}\n- Instance: {1}\n- Job: {2}\n- Severity: {3}\n- Service: {4}".format(
#                 alert.labels.alertname,
#                 alert.labels.instance,
#                 alert.labels.job,
#                 alert.labels.severity,
#                 alert.labels.service,
#             )
#             text_message_slack_only += "\n\n_Label:_\n- *Alertname*: {0}\n- *Instance*: {1}\n- *Job*: {2}\n- *Severity*: {3}\n- *Service*: {4}".format(
#                 alert.labels.alertname,
#                 alert.labels.instance,
#                 alert.labels.job,
#                 alert.labels.severity,
#                 alert.labels.service,
#             )
#             text_message_slack.append(
#                 SectionText(
#                     typeText=TypeText.markdown,
#                     text="\n_Label:_\n- *Alertname*: {0}\n- *Instance*: {1}\n- *Job*: {2}\n- *Severity*: {3}\n- *Service*: {4}".format(
#                         alert.labels.alertname,
#                         alert.labels.instance,
#                         alert.labels.job,
#                         alert.labels.severity,
#                         alert.labels.service,
#                     ),
#                 ).to_json()
#             )
#             critical = alert.labels.severity.lower() == "critical".lower()
#             # Block 4
#             text_message_wp += "\n\n_Common:_\n- *Alertname*: {0}\n- *Instance*: {1}\n- *Job*: {2}\n- *Severity*: {3}\n- *Service*: {4}".format(
#                 item.commonLabels.alertname,
#                 item.commonLabels.instance,
#                 item.commonLabels.job,
#                 item.commonLabels.severity,
#                 item.commonLabels.service,
#             )
#             text_message_telegram += "\n\nCommon:\n- Alertname: {0}\n- Instance: {1}\n- Job: {2}\n- Severity: {3}\n- Service: {4}".format(
#                 item.commonLabels.alertname,
#                 item.commonLabels.instance,
#                 item.commonLabels.job,
#                 item.commonLabels.severity,
#                 item.commonLabels.service,
#             )
#             text_message_slack_only += "\n\n_Common:_\n- *Alertname*: {0}\n- *Instance*: {1}\n- *Job*: {2}\n- *Severity*: {3}\n- *Service*: {4}".format(
#                 item.commonLabels.alertname,
#                 item.commonLabels.instance,
#                 item.commonLabels.job,
#                 item.commonLabels.severity,
#                 item.commonLabels.service,
#             )
#             text_message_slack.append(
#                 SectionText(
#                     typeText=TypeText.markdown,
#                     text="\n_Common:_\n- *Alertname*: {0}\n- *Instance*: {1}\n- *Job*: {2}\n- *Severity*: {3}\n- *Service*: {4}".format(
#                         item.commonLabels.alertname,
#                         item.commonLabels.instance,
#                         item.commonLabels.job,
#                         item.commonLabels.severity,
#                         item.commonLabels.service,
#                     ),
#                 ).to_json()
#             )
#             text_message_slack.append(SectionDivider().to_json())

#             notify = NotifyPrometheus(
#                 image=image,
#                 imageName=imageName,
#                 text_telegram=text_message_telegram,
#                 text_wp=text_message_wp,
#                 text_sms=text_message_sms,
#                 text_slack=text_message_slack,
#                 text_slack_only=text_message_slack_only,
#                 critical=critical,
#             )
#             alertObjects.append(notify)

#         for slack in items_slack:
#             client = WebClient(token=slack.token)
#             for alert in alertObjects:
#                 if alert.image is not None:
#                     try:
#                         response = client.files_upload(
#                             channels=slack.channel,
#                             file=alert.image,
#                             filename=alert.imageName + "_Prom.png",
#                             initial_comment=alert.text_slack_only
#                         )
#                         datapayload = alert.text_slack_only
#                         log = History()
#                         log.username_insert = user
#                         log.plataform = Plataform.slack
#                         log.request_payload = datapayload
#                         log.response_code = response.status_code
#                         log.response_text = str(response["message"])
#                         log.activator = write_notification_prometheus.__name__
#                         history_service.create(log)
#                         assert response["file"]  # the uploaded file
#                     except SlackApiError as e:
#                         # You will get a SlackApiError if "ok" is False
#                         assert e.response["ok"] is False
#                         assert e.response["error"]
#                         print(f"Got an error: {e.response['error']}")
#                         response = client.chat_postMessage(
#                             channel=slack.channel, blocks=alert.text_slack, text="Alerta"
#                         )
#                         datapayload = json.dumps(alert.text_slack)
#                         log = History()
#                         log.username_insert = user
#                         log.plataform = Plataform.slack
#                         log.request_payload = datapayload
#                         log.response_code = response.status_code
#                         log.response_text = str(response["message"])
#                         log.activator = write_notification_prometheus.__name__
#                         history_service.create(log)
#                     except:
#                         traceback.print_exc()
#                 else:
#                     try:
#                         response = client.chat_postMessage(
#                             channel=slack.channel, blocks=alert.text_slack, text="Alerta"
#                         )
#                         datapayload = json.dumps(alert.text_slack)
#                         log = History()
#                         log.username_insert = user
#                         log.plataform = Plataform.slack
#                         log.request_payload = datapayload
#                         log.response_code = response.status_code
#                         log.response_text = str(response["message"])
#                         log.activator = write_notification_prometheus.__name__
#                         history_service.create(log)
#                     except SlackApiError as e:
#                         assert e.response["ok"] is False
#                         assert e.response["error"]
#                         # str like 'invalid_auth', 'channel_not_found'
#                         print(f"Got an error: {e.response['error']}")

#                         datapayload = json.dumps(alert.text_slack)
#                         log = History()
#                         log.username_insert = user
#                         log.plataform = Plataform.slack
#                         log.request_payload = datapayload
#                         log.response_code = 400
#                         log.response_text = str(e.response["error"])
#                         log.activator = write_notification_prometheus.__name__
#                         history_service.create(log)

#         for telegram in items_telegram:
#             for alert in alertObjects:
#                 if alert.image is None:
#                     try:
#                         response = telegram_bot_api.sendText(
#                             chat_id=telegram.chat_id, msg=alert.text_telegram
#                         )
#                         log = History()
#                         log.username_insert = user
#                         log.plataform = Plataform.telegram
#                         log.request_payload = alert.text_telegram
#                         log.response_code = 200
#                         log.response_text = str(response)
#                         log.activator = write_notification_prometheus.__name__
#                         history_service.create(log)
#                     except:
#                         traceback.print_exc()
#                 else:
#                     try:
#                         response = telegram_bot_api.sendImage(
#                             chat_id=telegram.chat_id,
#                             photo=alert.image,
#                             caption=alert.text_telegram,
#                         )
#                         log = History()
#                         log.username_insert = user
#                         log.plataform = Plataform.telegram
#                         log.request_payload = alert.text_telegram
#                         log.response_code = 200
#                         log.response_text = str(response)
#                         log.activator = write_notification_prometheus.__name__
#                         history_service.create(log)
#                     except:
#                         traceback.print_exc()

#         for sms in items_sms:
#             for alert in alertObjects:
#                 if alert.critical == True:
#                     response = sendSMSClickatell(alert.text_sms, [sms.number])
#                     log = History()
#                     log.username_insert = user
#                     log.plataform = Plataform.sms
#                     log.request_payload = alert.text_sms
#                     log.activator = write_notification_prometheus.__name__
#                     if response is not None:
#                         log.response_code = response.status_code
#                         log.response_text = response.text
#                     history_service.create(log)

#         for wp in items_wp:
#             for alert in alertObjects:
#                 if alert.image is None:
#                     response = whatsapp_chat_api.sendText(
#                         chatID=wp.group_id, message=alert.text_wp
#                     )
#                 else:
#                     response = whatsapp_chat_api.sendFile(
#                         chatID=wp.group_id,
#                         file=alert.image,
#                         caption=alert.text_wp,
#                         fileMimeData="image/png;base64",
#                         fileName=alert.imageName + "_Prom.png",
#                     )
#                 log = History()
#                 log.username_insert = user
#                 log.plataform = Plataform.whatsapp
#                 log.request_payload = alert.text_wp
#                 log.response_code = response.status_code
#                 log.response_text = response.text
#                 log.activator = write_notification_prometheus.__name__
#                 history_service.create(log)
#     else:
#         print("*** Outputs not found ***")
#     end = currentmillis.current()
#     print("Notificacion in background {0} end {1}".format(current, end))
