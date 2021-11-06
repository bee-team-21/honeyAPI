import json
from typing import List, Optional, Union

from pydantic.main import BaseModel



class TypeText:
    plain_text = "plain_text"
    markdown = "mrkdwn"


class SectionText(BaseModel):
    typeText: str 
    text: str
    emoji: Optional[bool] = False

    # def __init__(self, typeText, text, emoji):
    #     self.typeText = (
    #         TypeText.plain_text
    #         if typeText != TypeText.plain_text and typeText != TypeText.markdown
    #         else typeText
    #     )
    #     self.text = text
    #     self.emoji = emoji

    def to_json(self):
        if self.typeText == TypeText.markdown:
            return {
                "type": "section",
                "text": {
                    "type": self.typeText,
                    "text": " " if self.text == "" else self.text,
                },
            }
        else:
            return {
                "type": "section",
                "text": {
                    "type": self.typeText,
                    "text": " " if self.text == "" else self.text,
                    "emoji": self.emoji,
                },
            }


class SectionImage(BaseModel):
    imageUrl: str
    nameImage: str
    text: Optional[str] = "Image"
    emoji: Optional[bool]= False

    # def __init__(self, text, imageUrl, nameImage, emoji):
    #     self.text = text
    #     self.imageUrl = imageUrl
    #     self.nameImage = nameImage
    #     self.emoji = emoji

    def to_json(self):
        return {
            "type": "image",
            "title": {
                "type": TypeText.plain_text,
                "text": " " if self.text == "" else self.text,
                "emoji": self.emoji,
            },
            "image_url": "https://api.slack.com/img/blocks/bkb_template_images/beagle.png"
            if self.imageUrl == ""
            else self.imageUrl,
            "alt_text": " " if self.nameImage == "" else self.nameImage,
        }


class SectionDivider(BaseModel):
    def to_json(self):
        return {"type": "divider"}


class SectionTextWithButton(BaseModel):
    textHead:str
    typeText: str = TypeText.plain_text
    textButton: str
    urlButton: str
    emoji: Optional[bool]= False

    # def __init__(self, typeText, text, textButton, urlButton, emoji):
        # self.typeText = (
        #     TypeText.plain_text
        #     if typeText != TypeText.plain_text and typeText != TypeText.markdown
        #     else typeText
        # )
        # self.text = text
        # self.textButton = textButton
        # self.urlButton = urlButton
        # self.emoji = emoji

    def to_json(self):
        if self.typeText == TypeText.markdown:
            return {
                "type": "section",
                "text": {
                    "type": self.typeText,
                    "text": " " if self.textHead == "" else self.textHead,
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": TypeText.plain_text,
                        "text": " " if self.textButton == "" else self.textButton,
                    },
                    "url": "https://api.slack.com/block-kit"
                    if self.urlButton == ""
                    else self.urlButton,
                },
            }
        else:
            return {
                "type": "section",
                "text": {
                    "type": self.typeText,
                    "text": " " if self.textHead == "" else self.textHead,
                    "emoji": self.emoji,
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": TypeText.plain_text,
                        "text": " " if self.textButton == "" else self.textButton,
                    },
                    "url": "https://api.slack.com/block-kit"
                    if self.urlButton == ""
                    else self.urlButton,
                },
            }


class Field(BaseModel):
    typeText: str = TypeText.plain_text
    text: Optional[str] = "Text Field"
    emoji: Optional[bool]= False
    # def __init__(self, typeText, text, emoji):
    #     self.typeText = (
    #         TypeText.plain_text
    #         if typeText != TypeText.plain_text and typeText != TypeText.markdown
    #         else typeText
    #     )
    #     self.text = text
    #     self.emoji = emoji

    def to_json(self):
        if self.typeText == TypeText.markdown:
            return {
                "type": self.typeText,
                "text": " " if self.text == "" else self.text,
            }
        else:
            return {
                "type": self.typeText,
                "text": " " if self.text == "" else self.text,
                "emoji": self.emoji,
            }


class SectionFields(BaseModel):
    fields: List[Field]
    # def __init__(self, fields):
    #     self.fields = fields

    def to_json(self):
        jsonfields = []
        for field in self.fields:
            jsonfields.append(field.to_json()) 
        return {"type": "section", "fields": jsonfields}

class SectionSimple(BaseModel):
    type: str = "Divider"
    content: Union[SectionText,SectionImage,SectionTextWithButton,SectionDivider]

class SectionMultiple(BaseModel):
    type: str = "Fields"
    contents: SectionFields