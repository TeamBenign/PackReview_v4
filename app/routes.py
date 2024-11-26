"""
This module implements a Flask-based web application that handles
user authentication, job review submissions,
forum discussions, and pagination of content. It provides the
following functionality:

- User Authentication: Users can log in, sign up, and log out.
- Job Reviews: Users can add, view, and filter job reviews, with reviews
being stored in a MongoDB database.
- Forums: Users can create and participate in discussions on different
topics in a forum section.
- Pagination: Displays job reviews and forum topics in a paginated manner,
 using Flask-Paginate.
- Database Handling: The application uses MongoDB to manage job reviews, user
 data, and forum topics, with separate
  collections for each (Jobs, Users, Forum).
- Search and Filter: The job reviews can be filtered by department, location,
and company.
- Top Jobs: Provides a view of the top jobs sorted by user ratings and recommendations.
"""
from collections import Counter
from pymongo.errors import PyMongoError
from datetime import datetime
from flask import render_template, request, redirect, session, flash, url_for, jsonify
from flask_paginate import Pagination, get_page_args
from bson import ObjectId
from app import app, DB
from utils import get_db
import bcrypt

JOBS_DB = None
USERS_DB = None
FORUM_DB = None
DB = None
IS_TEST = False


def set_test(test):
    """A method to set tests"""
    global IS_TEST
    IS_TEST = test
    return IS_TEST


def intialize_db():
    """A method to initialize database"""
    global JOBS_DB, DB, USERS_DB, FORUM_DB
    DB = get_db(IS_TEST)
    USERS_DB = DB.Users
    JOBS_DB = DB.Jobs
    FORUM_DB = DB.Forum
    return JOBS_DB, DB, USERS_DB, FORUM_DB


def process_jobs(job_list):
    """A method to process all jobs"""
    processed = []
    for job in job_list:
        job['id'] = job.pop('_id')
        processed.append(job)
    return processed


def get_all_jobs():
    """A method to get all jobs for required user"""
    all_jobs = list(JOBS_DB.find())
    return process_jobs(all_jobs)

def get_all_users():
    """A method to get all jobs for required user"""
    all_users = list(USERS_DB.find())
    return process_jobs(all_users)


def get_my_jobs(username):
    """A method to get all jobs for required user"""
    intialize_db()
    user = USERS_DB.find_one({"username": username})
    if user is None:
        pass

    reviews = user['reviews']
    return process_jobs(JOBS_DB.find({"_id": {'$in': reviews}}))

# create job review


@app.route('/review')
def review():
    """
    An API for the user review page, which helps the user to add reviews
    """
    intialize_db()
    if 'username' not in session or not session['username']:
        flash('Please log in first to add a review.', "danger")
        return redirect('/login')
    # if not ('username' in session.keys() and session['username']):
    #     return redirect("/")
    # entries = get_all_jobs()
    return render_template('review-page.html', entry='')


# view all
@app.route('/pageContent')
def page_content():
    """An API for the user to view all the reviews entered"""
    intialize_db()
    entries = get_all_jobs()
    dept_filter_entries = JOBS_DB.distinct("department")
    location_filter_entries = JOBS_DB.distinct("locations")
    # title_filter_entries = JOBS_DB.distinct("title")
    company_filter_entries = JOBS_DB.distinct("company")

    # pagination

    # print(entries)
    page, per_page, offset = get_page_args(
        page_parameter="page", per_page_parameter="per_page")
    total = len(entries)

    if not page or not per_page:
        offset = 0
        per_page = 10
        pagination_entries = entries[offset: offset + per_page]
    else:
        pagination_entries = entries[offset: offset + per_page]
        # print("ELSE!!!")

    pagination = Pagination(page=page, per_page=per_page,
                            total=total, css_framework='bootstrap4')

    return render_template('page_content.html', entries=pagination_entries, page=page,
                           per_page=per_page, pagination=pagination,
                           dept_filter_entries=dept_filter_entries,
                           location_filter_entries=location_filter_entries,
                           company_filter_entries=company_filter_entries)
def getCurrentTime():
    """A method to get current time"""
    return datetime.now().replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S")

@app.route('/forum/add_comment', methods=['POST'])
def add_comment():
    """API for creating a new forum comment of a specific topic"""
    intialize_db()
    # Check if 'username' is in session
    if 'username' not in session:
        return redirect('/login')  # Redirect to login if not authenticated

    if request.method == 'POST':
        data = request.json
        topicId, content = data['topicId'], data['content']
        try:
            FORUM_DB.update_one(
                {'_id': ObjectId(topicId)},
                {'$push': {
                    'comments': {'_cid': str(ObjectId()),'commenter': session['username'], 
                                 'content': content, 'likes': [], 'dislikes': [], 
                                 'timestamp': getCurrentTime()}
                        }
                }
            )
            comment = FORUM_DB.find_one({'_id': ObjectId(topicId)})['comments'][-1]
            comment['commenter_badge'] = get_badge(comment['commenter'])
            comment['comment_likes'] = len(comment['likes'])
            comment['comment_dislikes'] = len(comment['dislikes'])
            comment['timestamp'] = datetime.strptime(
                                    comment['timestamp'],
                                    "%Y-%m-%d %H:%M:%S").strftime("%A, %B %d, %Y, %I:%M %p")
            return jsonify({'status': 'success', 'data': comment})
        except Exception as e:
            return jsonify({'error': str(e)})

@app.route('/forum/update_reaction', methods=['POST'])
def update_reaction():
    """API for creating a new forum topic"""
    intialize_db()
    # Check if 'username' is in session
    if 'username' not in session:
        return redirect('/login')  # Redirect to login if not authenticated

    if request.method == 'POST':
        data = request.json
        topicId, commentId = data['topicId'], data['commentId']
        discussionType, reactionType = data['discussionType'], data['reactionType']
        topic = FORUM_DB.find_one({'_id': ObjectId(topicId)})
        if discussionType == 'topic':
            if session['username'] in topic['likes'] or session['username'] in topic['dislikes']:
                return jsonify({'error': 'You have already reacted this topic'})

            if reactionType == 'like':
                FORUM_DB.update_one(
                    {'_id': ObjectId(topicId)},
                    {'$push': {'likes': session['username']}}
                )
                res = FORUM_DB.find_one({'_id': ObjectId(topicId)})
                cnt = len(res['likes'])
                return jsonify({'status': 'success', 'data': cnt})
            else:
                FORUM_DB.update_one(
                    {'_id': ObjectId(topicId)},
                    {'$push': {'dislikes': session['username']}}
                )
                res = FORUM_DB.find_one({'_id': ObjectId(topicId)})
                cnt = len(res['dislikes'])
                return jsonify({'status': 'success', 'data': cnt})
        else:
            comments = topic['comments']

            comment = [c for c in comments if c['_cid'] == commentId][0]
            if (session['username'] in comment['likes'] or
                session['username'] in comment['dislikes']):
                return jsonify({'error': 'You have already reacted this comment'})
            if reactionType == 'like':
                FORUM_DB.update_one(
                    {'_id': ObjectId(topicId),'comments._cid': commentId},
                    {'$addToSet': {'comments.$.likes': session['username']}}
                )
                topic = FORUM_DB.find_one({'_id': ObjectId(topicId)})
                comments = topic['comments']
                comment = [c for c in comments if c['_cid'] == commentId][0]
                cnt = len(comment['likes'])
                return jsonify({'status': 'success', 'data': cnt})
            else:
                FORUM_DB.update_one(
                    {'_id': ObjectId(topicId),'comments._cid': commentId},
                    {'$addToSet': {'comments.$.dislikes': session['username']}}
                )
                topic = FORUM_DB.find_one({'_id': ObjectId(topicId)})
                comments = topic['comments']
                comment = [c for c in comments if c['_cid'] == commentId][0]
                cnt = len(comment['dislikes'])
                return jsonify({'status': 'success', 'data': cnt})

    return jsonify({'error': 'Invalid request'})

def get_badge(username):
    """A method to get badge"""
    Badges = ['NewBie', 'Intermediate', 'Advanced', 'Expert']
    user = USERS_DB.find_one({"username": username})
    if user is None:
        return "Anonymous"
    total_reviews = len(user['reviews'])
    if total_reviews < 5:
        return Badges[0]
    elif total_reviews < 10:
        return Badges[1]
    elif total_reviews < 15:
        return Badges[2]
    return Badges[3]

def getRefinedTopics(topics):
    """A method to refine topics"""
    for topic in topics:
        # Add badge for the author
        topic['author_badge'] = get_badge(topic['author'])
        topic['timestamp'] = datetime.strptime(topic['timestamp'],
                            "%Y-%m-%d %H:%M:%S").strftime("%A, %B %d, %Y, %I:%M %p")
        topic['topics_likes'] = len(topic['likes'])
        topic['topics_dislikes'] = len(topic['dislikes'])

        # Add badges for likes and dislikes
        topic['likes'] = [{'user': user, 'badge': get_badge(user)} for user in topic['likes']]
        topic['dislikes'] = [{'user': user, 'badge': get_badge(user)} for user in topic['dislikes']]

        # Process comments
        for comment in topic['comments']:
            comment['commenter_badge'] = get_badge(comment['commenter'])
            comment['timestamp'] = datetime.strptime(comment['timestamp'],
                                    "%Y-%m-%d %H:%M:%S").strftime("%A, %B %d, %Y, %I:%M %p")
            comment['likes'] = [{'user': user, 'badge': get_badge(user)} for user in comment['likes']]
            comment['dislikes'] = [{'user': user, 'badge': get_badge(user)} for user in comment['dislikes']]
            comment['comment_likes'] = len(comment['likes'])
            comment['comment_dislikes'] = len(comment['dislikes'])
    return topics

@app.route('/forum')
def forum():
    """API for viewing all forum topics"""
    intialize_db()
    topics = list(FORUM_DB.find())
    res = getRefinedTopics(topics)
    return render_template('forum.html', topics=res)


@app.route('/forum/new_topic', methods=['POST'])
def new_topic():
    """API for creating a new forum topic"""
    intialize_db()
    # Check if 'username' is in session
    if 'username' not in session:
        return redirect('/login')  # Redirect to login if not authenticated

    title = request.form['topic_title']
    content = request.form['topic_description']
    creator = session['username']  # Get the username of the logged-in user
    FORUM_DB.insert_one(
        {'title': title, 'content': content, 'comments': [], 'author': creator,
        'timestamp': getCurrentTime(), 'likes': [], 'dislikes': []
        }
    )
    return redirect(url_for('forum'))

@app.route('/forum/<topic_id>', methods=['GET', 'POST'])
def view_topic(topic_id):
    """API for viewing a specific forum topic"""
    intialize_db()
    topic = FORUM_DB.find_one({'_id': ObjectId(topic_id)})

    if request.method == 'POST':
        # Check if 'username' is in session before allowing comments
        if 'username' not in session:
            return redirect('/login')  # Redirect to login if not authenticated

        comment = request.form['comment']
        username = session['username']
        FORUM_DB.update_one(
            {'_id': ObjectId(topic_id)},
            {'$push': {'comments': {'username': username, 'comment': comment}}}
        )
        return redirect(url_for('view_topic', topic_id=topic_id))

    return render_template('view_topic.html', topic=topic)

@app.route('/forum/<topic_id>/upvote_post', methods=['POST'])
def upvote_post(topic_id):
    """API for upvoting a specific forum topic"""
    intialize_db()
    # Check if 'username' is in session before allowing vote
    if 'username' not in session:
        return redirect('/login')

    # Increment the upvote count
    FORUM_DB.update_one(
        {'_id': ObjectId(topic_id)},
        {'$inc': {'upvotes': 1}}
    )
    return redirect(url_for('forum'))


@app.route('/forum/<topic_id>/downvote_post', methods=['POST'])
def downvote_post(topic_id):
    """API for downvoting a specific forum topic"""
    intialize_db()
    # Check if 'username' is in session before allowing vote
    if 'username' not in session:
        return redirect('/login')

    # Increment the downvote count
    FORUM_DB.update_one(
        {'_id': ObjectId(topic_id)},
        {'$inc': {'downvotes': 1}}
    )
    return redirect(url_for('forum'))


# view all
@app.route('/myjobs')
def myjobs():
    """An API for the user to view all the reviews created by them"""
    intialize_db()

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

    return render_template('myjobs.html', entries=pagination_entries, page=page,
                           per_page=per_page, pagination=pagination)


# Get the top jobs
@app.route('/top_jobs')
def top_jobs():
    """An API to get Top Jobs"""
    intialize_db()
    jobs = get_all_jobs()
    # Sort jobs by sum of recommendation and rating
    top_job = sorted(
        jobs,
        key=lambda job: int(job.get("recommendation", 0)
                            or 0) + int(job.get("rating", 0) or 0),
        reverse=True
    )[:10]
    return render_template('top_jobs.html', jobs=top_job)


def get_avg_sal_titles_by_locations(jobs):
    """A method to get average salary by title and location"""
    locations = list({job['locations'] for job in jobs})
    titles = list({job['title'] for job in jobs})

    # Preparing the data
    average_pay = {title: [0] * len(locations) for title in titles}
    count = {title: [0] * len(locations) for title in titles}

    for job in jobs:
        location_idx = locations.index(job['locations'])
        title = job['title']
        average_pay[title][location_idx] += int(job['hourly_pay'])
        count[title][location_idx] += 1

    for title in titles:
        for i in range(len(locations)):
            if count[title][i] > 0:
                average_pay[title][i] /= count[title][i]
    # Convert the data to JSON for the JavaScript to use
    data = {
        "locations": locations,
        "titles": titles,
        "average_pay": average_pay
    }
    return data
def get_web_statistics(jobs, users):
    """Extract web statistics from jobs and users."""
    titles = [job['title'] for job in jobs]
    locations = [job['locations'] for job in jobs]
    ratings = [float(job['rating']) for job in jobs if 'rating' in job]

    web_stat = {
        "total_jobs": len(jobs),
        "total_companies": len(Counter(job['company'] for job in jobs)),
        "total_titles": len(Counter(titles)),
        "total_locations": len(Counter(locations)),
        'avg_ratings': sum(ratings) / len(ratings) if ratings else 0,
        'total_users': len(users)
    }
    return web_stat

def extract_location_data(jobs):
    """Extract job location data for plotting."""
    locations = [job['locations'] for job in jobs]
    location_counts = Counter(locations)
    return list(location_counts.keys()), list(location_counts.values())

def extract_company_data(jobs):
    """Extract company data for plotting."""
    companies = [job['company'] for job in jobs]
    company_counts = Counter(companies)
    return list(company_counts.keys()), list(company_counts.values())

def extract_hourly_pay_data(jobs):
    """Extract hourly pay details."""
    titles = [job['title'] for job in jobs]
    hourly_pays = [job['hourly_pay'] for job in jobs]
    return titles, hourly_pays

def extract_rating_data(jobs):
    """Extract job rating details."""
    ratings = [job['rating'] for job in jobs]
    rating_counts = Counter(ratings)
    return ratings, rating_counts
# dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """An API to get Top Jobs"""
    intialize_db()
    jobs = get_all_jobs()
    users = get_all_users()

    # Extract web statistics
    web_stat = get_web_statistics(jobs, users)

    # Extract data for charts
    cities, job_counts = extract_location_data(jobs)
    company_names, company_job_counts = extract_company_data(jobs)
    titles, hourly_pays = extract_hourly_pay_data(jobs)
    ratings, rating_counts = extract_rating_data(jobs)

    # Extract additional data if needed
    avg_sal_titles_by_locations = get_avg_sal_titles_by_locations(jobs)

    return render_template('dashboard.html',
                           web_stat=web_stat,
                           data=avg_sal_titles_by_locations,
                           cities=cities,
                           job_counts=job_counts,
                           companies=company_names,
                           company_job_counts=company_job_counts,
                           titles=titles,
                           hourly_pays=hourly_pays,
                           ratings=ratings,
                           rating_counts=rating_counts)

@app.route('/pageContentPost', methods=['POST'])
def page_content_post():
    """An API for the user to view specific reviews depending on the job title"""
    intialize_db()
    if request.method == 'POST':
        form = request.form
        search_title = form.get('search')
        print("search is", search_title)
        # filter_entries = get_all_jobs()
        if search_title.strip() == '':
            entries = get_all_jobs()
        else:
            print("s entered")
            entries = process_jobs(JOBS_DB.find(
                {"title": "/" + search_title + "/"}))
        dept_filter_entries = JOBS_DB.distinct("department")
        location_filter_entries = JOBS_DB.distinct("locations")
        # title_filter_entries = JOBS_DB.distinct("title")
        company_filter_entries = JOBS_DB.distinct("company")

        dept_filter_title = form.getlist("dept_filter")
        # location_filter_title = form.getlist("location_filter")
        # title_filter_title = form.getlist("title_filter")
        company_filter_title = form.getlist("company_filter")

        if company_filter_title and dept_filter_title:
            print("dept filter is", dept_filter_title)
            entries = process_jobs(JOBS_DB.find({"company": {
                "$in": company_filter_title}, "department": {"$in": dept_filter_title}}))
        elif dept_filter_title and not company_filter_title:
            print("location filter is", dept_filter_title)
            entries = process_jobs(JOBS_DB.find(
                {"department": {"$in": dept_filter_title}}))
        elif company_filter_title and not dept_filter_title:
            print("company filter is", company_filter_title)
            entries = process_jobs(JOBS_DB.find(
                {"company": {"$in": company_filter_title}}))
        page, per_page, offset = get_page_args(
            page_parameter="page", per_page_parameter="per_page")
        total = len(entries)

        if not page or not per_page:
            offset = 0
            per_page = 10
            pagination_entries = entries[offset: offset + per_page]
        else:
            pagination_entries = entries[offset: offset + per_page]
            # print("ELSE!!!")

        pagination = Pagination(page=page, per_page=per_page,
                                total=total, css_framework='bootstrap4')

        return render_template('page_content.html', entries=pagination_entries,
                               dept_filter_entries=dept_filter_entries,
                               location_filter_entries=location_filter_entries,
                               company_filter_entries=company_filter_entries, page=page,
                               per_page=per_page, pagination=pagination)
    return jsonify('')


@app.route('/')
@app.route('/home')
def home():
    """An API for the user to be able to access the homepage through the navbar"""
    intialize_db()
    return render_template('index.html')


@app.route('/add', methods=['POST'])
def add():
    """An API to help users add their reviews and store it in the database"""

    intialize_db()
    user = USERS_DB.find_one({"username": session['username']})
    if user is None:
        flash('User not found. Please log in again.', 'error')
        # Redirect to a login page or wherever appropriate
        return redirect('/login')

    reviews = user['reviews']

    if request.method == 'POST':
        form = request.form
        # Validate required fields
        required_fields = ['job_title', 'company', 'locations',
                           'job_description', 'department', 'hourly_pay',
                           'benefits', 'review', 'rating', 'recommendation']
        missing_fields = [
            field for field in required_fields if not form.get(field)]

        if missing_fields:
            flash('Please fill out the fields.', 'error')

        job = {
            "_id": form.get('job_title') + "_" + form.get('company') + "_" + form.get('locations')+ "_" + session['username'] + "_" + form.get('department'),
            "title": form.get('job_title'),
            "company": form.get('company'),
            "description": form.get('job_description'),
            "locations": form.get('locations'),
            "department": form.get('department'),
            "hourly_pay": form.get('hourly_pay'),
            "benefits": form.get('benefits'),
            "review": form.get('review'),
            "rating": form.get('rating'),
            "recommendation": form.get('recommendation'),
            "author": session['username'],
            "upvote": 0
        }

        if JOBS_DB.find_one({'_id': job['_id']}) is None:
            JOBS_DB.insert_one(job)
            reviews.append(job['_id'])
            USERS_DB.update_one({"username": session['username']}, {
                "$set": {"reviews": reviews}})
        else:
            JOBS_DB.update_one(
                {'_id': job['_id']},
                {"$set": job}  # Update the job details with the new values
            )

        if job['_id'] not in reviews:
            reviews.append(job['_id'])
            USERS_DB.update_one({"username": session['username']}, {
                                "$set": {"reviews": reviews}})

    return redirect("/myjobs")


@app.route('/logout')
def logout():
    """An API to help users logout"""
    session.pop('username', None)
    return redirect('/')


@app.route("/login", methods=["POST", "GET"])
def login():
    """An API to help users login"""
    intialize_db()

    if 'username' in session.keys() and session['username']:
        return redirect("/")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = USERS_DB.find_one({"username": username})

        # Verify the user exists and the password matches
        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            session["username"] = username
            return redirect("/")

        flash("Invalid username or password.", "danger")
        return redirect("/login")

    return render_template("login.html")




@app.route("/signup", methods=["POST", "GET"])
def signup():
    """An API to help users signup"""
    intialize_db()

    if 'username' in session.keys() and session['username']:
        print("User ", session['username'], " already logged in")
        return redirect("/")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user = USERS_DB.find_one({"username": username})

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return render_template("signup.html")

        # Check if username already exists
        if user:
            flash("Username already exists! Please login or use a different username.", "danger")
            return render_template("signup.html")

        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create a new user document
        user = {
            "username": username,
            "password": hashed_password,  # Store the hashed password
            "reviews": []
        }
        USERS_DB.insert_one(user)

        session["username"] = username  # Log in the user after signing up
        return redirect("/")

    return render_template("signup.html")






@app.route('/view/<view_id>')
def view(view_id):
    """An API to help view review information"""
    intialize_db()
    job_review = JOBS_DB.find_one({"_id": view_id})
    if job_review is None:
        return "Review not found", 404
    job_review['id'] = job_review.pop('_id')
    return render_template("view.html", entry=job_review)


@app.route('/upvote/<upvote_id>')
def upvote(upvote_id):
    """An API to update upvote information"""
    intialize_db()
    job_review = JOBS_DB.find_one({"_id": upvote_id})
    up_vote = job_review['upvote']
    up_vote += 1
    JOBS_DB.update_one({"_id": upvote_id}, {"$set": {"upvote": up_vote}})
    return redirect("/view/" + upvote_id)


@app.route('/downvote/<downvote_id>')
def downvote(downvote_id):
    """An API to update upvote information"""
    intialize_db()
    job_review = JOBS_DB.find_one({"_id": downvote_id})
    down_vote = job_review['upvote']
    down_vote -= 1
    JOBS_DB.update_one({"_id": downvote_id}, {"$set": {"upvote": down_vote}})
    return redirect("/view/" + downvote_id)


@app.route('/delete/<delete_id>')
def delete(delete_id):
    """An API to help delete a review"""
    intialize_db()
    user = USERS_DB.find_one({"username": session['username']})
    if user is None:
        pass

    reviews = user['reviews']
    reviews.remove(delete_id)
    USERS_DB.update_one({"username": session['username']}, {
        "$set": {"reviews": reviews}})

    res = JOBS_DB.delete_one({"_id": delete_id})
    if res.deleted_count == 0:
        return "Review not found", 404
    return redirect("/myjobs")


@app.route('/api/getUser')
def get_user():
    """Retrieve the username from the session if available."""
    try:
        if 'username' in session and session['username']:
            return jsonify(session['username'])
        return jsonify('')
    except KeyError as e:
        print("KeyError: ", e)
        return jsonify(''), 500
    except PyMongoError as e:
        print("Error: ", e)
        return jsonify(''), 500


@app.route('/api/updateReview')
def update_review():
    """Update a job review by its ID."""
    try:
        review_id = request.args.get('id')
        intialize_db()
        job_review = JOBS_DB.find_one({"_id": review_id})
        if job_review:
            job_review['id'] = job_review.pop('_id')
            return render_template("review-page.html", entry=job_review)
        return "Review not found", 404
    except KeyError as e:
        print("KeyError: ", e)
        return "Invalid ID provided", 400
    except PyMongoError as e:
        print("Error: ", e)
        return "An error occurred", 500
