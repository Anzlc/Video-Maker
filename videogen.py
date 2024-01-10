import praw
from redvid import Downloader
from moviepy.editor import *
from moviepy.video.fx.resize import resize
import datetime
import random
import glob


def gen_reddit_compilation(subreddit: str, search_posts: int, max_video_length: int, max_duration: int,
                           title_length: int):
    """

    :param subreddit: string
        A name of a subreddit without r/
    :param search_posts: int
        A maximum amount of top posts to be searched
    :param max_video_length: int
        A maximum Reddit video duration in seconds
    :param max_duration: int
        A maximum duration of the final video
    :param title_length: int
        Duration for how long should the title be displayed in seconds

    """

    reddit = praw.Reddit(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('SECRET'),
        user_agent=f"python:video-maker:v0.0.1 (by {os.getenv('REDDIT_USERNAME')})"
    )
    duration = 0
    videos = []

    subreddit = reddit.subreddit(subreddit)
    top_posts = subreddit.top(limit=search_posts, time_filter="day")

    filenames = []

    txt_clip = TextClip(f"Top r/{subreddit.display_name} posts on "
                        f"{datetime.datetime.now().day}/{datetime.datetime.now().month}/{datetime.datetime.now().year}",
                        fontsize=50, color='white', size=(1080, 1920))
    txt_clip = txt_clip.set_pos('center').set_duration(title_length)
    videos.append(txt_clip)
    duration += txt_clip.duration
    for i, post in enumerate(top_posts):
        try:
            down = Downloader(max_q=True)
            down.url = post.url

            down.path = f"videos/"
            down.check()
            down.filename = f"video {i}"

            if down.duration < max_video_length:
                if duration + down.duration + 1 <= max_duration:
                    down.download()
                    filenames.append((down.file_name.replace("\\", ""), down.duration))
                    duration += down.duration

            else:
                print(f"Skipping because video is longer then {max_video_length} seconds")
        except:
            print("Error occurred!")

    print(filenames)

    if len(filenames) > 0:
        for file in filenames:
            video = VideoFileClip(file[0])
            video = resize(video, width=1080)

            videos.append(video)

        final = concatenate_videoclips(videos, method="compose")

        final = resize(final, width=1080)

        final.write_videofile("final.mp4", fps=30)


def gen_motivational(name: str = "final"):
    """

    :param name: string
        Optional name for the file. Default 'final'.
    """

    # file paths for background videos and music
    motivational_videos = glob.glob("motivational/background/*.mp4")
    motivational_music = glob.glob("motivational/music/*.mp3")

    if len(motivational_videos) == 0 or len(motivational_music) == 0:
        raise Exception("No files found in background or music")

    print(motivational_videos)
    print(motivational_music)

    # file path for a file with motivational lines
    with open("motivational/lines.txt", "r") as f:
        line = random.choice(f.readlines())

    motivational_video = VideoFileClip(f"{random.choice(motivational_videos)}")
    motivational_music = AudioFileClip(f"{random.choice(motivational_music)}").subclip(t_start=2)
    motivational_line = TextClip(line,
                                 fontsize=45, method="caption", font="Work-Sans-Regular", color='white',
                                 size=(1000, None)).set_position("center").set_duration(motivational_video.duration)

    video = CompositeVideoClip([motivational_video, motivational_line])
    video.audio = motivational_music.set_duration(motivational_video.duration)
    video.write_videofile(f"motivational/{name}.mp4")
