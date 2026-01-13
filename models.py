from mongoengine import *
from uuid import uuid4
from datetime import datetime

class Role(Document):
    id=StringField(primary_key=True, default= lambda: str(uuid4()))
    name=StringField(required=True,unique=True)
    createdAt=DateTimeField(default=datetime.now())
    updateAt=DateTimeField()

class User(Document):
    id=StringField(primary_key=True, default= lambda: str(uuid4()))
    name=StringField(required=True)
    email=EmailField(required=True,unique=True)
    password=StringField(required=True)
    role=ReferenceField(Role,required=True)
    lastAssigned = BooleanField(default=False)
    createdAt=DateTimeField(default=datetime.now())
    updateAt=DateTimeField()

class Location(Document):
    id=StringField(primary_key=True, default= lambda: str(uuid4()))
    street=StringField(required=True)
    city=StringField(required=True)
    state=StringField(required=True)
    country=StringField(required=True)
    pincode=StringField(required=True,min_length=6,max_length=6)
    createdAt=DateTimeField(default=datetime.now())
    updateAt=DateTimeField()

class Issue(Document):
    user=ReferenceField(User,required=True)
    id=StringField(primary_key=True, default= lambda: str(uuid4()))
    issueTittle=StringField(required=True)
    issueDescription=StringField(required=True)
    category=StringField(required=True,choices=["Road","Garbage","Water","Electricity","Others"])
    location=ReferenceField(Location,required=True)
    imagePath=URLField()
    status=StringField(default='reported',choices=['reported','progress','resolved','rejected'])
    tags=StringField()
    assignedTo=ReferenceField(User,required=True)
    createdAt=DateTimeField(default=datetime.now())
    updatedAt=DateTimeField()

class IssueStatusHistory(Document):
    id=StringField(primary_key=True, default= lambda: str(uuid4()))
    issue=ReferenceField(Issue,required=True)
    prvStatus=StringField(required=True)
    nextStatus=StringField(required=True)
    updatedBy=ReferenceField(User,required=True)
    rejectedReason=StringField()
    resolvedAt=DateTimeField()
    updatedAt=DateTimeField()

class Notifications(Document):
    id=StringField(primary_key=True, default= lambda: str(uuid4()))
    user=ReferenceField(User,required=True)
    issue=ReferenceField(Issue,required=True)
    message=StringField(required=True)
    isViewed=BooleanField(default=False)
    createdAt=DateTimeField(default=datetime.now())
    updatedAt=DateTimeField()