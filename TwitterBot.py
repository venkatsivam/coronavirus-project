import tweepy
import sys

consumer_key = 'XXXX'
consumer_secret = 'XXXX'
access_token = 'XXXX'
access_token_secret = 'XXXX'

def upload_media(url,status_val):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    # api.update_status('hi')
    media = api.media_upload(url)
    # print(media)
    post_result = api.update_status(status=status_val, media_ids=[media.media_id])
    print("success!!")
    return '0'