
#!/usr/bin/env python3
from decimal import Decimal

import mongoengine as me
from datetime import datetime


# Connect to the MongoDB instance
me.connect('jobhub_database', host='localhost', port=27017)

#creating a job post model
class JobPost(me.Document):
    title = me.StringField(required=True, max_length=200)
    company = me.StringField(required=True, max_length=100)
    location = me.StringField(max_length=100)
    description = me.StringField()
    posted_date = me.DateTimeField(default=datetime.utcnow)
    salary = me.DecimalField(min_value=0)

    def _str_(self):
        return f'{self.title} at {self.company}'

#creating a Users model

class User(me.Document):
    username = me.StringField(required=True, unique=True)
    email = me.EmailField(required=True, unique=True)
    password = me.StringField(required=True)
    is_admin = me.BooleanField(default=False)

    def _str_(self):
        return self.username

#create and save jobPost document to mongodb

job = JobPost(
    title="JuniorSoftware Engineer",
    company="Tech Innovators",
    location="Johannesburg",
    description="Develop and maintain software solutions.",
    salary=Decimal('7500.00')

)

# Save it to MongoDB
job.save()

#creating a user document and saving it to mongodb

user = User(
        username="Itumeleng Malau",
        email="itumeleng@gmail.com",
        password="flyaway",
        is_admin=True
)
user.save()