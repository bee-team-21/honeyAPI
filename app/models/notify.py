from datetime import datetime
from bson import ObjectId
from typing import List, Union
from pydantic import BaseModel
from app.models.slack_card import (
    SectionMultiple,
    SectionSimple,
    SectionText,
    SectionImage,
    SectionTextWithButton,
    SectionDivider,
    TypeText,
    Field,
    SectionFields,
)


class NotifyPrometheus(BaseModel):
    image: bytes = None
    imageName: str = ""
    text_slack_only: str = ""
    text_slack: list = []
    text_sms: str = ""
    text_wp: str = ""
    text_telegram: str = ""
    critical: bool = False
class Notify(BaseModel):
    segment: str
    username: str = "Alertbot"
    icon_emoji: str = ":exclamation:"
    data: List[Union[SectionSimple, SectionMultiple]] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    class Config:
        schema_extra = {
            "example": {
                "segment": "default",
                "username": "Alertbot",
                "icon_emoji": ":exclamation:",
                "data": [
                    {
                        "type": "Text",
                        "content": {
                            "typeText": "mrkdwn",
                            "text": "Hello World With Markdown",
                        },
                    },
                    {
                        "type": "Text",
                        "content": {
                            "typeText": "plain_text",
                            "text": "Hello World Plain :) Without Emojis",
                            "emoji": False,
                        },
                    },
                    {
                        "type": "Text",
                        "content": {
                            "typeText": "plain_text",
                            "text": "Hello World Plain :) With Emojis",
                            "emoji": True,
                        },
                    },
                    {"type": "Divider", "content": {}},
                    {
                        "type": "Image",
                        "content": {
                            "imageUrl": "https://api.slack.com/img/blocks/bkb_template_images/beagle.png",
                            "nameImage": "Name Image",
                            "text": "Text Image",
                            "emoji": True,
                        },
                    },
                    {
                        "type": "Fields",
                        "contents": {
                            "fields": [
                                {
                                    "typeText": "plain_text",
                                    "text": "My Text",
                                    "emoji": False,
                                },
                                {
                                    "typeText": "plain_text",
                                    "text": "My Text :D",
                                    "emoji": True,
                                },
                            ]
                        },
                    },
                    {
                        "type": "TextWithButton",
                        "content": {
                            "typeText": "plain_text",
                            "textHead": "Text",
                            "textButton": "Button",
                            "urlButton": "https://api.slack.com/block-kit",
                            "emoji": False
                        }
                    }
                ],
            }
        }


def BuildSegmentText(content: SectionText):
    text = ValidateNoEmpty(content.text, " ")
    type = ValidateNoEmpty(content.typeText, TypeText.plain_text)
    emoji = ValidateNoEmptyBool(content.emoji, False)
    return SectionText(typeText=type, text=text, emoji=emoji).to_json()


def BuildSegmentImage(content: SectionImage):
    # Validate Image
    image = ValidateNoEmpty(
        content.imageUrl,
        "https://api.slack.com/img/blocks/bkb_template_images/beagle.png",
    )
    # Validate Name
    name = ValidateNoEmpty(content.nameImage, "Image")
    # Validate Text
    text = ValidateNoEmpty(content.text, " ")
    # Validate Emoji
    emoji = ValidateNoEmptyBool(content.emoji, False)
    return SectionImage(
        imageUrl=image, nameImage=name, text=text, emoji=emoji
    ).to_json()


def BuildSegmentDivider(content: SectionDivider):
    return SectionDivider().to_json()


def BuildSegmentTextButton(content: SectionTextWithButton):
    text = ValidateNoEmpty(content.textHead, " ")
    type = ValidateNoEmpty(content.typeText, TypeText.plain_text)
    textButton = ValidateNoEmpty(content.textButton, "Go")
    urlButton = ValidateNoEmpty(content.urlButton, "https://google.com")
    emoji = ValidateNoEmptyBool(content.emoji, False)
    return SectionTextWithButton(
        typeText=type,
        textHead=text,
        textButton=textButton,
        urlButton=urlButton,
        emoji=emoji,
    ).to_json()


def BuildSegmentField(content: SectionFields):
    slackFields = []
    for ifield in content.fields:
        slackFields.append(
            Field(
                typeText=ValidateNoEmpty(ifield.typeText, TypeText.plain_text),
                text=ValidateNoEmpty(ifield.text, " "),
                emoji=ValidateNoEmptyBool(ifield.emoji, False),
            )
        )
    return SectionFields(fields=slackFields).to_json()


def ValidateNoEmpty(text: str, defaulText: str):
    validate = text
    if validate == "":
        validate = defaulText
    return validate


def ValidateNoEmptyBool(valBool: bool, defaultBool: bool):
    validate = valBool
    if validate != True and validate != False:
        validate = defaultBool
    return validate


switcher = {
    "Text": BuildSegmentText,
    "Image": BuildSegmentImage,
    "Divider": BuildSegmentDivider,
    "TextWithButton": BuildSegmentTextButton,
    "Fields": BuildSegmentField,
}


def switch(argument: Union[SectionSimple, SectionMultiple]):
    # Get the function from switcher dictionary
    types = argument.type
    func = switcher.get(types, BuildSegmentDivider)
    # Execute the function
    if types == "Fields":
        return func(argument.contents)
    else:
        return func(argument.content)
