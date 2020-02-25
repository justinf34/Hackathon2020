# Calgaryhacks 2020 
YouTube playlist compiler for University of Calgary courses 

### Overview
This project was made for UofC Calgaryhacks 2020 hosted by CSUS (Computer science undergrad society).

Website: https://calgaryhacks-2020.devpost.com/

Hackathon Themes
1. Calgary related game
2. Assisted living 
3. University experience

We decided to improve the University experience.
Our project grabs the public univeristy calendar and parse the keywords to identifty what is important in the course, then it use the youtube api get the relevent search requests then it's send to a website as a collection of playlists for each topic.

## Installation 

Clone this repo 

Dependencies
- Install Python 3+ 
- Install Pip
- Install VirtualEnv
- Install google api cloud python libaries 

How to run
1) Change to flask-backend folder
2) flask run app.py 

## Build With 

- Frontend:HTML,CSS, Bootstrap, Jquery 
- Backend: Python/Flask , Firestore (database)
- Other: Youtube API, beautifulsoup (python parser)
 
## API Usage

The API keys on this repo have been removed/expired, therefore you must generate new keys if you would like to see it's functioning.

YoutubeAPI https://developers.google.com/explorer-help/guides/code_samples#python
Firestore: https://firebase.google.com/docs/firestore/use-rest-api

Just find the varibales called DEVELOPER_KEY OR API_KEY and add a new key.


## Authors

- Justin Flores github.com/justinf34
- Tony Wong github.com/hitony7
- Alexander Chao https://github.com/AlexanderChao14
- Gurvir Dehal https://github.com/GurvirDehal
- Bryan Huynh https://github.com/BryanHuynh

##### Future
- Imporve parsing with ML
- Improve rating system
- Improve frontend




