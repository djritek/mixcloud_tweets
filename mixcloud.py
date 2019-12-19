#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import json
import urllib
import requests
from requests_oauthlib import OAuth1Session

from authids import data

def list_get():
    # static urls
    baseurl = 'https://api.mixcloud.com'
    user = data.mixcloud_info()
    cloudcast = 'cloudcasts'

    id_lists = []
    search_result = requests.get(baseurl + '/' + user + '/' + cloudcast + '/')
    search_data = json.loads(search_result.text)
    for keys in search_data['data']:
        id_lists.append(str(keys['key']))
    choiceid = random.choice(id_lists)
    show_result = requests.get(baseurl + choiceid)
    show_data = json.loads(show_result.text)
    show_name = show_data['name']
    show_thumb = show_data['pictures']['large']
    show_url = show_data['url']

    return show_name, show_thumb, show_url


def twitter_post(thumb, message):
    #import for your twitter.com user data from external variables.
    twit_cons_key, twit_cons_secret, twit_access_token, twit_access_secret = data.twitter_auth_info()

    url_media = "https://upload.twitter.com/1.1/media/upload.json"
    url_post = "https://api.twitter.com/1.1/statuses/update.json"

    twitter = OAuth1Session(twit_cons_key, twit_cons_secret, twit_access_token, twit_access_secret)

    # Image upload
    files = {"media" : open(thumb, 'rb')}
    req_media = twitter.post(url_media, files=files)
    if req_media.status_code != 200:
        print("Image upload failed : " + req_media.text)
        exit()
    media_id = json.loads(req_media.text)['media_id']

    # tweet post
    params = {'status': message, "media_ids": [media_id]}
    req_post = twitter.post(url_post, params = params)

    if req_post.status_code != 200:
        print("Tweet post failed. : " + req_post.text)
        exit()


def main():
    show_name, show_thumb, show_url = list_get()
    jp_head = '[My Mixcloud Bot]'
    message = jp_head +  ' : ' + show_name + '  ' + str(show_url)
    print(message)
    imgget = urllib.request.urlopen(show_thumb)
    with open('./mixcloud_sample.jpg', 'wb') as savefile:
        savefile.write(imgget.read())
    twitter_post('./mixcloud_sample.jpg', message)


if __name__ =='__main__':
    main()
