from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, login_user, logout_user, current_user, LoginManager
from mongoengine import connect, StringField, BooleanField, EmailField, Document
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
login_manager = LoginManager(app)
app.secret_key = 'supersecretkey'

# Connecting to MongoDB Atlas
connect(db="jobhub_db", host="your_mongo_atlas_url")

#creating User model for storing data in mongodb

class User(Document, UserMixin):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    is_admin = BooleanField(default=False)
    skills = ListField(StringField())
    portfolio = URLField()
    courses_completed = ListField(StringField())  # Can also be ReferenceField to another model
    reviews = ListField(StringField())  # Example: ["Great work!", "Very professional"]
    is_mentor = BooleanField(default=False)
    mentor_bio = StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

#signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        user.save()
        login_user(user)
        return redirect(url_for('profile'))
    return render_template('signup.html')

#login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.objects(email=request.form['email']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('profile'))
        flash("Invalid login details.")
    return render_template('login.html')
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

#defining job_post model
class JobPost(Document):
    title = StringField(required=True)
    company = StringField(required=True)
    location = StringField(required=True)
    category = StringField(required=True)
    description = StringField()
    salary = DecimalField()

@app.route('/jobs')
def job_listings():
    location = request.args.get('location')
    category = request.args.get('category')

    query = {}
    if location:
        query['location__icontains'] = location
    if category:
        query['category__icontains'] = category

    jobs = JobPost.objects(**query)
    return render_template('job_listings.html', jobs=jobs)

#creating an application model

class Application(Document):
    user = ReferenceField(User)
    job = ReferenceField(JobPost)
    applied_at = DateTimeField(default=datetime.utcnow)

@app.route('/apply/<job_id>', methods=['POST'])
@login_required
def apply_job(job_id):
    job = JobPost.objects(id=job_id).first()
    if job:
        application = Application(user=current_user, job=job)
        application.save()
        return redirect(url_for('job_listings'))
    return 'Job not found', 404

#mentorship route
@app.route('/mentors')
def mentors():
    mentors = User.objects(is_mentor=True)
    return render_template('mentors.html', mentors=mentors)
# definig courses model
class Course(Document):
    title = StringField(required=True)
    description = StringField()
    duration = IntField()

# defining user course progress

class UserCourseProgress(Document):
    user = ReferenceField(User)
    course = ReferenceField(Course)
    progress = DecimalField(min_value=0, max_value=100)

#courses route
@app.route('/courses')
def courses():
    courses = Course.objects()
    return render_template('courses.html', courses=courses)
#route to getting a specific course by id
@app.route('/course/<course_id>')
@login_required
def course_detail(course_id):
    course = Course.objects(id=course_id).first()
    progress = UserCourseProgress.objects(user=current_user, course=course).first()
    return render_template('course_detail.html', course=course, progress=progress)
(venv) itumeleng@LDIL-11:~/alx-Webstack---Portfolio-Project/jobhubSA/full-project$
