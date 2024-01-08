from dotenv import load_dotenv
from videogen import *


MAX_DURATION = 60
TITLE_LENGTH = 2
SEARCH_POSTS = 21
SUBREDDIT = "oddlysatisfying"
MAX_VIDEO_LENGTH = 50

"""
reddit.env:
    SECRET=<reddit app secret>
    CLIENT_ID=<reddit client id>
    REDDIT_USERNAME=<your reddit username>
"""

load_dotenv("reddit.env")


print("1: reddit-comp")
print("2: motivational")
print("3: motivational-batch")


video_type = input("Enter video type: ")


match video_type:
    case "1" | "reddit-comp":
        gen_reddit_compilation(SUBREDDIT, SEARCH_POSTS, MAX_VIDEO_LENGTH, MAX_DURATION, TITLE_LENGTH)
        print("Finished")
    case "2" | "motivational":
        gen_motivational()
        print("Finished")
    case "3" | "motivational-batch":
        for i in range(10):
            gen_motivational(name=f"final{i}")
        print("Finished")
    case _: print("Unknown command!")
