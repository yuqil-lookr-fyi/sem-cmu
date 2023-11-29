import os
import shutil
import random
import requests
from mastodon import Mastodon
from dotenv import load_dotenv

load_dotenv()  # This loads the environment variables from .env file
client_key = os.getenv("MASTODON_CLIENT_KEY")
client_secret = os.getenv("MASTODON_CLIENT_SECRET_KEY")
access_token = os.getenv("MASTODON_ACCESS_TOKEN")


def fetch_random_post(client_key, client_secret, access_token):
    # Initialize Mastodon client
    mastodon = Mastodon(
        client_id=client_key,
        client_secret=client_secret,
        access_token=access_token,
        api_base_url="https://mastodon.social",  # Replace with your Mastodon instance URL
    )

    # Fetch public posts
    public_posts = mastodon.timeline_public(limit=2)

    # Select and return a random post
    if public_posts:
        return random.choice(public_posts)
    else:
        print("No posts found.")
        return None


def create_new_feed(download_images_only=False, num_posts=8):
    # Fetch specified number of random posts
    random_posts = []
    while len(random_posts) < num_posts:
        post = fetch_random_post(client_key, client_secret, access_token)
        if post:
            # Check if post has image media when download_images_only is True
            if download_images_only:
                if "media_attachments" in post and any(
                    media["type"] == "image" for media in post["media_attachments"]
                ):
                    random_posts.append(post)
            else:
                random_posts.append(post)

    # Create a directory for the new feed
    new_feed_path = "./new_feed"
    if os.path.exists(new_feed_path):
        shutil.rmtree(new_feed_path)
    os.makedirs(new_feed_path)

    # Save posts and images
    for i, post in enumerate(random_posts):
        # Save text content only if download_images_only is False
        text_filename = os.path.join(new_feed_path, f"post_{i}.txt")
        with open(text_filename, "w", encoding="utf-8") as file:
            file.write(post["content"])

        # Save images
        if "media_attachments" in post:
            for j, media in enumerate(post["media_attachments"]):
                if media["type"] == "image":
                    image_url = media["url"]
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image_filename = os.path.join(
                            new_feed_path, f"image_{i}_{j}.jpeg"
                        )
                        with open(image_filename, "wb") as img_file:
                            img_file.write(image_response.content)
