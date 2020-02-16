from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
# from parser import get_key_words

from firebase_admin import credentials, firestore, initialize_app

from google.cloud import storage, exceptions


app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
course_ref = db.collection('Courses')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/playlist')
def temp():

    course_name = request.args.get('search')
    query = course_name.split(' ')

    has_course = course_ref.document(course_name).get()
    has_course = has_course.to_dict()

    if has_course is None:
        words = get_key_words(query[0], query[1])
        returnJSON = []
        for word in words:
            video_ids = youtube_searchURL(word)
            y = json.dumps({
                'keyword': word,
                'videos': video_ids
            })
            returnJSON.append(y)
            print(returnJSON[0])
    else:
        return render_template("playlist.html", result=returnJSON)


@app.route('/insert')
def insert():
    temp = 'STAT 217'
    # course = course_ref.document(temp).collection(u'Keywords').document(
    #     u'Estimation of population parameters').collection(u'Videos').document(u'FX51BBGoE68').get()
    data = {
        'rating': 0
    }

    vid_id = 'rIud0ekk-sM'

    keyword = 'confidence intervals for means'
    course = course_ref.document(temp)
    course.collection(u'Keywords').document(
        keyword).collection(u'Videos').document(vid_id).set(data)
    return "I added :^)"
    # course_again = course.to_dict()
    # if course_again is None:
    #     # course = course_ref.document(temp).collection(u'Keywords').document(
    #     #     u'Estimation of population parameters').collection(u'Videos').document(u'FX51BBGoE68').get()
    #     print("I FAILED")
    #     return "Failed"

    # else:
    #     print(course_again)
    #     return "Hello"


if __name__ == '__main__':
    app.run(debug=True)


# museums = db.collection_group(u'landmarks')\
#     .where(u'type', u'==', u'museum')
# docs = museums.stream()
# for doc in docs:
#     print(u'{} => {}'.format(doc.id, doc.to_dict()))
