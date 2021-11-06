from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.validators.mongo import PyObjectId

class Labels(BaseModel):
    alertname: Optional[str] = "alertname"
    instance: Optional[str] = "instance"
    service: Optional[str] = "service"
    severity: Optional[str] = "severity"
    job: Optional[str] = "job"


class Annotations(BaseModel):
    console:  Optional[str] = "console"
    summary:  Optional[str] = "summary"
    text:  Optional[str] = None
    description:  Optional[str] = None

class Alert(BaseModel):
    status: Optional[str] = "status"
    labels: Optional[Labels] = Labels()
    annotations: Optional[Annotations] = Annotations()
    startsAt: Optional[str] = "2021-01-31T12:00:29.588884798-04:00"
    endsAt:  Optional[str] = "0001-01-01T00:00:00"
    generatorURL: Optional[str] = "http://prometheus.int.example.net/<generating_expression>"



class Alertmanager(BaseModel):
    receiver: str
    status: Optional[str] = "status"
    alerts: List[Alert]
    # groupLabels: GroupLabels
    commonLabels: Optional[Labels] = Labels()
    commonAnnotations: Optional[Annotations] = Annotations()
    externalURL: Optional[str] = "externalURL"
    version: Optional[str] = "version"
    groupKey: Optional[str] = "groupKey"
class AlertmanagerInDB(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    alert: Alertmanager
    start: Optional[int]
    disabled: Optional[bool] = False
    date_insert: Optional[datetime] = None