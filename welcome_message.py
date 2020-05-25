""" This is a simple Python script for accessing the Twitter API and sending
a series of direct messages with various options (quick-reply, media, etc.)

Additionally, this script includes a small sentiment analyzer for auto replies! """


import tweepy  # note changes to tweepy/api.py --- CANNOT use standard Tweepy library distribution
import twitter_credentials  # for OAuthHandler

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


######  WELCOME MESSAGE TOOL  ###### 
class WelcomeMessageSetup():
    def __init__(self, api_object):
        self.API = api_object

    # Send plaintext message
    def set_plain_message(self):
        self.name = input("Name this new message: ")
        self.message_text = input("Message body text: ")
        self.welcome_message= self.API.new_welcome_message(name=self.name, text=self.message_text)
        print(self.welcome_message)
        self.API.new_welcome_message_rule(self.welcome_message.id)

    # Send message with media
    def set_media_message(self):
        self.name = input("Name this new message: ")
        self.message_text = input("Message body text: ")
        self.media_filename = input("Media filename or path: ")
        self.media_category = input("Exactly input the media type from the following (dm_image, dm_gif, dm_video): ")
        kwargs = dict()
        kwargs["media_filename"] = self.media_filename
        kwargs["media_category"] = self.media_category
        kwargs["shared"] = "true"
        kwargs["shared_media"] = "true"
        self.media_upload = self.API.media_upload_async(**kwargs)
        self.attachment_type = "media"
        self.media_id = self.media_upload['media_id']
        self.welcome_message = self.API.new_welcome_message(name=self.name, text=self.message_text, attachment_type = self.attachment_type, attachment_media_id=self.media_id)
        print(self.welcome_message)
        self.API.new_welcome_message_rule(self.welcome_message.id)

    def remove_welcome_message(self):
        self.welcome_message = self.API.get_welcome_message_rule()
        print("Removing the following: \n", self.welcome_message)
        remove_condition = input("Would you like to continue? (y/n) ").lower()
        while (remove_condition != "y" and remove_condition != "n"):
            remove_condition = input("Sorry, invalid input.  Let's try again: would you like to continue? (y/n) ").lower()
        if (remove_condition == "y"):
            self.API.destroy_welcome_message_rule(self.welcome_message.id)
        else:
            print("Okay, bye now.")

        


###################################
######  SET WELCOME MESSAGE  ###### 
###################################        

# initialize API Object
my_API_object = TwitterObjectAPI()
api = my_API_object.get_api_object()

def GetChoice():
    print("Select from the following:")
    print("1. Print then DELETE current Welcome Message.\n2. Plain Welcome message\n3. Welcome message with Media\n4. Welcome message with Quick-Reply Options\n5. Welcome message with Calls-to-Action")
    selected_choice = input("Input the # corresponding to the option you choose: ")
    while True:
        try:
            choice_number = int(selected_choice)
            if (1 <= choice_number and 5 >= choice_number):
                return selected_choice
            else:
                print("Pick a number from {1,2,3,4,5}: ")
                selected_choice = input()
        except:
            print("You have to enter an integer :(\nPick a number from {1,2,3,4,5}: ")
            selected_choice = input()
    return selected_choice

messenger = WelcomeMessageSetup(api)
print("Welcome to slide-into-the-DMs welcome messenge setup manager!")
print("-------------------------------------------------------------")
selection = int(GetChoice())
if selection == 1:
    messenger.remove_welcome_message()
elif selection == 2:
    messenger.set_plain_message()
elif selection == 3:
    messenger.set_media_message()
else:
    print("This functionality is not complete.  Please edit welcome_message.py :)")




