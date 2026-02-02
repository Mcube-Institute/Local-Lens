from mongoengine import *
from uuid import uuid4
from datetime import datetime

class Role(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid4()))
    name = StringField(required=True, unique=True)
    createdAt = DateTimeField(default=datetime.now())
    updatedAt = DateTimeField()

class User(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid4()))
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField()
    role = ReferenceField(Role, required=True, reverse_delete_rule=DENY,default=lambda: Role.objects(name="User").first())
    lastAssigned = BooleanField(default=False)
    createdAt = DateTimeField(default=datetime.now())
    updatedAt = DateTimeField()

class Location(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid4()))
    street = StringField(required=True)
    city = StringField(required=True)
    state = StringField(required=True)
    country = StringField(required=True)
    pincode = StringField(required=True, min_length=6, max_length=6)
    createdAt = DateTimeField(default=datetime.now())
    updatedAt = DateTimeField()

class Issue(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid4()))
    user = ReferenceField(User, required=True)
    issueTittle = StringField(required=True)   
    issueDescription = StringField(required=True)
    category = StringField(required=True)
    location = ReferenceField(Location, required=True)
    attachments = ListField(StringField())
    tags = StringField()
    status = StringField(default="REPORTED",choices=["REPORTED", "IN_PROGRESS", "RESOLVED", "CLOSED"])
    assignedTo = ReferenceField(User, required=True)
    createdAt = DateTimeField(default=datetime.now())
    updatedAt = DateTimeField()

class IssueStatusHistory(Document):
    id=StringField(primary_key=True, default= lambda: str(uuid4()))
    issue=ReferenceField(Issue,required=True)
    prevStatus=StringField(required=True)
    nextStatus=StringField(required=True)
    updatedBy=ReferenceField(User,required=True)
    rejectedReason=StringField()
    resolvedAt=DateTimeField()
    createdAt = DateTimeField(default=datetime.now())
    updatedAt=DateTimeField()

class Notifications(Document):
    id=StringField(primary_key=True, default= lambda: str(uuid4()))
    user=ReferenceField(User,required=True)
    issue=ReferenceField(Issue,required=True)
    message=StringField(required=True)
    isViewed=BooleanField(default=False)
    createdAt=DateTimeField(default=datetime.now())
    updatedAt=DateTimeField()