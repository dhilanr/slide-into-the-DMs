""" This is a simple Python script for accessing the Twitter API and sending
a series of direct messages with various options (quick-reply, media, etc.)

Additionally, this script includes a small sentiment analyzer for auto replies!
Sends a quick-reply with media and asks if sentiment was captured correctly."""


import tweepy  # note changes to tweepy/api.py --- CANNOT use standard Tweepy library distribution
import twitter_credentials  # for OAuthHandler

# for data analytics and sentiment analysis:
from textblob import TextBlob


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

    # Send auto-reply message with quick-reply options (with two options for media)
    def send_auto_reply(self, recipient_id, text, quick_reply_options, media_filename):
        self.quick_reply_type = "options"
        self.quick_reply_options = quick_reply_options
        self.recipient_id = recipient_id
        self.media_filename = media_filename
        self.media_upload = self.API.media_upload(self.media_filename)
        self.attachment_type = "media"
        self.media_id = self.media_upload.media_id
        self.message_text = text
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

    # Return most recent direct message (sent or received)
    def get_dm(self, count):
        return self.API.list_direct_messages(count = count)


###################################
######  SEND DIRECT MESSAGE  ###### 
###################################


# initialize options for DM
mad_options = [
        {
            "label":"Yup, I'm NOT HAPPY!",
            "description":"You're in big trouble, Dhilan!",
            "metadata":"external_id_1"
        },
        {
            "label":"NOPE, I'm HAPPY!",
            "description":"but now i'm a little mad!!",
            "metadata":"external_id_2"
        }
    ]

happy_options = [
        {
            "label":"You're right, I AM HAPPY!",
            "description":"You're so perceptive, Dhilan :)",
            "metadata":"external_id_1"
        },
        {
            "label":"NOPE, I'm NOT HAPPY!",
            "description":"and now i'm even less pleased!!!",
            "metadata":"external_id_2"
        }
    ]


def GetCount():
    count = input("How many recent messages would you like to view? (input number 1-10) ")
    while True:
        try:
            count_value = int(count)
            if (1 <= count_value and 10 >= count_value):
                return count_value
            else:
                print("Pick a number from {1,2,3,...,10}: ")
                count = input()
        except:
            print("You have to enter an integer :(\nPick a number from {1,2,3,...,10}: ")
            count = input()
    return count_value


def SentimentReply(text, recipient_ID, messengerObject):
    sentiment_bool = False
    analysis = TextBlob(text)
    print(f"Sentiment analysis: {analysis.sentiment}\n")
    if analysis.sentiment[0]>0:
        print ('Positive sentiment :)\n')
        sentiment_bool = True
    else:
        print ('Negative\n')
    continue_bool = input("Would you like to auto-reply? (y/n) ").lower()
    while (continue_bool != "y" and continue_bool != "n"):
        continue_bool = input("Invalid input.  Would you like to auto-reply? (y/n) ").lower()
    if continue_bool == "y" and sentiment_bool == True:
        media_filename = "happy.png"
        message_text = "Hi, to better prepare Dhilan for your next interaction, I'll try to guess your feelings at this moment in time.  Looks like you're happy!"
        messengerObject.send_auto_reply(recipient_ID, message_text, happy_options, media_filename)
    elif continue_bool == "y" and sentiment_bool == False:
        media_filename = "angry.png"
        message_text = "Hi, to better prepare Dhilan for your next interaction, I'll try to guess your feelings at this moment in time.  Looks like you're not happy!"
        messengerObject.send_auto_reply(recipient_ID, message_text, mad_options, media_filename)
    else:
        print("Okay, no auto-reply :(\n")




###################################
##         IT BEGINS :)          ##
###################################
# initialize API Object
my_API_object = TwitterObjectAPI()
api = my_API_object.get_api_object()

messenger = DirectMessenger(api)
print("Welcome to slide-into-the-DMs direct messenger (your one stop shop for all things DMs)!")
print("---------------------------------------------------------------------------------------")
count = int(GetCount())
recent_messages = messenger.get_dm(count = count)
if (count == 1):
    if int(recent_messages.message_create['sender_id']) != twitter_credentials.PERSONAL_ID: # not Dhilan's Sender ID
        print("---------------------------------------------------------------------------------------")
        senderID = int(recent_messages.message_create['sender_id'])
        print(f"Sender is: {senderID} who is {messenger.API.get_user(senderID).screen_name}\n")
        current_text = recent_messages.message_create['message_data']['text']
        print(f"Text is: {current_text}\n")
        SentimentReply(current_text, senderID, messenger)
else:
    for i in range (len(recent_messages)):
        current_direct_message = recent_messages[i].message_create
        if int(current_direct_message['sender_id']) != twitter_credentials.PERSONAL_ID: # not Dhilan's Sender ID
            print("---------------------------------------------------------------------------------------")
            senderID = int(current_direct_message['sender_id'])
            print(f"Sender is: {senderID} who is {messenger.API.get_user(senderID).screen_name}")
            current_text = current_direct_message['message_data']['text']
            print(f"Text is: {current_text}\n")
            SentimentReply(current_text, senderID, messenger)

    print("All done :)\n\n")









### HELPER FUNCTION TO LIST PROPERTIES OF AN OBJECT ###
# temp = vars(messenger.API.list_direct_messages()[0])
# for item in temp:
#     print(item, ':', temp[item])