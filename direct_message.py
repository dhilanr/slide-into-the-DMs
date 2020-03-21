""" This is a simple Python script for accessing the Twitter API and sending
a series of direct messages with various options (quick-reply, media, etc.)

Additionally, this script includes a small sentiment analyzer for auto replies! """


import tweepy  # note changes to tweepy/api.py --- CANNOT use standard Tweepy library distribution
import twitter_credentials  # for OAuthHandler

# for data analytics and sentiment analysis:
# from textblob import TextBlob
# import regex as re

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt


######  AUTHENTICATION  ######
class AuthenticateTool():

    def authenticate_via_OAUTH(self):
        auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


######  API OBJECT  ###### 
class TwitterObjectAPI():
    def __init__(self):
        self.auth = AuthenticateTool().authenticate_via_OAUTH()  # calls AuthenticationTool
        self.api_object = tweepy.API(self.auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

    def get_api_object(self):
        return self.api_object


######  USER_ID FINDER  ######
class FoundUser():
    """
    FIND, PRINT, & RETURN DESIRED USER ID GIVEN SCREEN_NAME
    """
    def __init__(self, api_object):
        self.API = api_object

    def return_ID(self):
        self.twitter_handle = input("Enter Twitter Handle of User to Find: ")
        self.found_user = self.API.get_user(screen_name = self.twitter_handle)
        print("finding...")
        print("NAME: " + self.found_user.name)
        print("Screen Name: " + self.found_user.screen_name)
        print("ID: " + str(self.found_user.id) + "\n")
        return self.found_user.id


######  DIRECT MESSAGE TOOL  ###### 
class DirectMessenger():
    def __init__(self, api_object):
        self.API = api_object

    # Send plaintext message
    def send_plain_message(self):
        self.found_user = FoundUser(self.API)
        self.recipient_id = self.found_user.return_ID()
        self.message_text = input("Message body text: ")
        self.API.send_direct_message(recipient_id=self.recipient_id, text=self.message_text)


    # Send message with media
    def send_media(self):
        self.found_user = FoundUser(self.API)
        self.recipient_id = self.found_user.return_ID()
        self.media_filename = input("Media filename or path: ")
        self.media_upload = self.API.media_upload(self.media_filename)
        self.attachment_type = "media"
        self.media_id = self.media_upload.media_id
        self.message_text = input("Message body text: ")
        self.API.send_direct_message(recipient_id=self.recipient_id, text=self.message_text, attachment_type = self.attachment_type, attachment_media_id=self.media_id)

    # Send message with quick-reply options (with or without media)
    def send_quick_reply(self, quick_reply_options, media_boolean):
        self.quick_reply_type = "options"
        self.quick_reply_options = quick_reply_options
        self.found_user = FoundUser(self.API)
        self.recipient_id = self.found_user.return_ID()
        if (media_boolean):
            self.media_filename = input("Media filename or path: ")
            self.media_upload = self.API.media_upload(self.media_filename)
            self.attachment_type = "media"
            self.media_id = self.media_upload.media_id
        else:
            self.media_id = None
            self.attachment_type = None
        self.message_text = input("Message body text: ")
        self.API.send_direct_message(recipient_id=self.recipient_id, text=self.message_text, quick_reply_type = self.quick_reply_type, quick_reply_options = self.quick_reply_options, attachment_type = self.attachment_type, attachment_media_id=self.media_id)

    # Send message with calls-to-action (with or without media)
    def send_ctas(self, ctas, media_boolean):
        self.media_boolean = media_boolean
        self.ctas = ctas
        self.found_user = FoundUser(self.API)
        self.recipient_id = self.found_user.return_ID()
        if (media_boolean):
            self.media_filename = input("Media filename or path: ")
            self.media_upload = self.API.media_upload(self.media_filename)
            self.attachment_type = "media"
            self.media_id = self.media_upload.media_id
        else:
            self.media_id = None
            self.attachment_type = None
        self.message_text = input("Message body text: ")
        self.API.send_direct_message(recipient_id=self.recipient_id, text=self.message_text, ctas = self.ctas, attachment_type = self.attachment_type, attachment_media_id=self.media_id)



###################################
######  SEND DIRECT MESSAGE  ###### 
###################################

# initialize API Object
my_API_object = TwitterObjectAPI()
api = my_API_object.get_api_object()


# initialize options for DM
options = [
        {
            "label":"Uh huh",
            "description":"give me some phthalo green",
            "metadata":"external_id_1"
        },
        {
            "label":"NOPE, it's just Chuck Testa",
            "description":"i want some prussian blue",
            "metadata":"external_id_2"
        }
    ]


ctas = [
    {
        "type":"web_url",
        "label":"Eddie",
        "url":"http://www.read.seas.harvard.edu/~kohler/"
    },
    {
        "type":"web_url",
        "label":"Mike Smith",
        "url":"https://scholar.harvard.edu/mikesmith"
    },
    {
        "type":"web_url",
        "label":"Robin Gottlieb",
        "url":"https://www.youtube.com/watch?v=9A1Rx-p2Awg"
    }
]

ctas_politics = [
    {
        "type":"web_url",
        "label":"Bernie",
        "url":"https://berniesanders.com/"
    },
    {
        "type":"web_url",
        "label":"Biden",
        "url":"https://joebiden.com/"
    },
    {
        "type":"web_url",
        "label":"The Donald",
        "url":"https://www.donaldjtrump.com/"
    }
]

def GetChoice():
    print("Select from the following:")
    print("1. Plain Message\n2. Message with Media\n3. Message with Quick-Reply Options\n4. Message with Calls-to-Action")
    selected_choice = input("Input the # corresponding to the option you choose: ")
    while True:
        try:
            choice_number = int(selected_choice)
            if (1 <= choice_number and 4 >= choice_number):
                return selected_choice
            else:
                print("Pick a number from {1,2,3,4}: ")
                selected_choice = input()
        except:
            print("You have to enter an integer :(\nPick a number from {1,2,3,4}: ")
            selected_choice = input()
    return selected_choice

messenger = DirectMessenger(api)
print("Welcome to slide-into-the-DMs direct messenger (your one stop shop for all things DMs)!")
print("---------------------------------------------------------------------------------------")
selection = int(GetChoice())

if selection == 1:
    messenger.send_plain_message()
elif selection == 2:
    messenger.send_media()
else:
    media_condition = input("Would you like to send media, too? (y/n) ").lower()
    while (media_condition != "y" and media_condition != "n"):
        media_condition = input("Sorry, invalid input mister.  Let's try again: would you like to send media, too? (y/n) ").lower()

    if selection == 3:
        print("Your current Quick-Reply options (change in direct_message.py) are as follows")
        print(options)
        continue_bool = input("Would you like to continue? (y/n) ").lower()
        while (continue_bool == "y" and continue_bool == "n"):
            continue_bool = input("Invalid input.  Would you like to continue? (y/n) ").lower()
            print(continue_bool)
        if media_condition == "y" and continue_bool == "y":
            messenger.send_quick_reply(options, True)
        elif continue_bool == "y":
            messenger.send_quick_reply(options, False)
        else:
            print("Okay, see ya later alligator.")
    else:
        print("Your current Calls-to-Action (change in direct_message.py) are as follows")
        print(ctas)
        continue_bool = input("Would you like to continue? (y/n) ").lower()
        while (continue_bool != "y" and continue_bool != "n"):
            continue_bool = input("Invalid input.  Would you like to continue? (y/n) ").lower()
        if media_condition == "y" and continue_bool == "y":
            messenger.send_ctas(ctas_politics, True)
        elif continue_bool == "y":
            messenger.send_ctas(ctas_politics, False)
        else:
            print("Okay, see ya later alligator.")




