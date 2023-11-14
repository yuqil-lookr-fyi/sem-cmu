import os
import shutil
import random


def create_new_feed():
    base_path = "."  # Replace with the path to your repo
    safe_path = os.path.join(base_path, "autistic_safe")
    unsafe_path = os.path.join(base_path, "autistic_unsafe")
    new_feed_path = os.path.join(base_path, "new_feed")

    # Delete new_feed directory if it exists
    if os.path.exists(new_feed_path):
        shutil.rmtree(new_feed_path)

    # Create new_feed directory
    os.makedirs(new_feed_path)

    # Gather all posts with directory prefix to ensure uniqueness
    all_posts = [
        ("safe", p) for p in os.listdir(safe_path) if not p.endswith("_reason.txt")
    ] + [
        ("unsafe", p) for p in os.listdir(unsafe_path) if not p.endswith("_reason.txt")
    ]

    # Randomly pick 7 posts
    selected_posts = random.sample(all_posts, 7)

    # Copy and rename the selected posts
    for i, (dir_prefix, post) in enumerate(selected_posts):
        src_path = os.path.join(
            safe_path if dir_prefix == "safe" else unsafe_path, post
        )

        # Determine file extension
        _, ext = os.path.splitext(post)
        new_filename = f"post_{i}{ext}"
        dest_path = os.path.join(new_feed_path, new_filename)

        shutil.copyfile(src_path, dest_path)

    print("New feed created with 7 posts.")
