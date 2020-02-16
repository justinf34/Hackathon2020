from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

app = Flask(__name__)

# Connecting to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://josh_prowse:Prowse123@hackathon-2020.cfwfxw7xy4fu.us-east-2.rds.amazonaws.com/yt_vid_course_compiler'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/hi')
def temp():
    return "search"


if __name__ == '__main__':
    app.run(debug=True)
