#!/usr/bin/env python3

from decimal import Decimal
import mongoengine as me
from datetime import datetime

# Connect to the MongoDB instance
me.connect('jobhub_database', host='mongodb+srv://itumelengmalau:Itumeleng1@cluster0.ivz3n.mongodb.net')

# Creating a JobPost model
class JobPost(me.Document):
    title = me.StringField(required=True, max_length=200)
    company = me.StringField(required=True, max_length=100)
    location = me.StringField(max_length=100)
    description = me.StringField()
    posted_date = me.DateTimeField(default=datetime.utcnow)
    salary = me.DecimalField(min_value=0)

    def __str__(self):
        return f'{self.title} at {self.company}'

# Creating a User model
class User(me.Document):
    username = me.StringField(required=True, unique=True)
    email = me.EmailField(required=True, unique=True)
    password = me.StringField(required=True)
    is_admin = me.BooleanField(default=False)

    def __str__(self):
        return self.username

# Create and save a JobPost document to MongoDB
job = JobPost(
    title="Junior Software Engineer",
    company="Tech Hub",
    location="Johannesburg",
    description="Develop and maintain software solutions.",
    salary=Decimal('7500.00')
)

# Save it to MongoDB
job.save()

# Create and save a User document to MongoDB
user = User(
    username="Itumeleng Mulaudzi",
    email="itumeleng1@gmail.com",
    password="flyaway",
    is_admin=True
)
user.save()
