from flask import (
    Flask,
    render_template,
    send_from_directory,
    url_for,
    request,
    redirect,
    jsonify,
)

import os

# Import the function to create new feed
from util.create_new_feed import create_new_feed
from util.openai_api import query_gpt, query_gpt_image_prompt

app = Flask(__name__)

# Path to your new_feed directory
NEW_FEED_PATH = "./new_feed"

# Generate the new feed
# create_new_feed()


def read_text_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


@app.route("/")
def index():
    posts = []
    text_files = [f for f in os.listdir(NEW_FEED_PATH) if f.endswith(".txt")]

    for text_file in text_files:
        post_number = text_file.split("_")[1].split(".")[0]
        content = read_text_file(os.path.join(NEW_FEED_PATH, text_file))
        post = {"type": "text", "content": content, "images": []}

        # Find related images
        for filename in os.listdir(NEW_FEED_PATH):
            if filename.startswith(f"image_{post_number}_") and filename.endswith(
                ".jpeg"
            ):
                post["images"].append(url_for("new_feed", filename=filename))

        posts.append(post)
    return render_template("index.html", posts=posts)


@app.route("/process_post", methods=["POST"])
def process_post():
    text_content = request.form.get("text_content")
    image_filename = request.form.get("image_filename")
    if image_filename and image_filename.endswith((".jpg", ".jpeg", ".png", ".webp")):
        file_path = os.path.join(NEW_FEED_PATH, image_filename)
        if not os.path.exists(file_path):
            return jsonify({"result": "File not found"})
        print("Image detected")

        prompt = ""
        if text_content:
            prompt = text_content

        # Process as image with text prompt if available
        gpt_response = query_gpt_image_prompt(image_filename, prompt)
    else:
        print("Text detected")
        gpt_response = query_gpt(text_content)

    return jsonify({"result": gpt_response})


@app.route("/new_feed/<filename>")
def new_feed(filename):
    return send_from_directory(NEW_FEED_PATH, filename)


if __name__ == "__main__":
    app.run(debug=True, port=5005)
