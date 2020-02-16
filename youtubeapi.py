# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
# Edited by tony Wong for hack 2020

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery 
import googleapiclient.errors

import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

api_key = "AIzaSyAOW_wS_ihdJubtncGByfmJ1S-Zk5Knr6w"




    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

DEVELOPER_KEY = 'AIzaSyAOW_wS_ihdJubtncGByfmJ1S-Zk5Knr6w'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search():
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

    # Get credentials and create an API client

    request = youtube.search().list(
        part="snippet",
        q="naruto",                     #change q for keywords of search type
        type="video"
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    youtube_search()

