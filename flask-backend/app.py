from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from parser import get_key_words
from youtubeapi import youtube_searchURL
import json

app = Flask(__name__)

# Connecting to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://josh_prowse:Prowse123@hackathon-2020.cfwfxw7xy4fu.us-east-2.rds.amazonaws.com/yt_vid_course_compiler'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/playlist.html')
def temp():
    query = request.args.get('search').split(' ')
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
    return render_template("playlist.html", result=returnJSON)


if __name__ == '__main__':
    app.run(debug=True)