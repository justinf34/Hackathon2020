from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
#from parser import get_key_words
from youtubeapi import youtube_searchURL
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
            video_ids = threepart[0]
            titles = threepart[1]
            descs = threepart[2]
            y = {
                'keyword': word,
                'videos': video_ids,
                'title': titles,
                'desc' : descs
            }
            returnJSON.append(y)
            for i in range(len(video_ids)):
                data= {
                    'title': titles[i],
                    'desc' : descs[i]
                }
                if word:
                    course_ref.document(course_name).set(fake_data)
                    course_ref.document(course_name).collection(
                        u'Keywords').document(word).set(fake_data)
                    course_ref.document(course_name).collection(u'Keywords').document(
                        word).collection(u'Videos').document(ids).set(data)
        print('NOT IN FIREBASE')

    else:
        course = course_ref.document(course_name)
        keywords = course.collection(u'Keywords').stream()

        for keyword in keywords:
            vid_ids = []
            vid_title = [] 
            vid_desc = {}
            vids = course.collection(u'Keywords').document(
                keyword.id).collection(u'Videos').stream()
            for vid in vids:
                vid_ids.append(vid.id)
                vid_title.append(vid.title)
                vid_desc.append(vid.desc)
            y = {
                'keyword': keyword.id,
                'videos': vid_ids,
                'title' : vid_title,
                'desc' : vid_desc
            }
            returnJSON.append(y)
        print('IN FIREBASE')
    print(returnJSON)
    result = {
        'array' : returnJSON
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

import sys
import requests
from bs4 import BeautifulSoup



def get_key_words(course_name, course_code):
    def get_course_link(course_name):
        url = "https://www.ucalgary.ca/pubs/calendar/current/course-desc-main.html"
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'lxml')
        soup.prettify()
        link_text_tags = soup.find_all('a', {'class' : 'link-text'})

        def get_course():
            for tag in link_text_tags:
                inner_text = tag.text
                if (course_name in inner_text):
                    return tag.get('href')

        course_link = "https://www.ucalgary.ca/pubs/calendar/current/" + get_course()
        return course_link

    def get_desc(course_link, course_code):
        r = requests.get(course_link).text
        soup = BeautifulSoup(r, 'lxml')
        soup.prettify()
        num_links = soup.find_all('a', {'class' : 'link-text'})
        
        def get_number():
            for tag in num_links:
                if (course_code in tag.text):
                    return tag.get('href').split('#')[1]
        number = get_number()
        parent = soup.find('a', {'name' : number}).parent
        desc = parent.find('span', {'class' : 'course-desc'}).text
        # print(desc)
        return desc

    def string_contains(str1,str2):
        lst1 = str1.split(' ')
        lst2 = str2.split(' ')

        if len(lst1) <= len(lst2):
            return lst1 == lst2[:len(lst1)]

        return False

    common_pun = [",", ".", ";", ":"]
    common_words = ["the", "to", "of", "and", " a ", "in", "that", "for", "it", "on", "with", "as", "do", "at", "this", "by", "from", "an", "all", "there", "their", "what"]
    def remove_word(desc, wordIndex):
        if (wordIndex < 0):
            return desc
        if (string_contains(common_words[wordIndex], desc)):
            return remove_word(desc.replace(common_words[wordIndex],''), wordIndex - 1)
        else: 
            return remove_word(desc, wordIndex - 1)
        

    def remove_pun(desc, punIndex):
        if(punIndex < 0):
            return desc
        arr = []
        for d in desc:
            for lol in d:
                returnValue = lol.split(common_pun[punIndex])
                arr.append(returnValue)

        return remove_pun(arr, punIndex - 1)

    try:
        description = get_desc(get_course_link(course_name), course_code)
        # d2 = remove_word(description, len(common_words) - 1) # doesn't work rn
        d3 = remove_pun([[description]], len(common_pun) - 1)
        d4 = []
        for i in d3:
            for j in i:
                if j:
                    d4.append(j.strip())
        return d4
    except Exception as e: 
        print(e)
        return -1 