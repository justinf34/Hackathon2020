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
import json


# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

DEVELOPER_KEY = 'AIzaSyBWBoNXGOCFkjMsMzyEBjxUXbu7U-9Ymm8'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Full JSON


def youtube_search(keyword):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Get credentials and create an API client

    request = youtube.search().list(
        part="snippet",
        q=keyword,  # change q for keywords of search type
        type="video"
    )
    response = request.execute()

    return response

# videoID ONLY
# return a list of IDs


def youtube_searchURL(keyword):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Get credentials and create an API client

    request = youtube.search().list(
        part="snippet",
        q=keyword,  # change q for keywords of search type
        type="video",
        maxResults=1
    )
    response = request.execute()

    IDs = []
    # Finds the youtube IDs for the path of the youtube URL
    for search_result in response.get('items', []):
        # print(search_result['id']['videoId'])
        IDs.append((search_result['id']['videoId']))

    return IDs


# Returns Stats of a Video given an VIDEO_ID
""" "statistics": 
    "viewCount"
    "likeCount"
    "dislikeCount"
    "favoriteCount"
    "commentCount" """


def youtube_searchSTAT(VIDEO_ID):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Get credentials and create an API client

    request = youtube.videos().list(
        part="id, statistics",
        id=VIDEO_ID  # VIDEO ID
    )
    response = request.execute()

    return response


if __name__ == "__main__":
    print(youtube_searchURL("naruto"))  # example keyword
    print(youtube_searchSTAT("koY0fIVMS_s"))  # example VideoID
