from bson import ObjectId
from flask import render_template, request, redirect, session, flash,url_for
from flask_restful import Resource, reqparse
from flask_paginate import Pagination, get_page_args
from app import app, db
from app.models import Reviews
from utils import get_DB
import time

jobsDB = None
usersDb = None
forumDB = None
db = None
isTest = False

def setTest(test):
    global isTest
    isTest = test

def intializeDB():
    global jobsDB, db, usersDb, forumDB
    db = get_DB(isTest)
    usersDb = db.Users
    jobsDB = db.Jobs
    forumDB = db.Forum


def process_jobs(job_list):
    processed = list()
    for job in job_list:
        job['id'] = job.pop('_id')
        processed.append(job)
    return processed


def get_all_jobs():
    all_jobs = list(jobsDB.find())
    return process_jobs(all_jobs)


def get_my_jobs(username):
    intializeDB()
    user = usersDb.find_one({"username": username})
    if user == None:
        pass

    reviews = user['reviews']
    return process_jobs(jobsDB.find({"_id": {'$in': reviews}}))

# create job review


@app.route('/review')
def review():
    """
    An API for the user review page, which helps the user to add reviews
    """
    intializeDB()
    if 'username' not in session or not session['username']:
        flash('Please log in first to add a review.',"danger")
        return redirect('/login')
    # if not ('username' in session.keys() and session['username']):
    #     return redirect("/")
    entries = get_all_jobs()
    return render_template('review-page.html', entries=entries)


# view all
@app.route('/pageContent')
def page_content():
    """An API for the user to view all the reviews entered"""
    intializeDB()
    entries = get_all_jobs()
    dept_filter_entries = jobsDB.distinct("department")
    location_filter_entries = jobsDB.distinct("locations")
    title_filter_entries = jobsDB.distinct("title")
    company_filter_entries = jobsDB.distinct("company")

    # pagination

    # print(entries)
    page, per_page, offset = get_page_args(
        page_parameter="page", per_page_parameter="per_page")
    total = len(entries)

    if not page or not per_page:
        offset = 0
        per_page = 10
        pagination_entries = entries[offset: offset+per_page]
    else:
        pagination_entries = entries[offset: offset+per_page]
        # print("ELSE!!!")

    pagination = Pagination(page=page, per_page=per_page,
                            total=total, css_framework='bootstrap4')

    #
    # print("HERE!!!", pagination._get_single_page_link())
    # return render_template('page_content.html', entries=pagination_entries, page=page, per_page=per_page, pagination=pagination)
    return render_template('page_content.html', entries=pagination_entries, page=page, per_page=per_page, pagination=pagination, dept_filter_entries=dept_filter_entries, location_filter_entries=location_filter_entries, company_filter_entries=company_filter_entries)

@app.route('/forum')
def forum():
    """API for viewing all forum topics"""
    intializeDB()
    topics = forumDB.find()
    return render_template('forum.html', topics=topics)

@app.route('/forum/new', methods=['GET', 'POST'])
def new_topic():
    """API for creating a new forum topic"""
    intializeDB()
    # Check if 'username' is in session
    if 'username' not in session:
        return redirect('/login')  # Redirect to login if not authenticated

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        forumDB.insert_one({'title': title, 'content': content, 'comments': []})
        return redirect(url_for('forum'))
    return render_template('new_topic.html')

@app.route('/forum/<topic_id>', methods=['GET', 'POST'])
def view_topic(topic_id):
    """API for viewing a specific forum topic"""
    intializeDB()
    topic = forumDB.find_one({'_id': ObjectId(topic_id)})
    
    if request.method == 'POST':
        # Check if 'username' is in session before allowing comments
        if 'username' not in session:
            return redirect('/login')  # Redirect to login if not authenticated
            
        comment = request.form['comment']
        forumDB.update_one(
            {'_id': ObjectId(topic_id)},
            {'$push': {'comments': comment}}
        )
        return redirect(url_for('view_topic', topic_id=topic_id))
    
    return render_template('view_topic.html', topic=topic)


# view all
@app.route('/myjobs')
def myjobs():
    """An API for the user to view all the reviews created by them"""
    intializeDB()

    # Check if 'username' is in session
    if 'username' not in session:
        return redirect('/login')  # Redirect to login if not authenticated

    entries = get_my_jobs(session['username'])
    page, per_page, offset = get_page_args(
        page_parameter="page", per_page_parameter="per_page")
    total = len(entries)

    if not page or not per_page:
        offset = 0
        per_page = 10
        pagination_entries = entries[offset: offset + per_page]
    else:
        pagination_entries = entries[offset: offset + per_page]

    pagination = Pagination(page=page, per_page=per_page,
                            total=total, css_framework='bootstrap4')

    return render_template('myjobs.html', entries=pagination_entries, page=page, per_page=per_page, pagination=pagination)


#Get the top jobs
@app.route('/top_jobs')
def top_jobs():
    intializeDB()
    jobs = get_all_jobs()
    # Sort jobs by sum of recommendation and rating
    topJobs = sorted(
        jobs, 
        key=lambda job: job.get("recommendation", 0) + job.get("rating", 0), 
        reverse=True
    )[:10]
    return render_template('top_jobs.html', jobs=topJobs)

# search
@app.route('/pageContentPost', methods=['POST'])
def page_content_post():
    """An API for the user to view specific reviews depending on the job title"""
    intializeDB()
    if request.method == 'POST':
        form = request.form
        search_title = form.get('search')
        print("search is", search_title)
        filter_entries = get_all_jobs()
        if search_title.strip() == '':
            entries = get_all_jobs()
        else:
            print("s entered")
            entries = process_jobs(jobsDB.find(
                {"title": "/"+search_title+"/"}))
        dept_filter_entries = jobsDB.distinct("department")
        location_filter_entries = jobsDB.distinct("locations")
        title_filter_entries = jobsDB.distinct("title")
        company_filter_entries = jobsDB.distinct("company")

        dept_filter_title = form.getlist("dept_filter")
        location_filter_title = form.getlist("location_filter")
        title_filter_title = form.getlist("title_filter")
        company_filter_title = form.getlist("company_filter")

        if company_filter_title and dept_filter_title:
            print("dept filter is", dept_filter_title)
            entries = process_jobs(jobsDB.find({"company":  {
                                   "$in": company_filter_title}, "department":  {"$in": dept_filter_title}}))
        elif dept_filter_title and not company_filter_title:
            print("location filter is", dept_filter_title)
            entries = process_jobs(jobsDB.find(
                {"department":  {"$in": dept_filter_title}}))
        elif company_filter_title and not dept_filter_title:
            print("company filter is", company_filter_title)
            entries = process_jobs(jobsDB.find(
                {"company":  {"$in": company_filter_title}}))
        page, per_page, offset = get_page_args(
            page_parameter="page", per_page_parameter="per_page")
        total = len(entries)

        if not page or not per_page:
            offset = 0
            per_page = 10
            pagination_entries = entries[offset: offset+per_page]
        else:
            pagination_entries = entries[offset: offset+per_page]
            # print("ELSE!!!")

        pagination = Pagination(page=page, per_page=per_page,
                                total=total, css_framework='bootstrap4')

        return render_template('page_content.html', entries=pagination_entries,
                               dept_filter_entries=dept_filter_entries,
                               location_filter_entries=location_filter_entries,
                               company_filter_entries=company_filter_entries, page=page, per_page=per_page, pagination=pagination)


@app.route('/')
@app.route('/home')
def home():
    """An API for the user to be able to access the homepage through the navbar"""
    intializeDB()
    return render_template('index.html')


@app.route('/add', methods=['POST'])
def add():
    """An API to help users add their reviews and store it in the database"""
    
    
    intializeDB()
    user = usersDb.find_one({"username": session['username']})
    if user == None:
        flash('User not found. Please log in again.', 'error')
        return redirect('/login')  # Redirect to a login page or wherever appropriate

    reviews = user['reviews']

    if request.method == 'POST':
        form = request.form        
        # Validate required fields
        required_fields = ['job_title', 'company', 'locations', 'job_description', 'department', 'hourly_pay', 'benefits', 'review', 'rating', 'recommendation']
        missing_fields = [field for field in required_fields if not form.get(field)]

        if missing_fields:
            flash('Please fill out the fields.', 'error')

        job = {
            "_id": form.get('job_title') + "_" + form.get('company') + "_" + form.get('locations'),
            "title": form.get('job_title'),
            "company": form.get('company'),
            "description": form.get('job_description'),
            "locations": form.get('locations'),
            "department": form.get('department'),
            "hourly_pay":   form.get('hourly_pay'),
            "benefits": form.get('benefits'),
            "review": form.get('review'),
            "rating": form.get('rating'),
            "recommendation": form.get('recommendation'),
            "author": session['username'],
            "upvote": 0
        }

        if jobsDB.find_one({'_id': job['_id']}) == None:
            jobsDB.insert_one(job)
            reviews.append(job['_id'])
            usersDb.update_one({"username": session['username']}, {
                               "$set": {"reviews": reviews}})

    return redirect('/')


@app.route('/logout')
def logout():
    """An API to help users logout"""
    session.pop('username', None)
    return redirect('/')


@app.route("/login", methods=["POST", "GET"])
def login():
    """An API to help users login"""
    intializeDB()
    
    # Check if user is already logged in
    if 'username' in session.keys() and session['username']:
        return redirect("/")
    
    if request.method == "POST":
        username = request.form.get("username")
        user = usersDb.find_one({"username": username})
        passw = request.form.get("password")

        # Check if user exists and password matches
        if user and user["password"] == passw:
            session["username"] = username
            return redirect("/")
        else:
            flash("Invalid username or password.","danger")  # Provide specific error message
            return redirect("/login")  # Redirect back to the login page

    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """An API to help users signup"""
    intializeDB()
    
    if 'username' in session.keys() and session['username']:
        print("User ", session['username'], " already logged in")
        return redirect("/")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")  # Get the confirmed password

        user = usersDb.find_one({"username": username})

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!","danger")  # Show an error message
            return render_template("signup.html")

        # New user
        if not user:
            user = {
                "username": username,
                "password": password,  # Consider hashing this password before storing
                "reviews": list()
            }
            usersDb.insert_one(user)
            session["username"] = username  # Log in the user after signing up
            return redirect("/")

        flash("Username already exists! please login or use different username","danger")  # Show an error message if username is taken
        return render_template("signup.html")

    return render_template("signup.html")


@app.route('/view/<id>')
def view(id):
    """An API to help view review information"""
    intializeDB()
    jobReview = jobsDB.find_one({"_id": id})
    jobReview['id'] = jobReview.pop('_id')
    return render_template("view.html", entry=jobReview)


@app.route('/upvote/<id>')
def upvote(id):
    """An API to update upvote information"""
    intializeDB()
    jobReview = jobsDB.find_one({"_id": id})
    upvote = jobReview['upvote']
    upvote += 1
    jobsDB.update_one({"_id": id}, {"$set": {"upvote": upvote}})
    return redirect("/view/"+id)


@app.route('/downvote/<id>')
def downvote(id):
    """An API to update upvote information"""
    intializeDB()
    jobReview = jobsDB.find_one({"_id": id})
    upvote = jobReview['upvote']
    upvote -= 1
    jobsDB.update_one({"_id": id}, {"$set": {"upvote": upvote}})
    return redirect("/view/"+id)


@app.route('/delete/<id>')
def delete(id):
    """An API to help delete a review"""
    intializeDB()
    user = usersDb.find_one({"username": session['username']})
    if user == None:
        pass

    reviews = user['reviews']
    reviews.remove(id)
    usersDb.update_one({"username": session['username']}, {
                       "$set": {"reviews": reviews}})

    jobsDB.delete_one({"_id": id})
    return redirect("/myjobs")
