from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from parser import get_key_words

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

    print(query)

    has_course = course_ref.document(course_name).get()
    has_course = has_course.to_dict()

    data = {
        'rating': 0
    }

    returnJSON = []
    if True:
        words = get_key_words(query[0], query[1])
        for word in words:
            video_ids = youtube_searchURL(word)
            y = json.dumps({
                'keyword': word,
                'videos': video_ids
            })
            returnJSON.append(y)
            print(returnJSON[0])
            for ids in video_ids:
                if word:
                    course_ref.document(course_name).collection(u'Keywords').document(
                        word).collection(u'Videos').document(ids).set(data)

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
    keywords = course.collection(u'Keywords').stream()

    returnJSON = []
    for keyword in keywords:
        vid_ids = []
        vids = course.collection(u'Keywords').document(
            keyword.id).collection(u'Videos').stream()
        for vid in vids:
            vid_ids.append(vid.id)

        y = json.dumps({
            'keyword': keyword.id,
            'videos': vid_ids
        })
        returnJSON.append(y)

    print(returnJSON)

    return "hi"
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
