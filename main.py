import praw
from selenium import webdriver
from gtts import gTTS
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips
import dotenv

# Reddit API credentials
dotenv.load_dotenv()

reddit = praw.Reddit(
    client_id=dotenv.get_key("CLIENT_ID"),
    client_secret=dotenv.get_key("CLIENT_SECRET"),
    user_agent=dotenv.get_key("USER_AGENT"),
)

# Access Reddit thread
submission = reddit.subreddit("AskReddit").hot(limit=25)
submission = next(submission)

# Extract title and comments
title = submission.title
comments = []

for top_level_comment in submission.comments:
    if isinstance(top_level_comment, praw.models.MoreComments):
        continue

    if top_level_comment.body in ["[removed]", "[deleted]"]:
        continue

    comments.append(top_level_comment.body)

# Take screenshots
driver = webdriver.Chrome()
driver.get(submission.url)
driver.save_screenshot("reddit_thread.png")
driver.quit()

# Generate TTS voiceover
text = title + ". " + " ".join(comments)
tts = gTTS(text=text, lang="en")
tts.save("voiceover.mp3")

# Combine screenshots and voiceover
clip = ImageSequenceClip(["reddit_thread.png"], fps=1)

# Load audio file
audio = AudioFileClip("voiceover.mp3")

# Make the audio file match the length of the video file
audio = audio.set_duration(clip.duration)

# Combine video and audio
final_clip = clip.set_audio(audio)

# Write the final video file
final_clip.write_videofile("tiktok_video.mp4", codec="libx264")
