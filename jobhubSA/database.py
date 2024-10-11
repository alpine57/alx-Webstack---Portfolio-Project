
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
#!/usr/bin/env python3
from decimal import Decimal
import mongoengine as me
from datetime import datetime
import bcrypt

# Connect to the MongoDB instance
me.connect('jobhubSA', host='localhost', port=27017)

# Creating a JobPost model
class JobPost(me.Document):
    title = me.StringField(required=True, max_length=200)
    company = me.StringField(required=True, max_length=100)
    location = me.StringField(max_length=100)
    description = me.StringField()
    posted_date = me.DateTimeField(default=datetime.utcnow)
    salary = me.DecimalField(min_value=Decimal('0.00'))

    def __str__(self):
        return f'{self.title} at {self.company}'


# Creating a User model
class User(me.Document):
    username = me.StringField(required=True, unique=True, max_length=50)
    email = me.EmailField(required=True, unique=True)
    password = me.StringField(required=True)
    is_admin = me.BooleanField(default=False)

    def __str__(self):
        return self.username

    # Hash the password before saving
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Verify if the input password matches the stored hashed password
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


# Get the username, email, and password dynamically from user input (Terminal)
username_input = input("Enter username: ")
email_input = input("Enter email: ")
password_input = input("Enter password: ")

# Creating a User document dynamically
user = User(
    username=username_input,
    email=email_input,
    is_admin=False  # or True depending on the requirement
)

# Set the hashed password dynamically
user.set_password(password_input)

# Save the user to MongoDB
user.save()

print(f"User {username_input} created successfully!")

# Example: Verify a user's password by asking them to enter it again
input_password = input(f"Enter the password to verify for {username_input}: ")
is_correct_password = user.check_password(input_password)

if is_correct_password:
    print(f"Password for user {user.username} is correct!")
else:
    print(f"Password for user {user.username} is incorrect!")
