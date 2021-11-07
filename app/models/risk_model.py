from typing import Literal, Optional
from pydantic import BaseModel, Field

class Risk(BaseModel):
    risk: Optional [Literal ['low','mid','high']] = None
    confidence: float
    detail: Optional[str] = ""
    image: Optional[str]
    imageBinary: Optional[bytes]
    imageContentType: Optional[str]
    imageFilename: Optional[str]
    site: Optional[str]
    gps: Optional[str]