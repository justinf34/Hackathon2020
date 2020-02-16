from bs4 import BeautifulSoup
import requests
import sys
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from parser import get_key_words
from youtubeapi import youtube_search3
import json
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
    print(has_course)
    data = {
        'rating': 0
    }

    fake_data = {
        'fake': 0
    }

    returnJSON = []
    if has_course is None:
        words = get_key_words(query[0], query[1])
        for word in words:
            #video_ids = youtube_search3(word)
            threepart = youtube_search3(word)
            vid_ids = threepart[0]
            titles = threepart[1]
            descs = threepart[2]
            y = {
                'keyword': word,
                'videos': vid_ids,
                'title': titles,
                'desc': descs
            }
            returnJSON.append(y)
            for i in range(len(vid_ids)):
                data = {
                    'title': titles[i],
                    'desc': descs[i]
                }
                if word:
                    course_ref.document(course_name).set(fake_data)
                    course_ref.document(course_name).collection(
                        u'Keywords').document(word).set(fake_data)
                    course_ref.document(course_name).collection(u'Keywords').document(
                        word).collection(u'Videos').document(vid_ids[i]).set(data)
        print('NOT IN FIREBASE')

    else:
        course = course_ref.document(course_name)
        keywords = course.collection(u'Keywords').stream()

        for keyword in keywords:
            vid_ids = []
            vid_title = []
            vid_desc = []
            vids = course.collection(u'Keywords').document(
                keyword.id).collection(u'Videos').stream()
            for vid in vids:
                vid_ids.append(vid.id)
                temp = vid.to_dict()
                print("HERRRRRREEEEE")

                vid_title.append(temp['title'])
                vid_desc.append(temp['desc'])
            y = {
                'keyword': keyword.id,
                'videos': vid_ids,
                'title': vid_title,
                'desc': vid_desc
            }
            returnJSON.append(y)
        print('IN FIREBASE')
    print(returnJSON)
    result = {
        'array': returnJSON
    }
    return render_template("playlist.html", result=result)


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
