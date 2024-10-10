from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Set up the MongoDB connection

app.config['MONGO_URI'] = "mongodb://localhost:27017/jobhubSA"
mongo = PyMongo(app)

# Route for the home page (show job listings)
@app.route('/')
def index():
    jobs = mongo.db.jobs.find()  # Get all job posts
    return render_template('index.html', jobs=jobs)

# Route for posting a new job
@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        job_title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        
        
        # Insert new job into the database
        mongo.db.jobs.insert_one({
            'title': job_title,
            'company': company,
            'description': description
        })
        return redirect(url_for('index'))
    
    return render_template('post_job.html')

# Route to view a specific job post
@app.route('/job/<job_id>')
def job_detail(job_id):
    job = mongo.db.jobs.find_one({'_id': ObjectId(job_id)})
    return render_template('job_list.html', job=job)

if __name__ == '__main__':
    app.run(debug=True)
