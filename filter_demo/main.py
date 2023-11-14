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
from util.openai_api import query_gpt, query_gpt_image

app = Flask(__name__)

# Path to your new_feed directory
NEW_FEED_PATH = "./new_feed"

# Generate the new feed
create_new_feed()


def read_text_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


@app.route("/")
def index():
    posts = []
    for filename in os.listdir(NEW_FEED_PATH):
        file_path = os.path.join(NEW_FEED_PATH, filename)
        if filename.endswith(".txt"):
            content = read_text_file(file_path)
            posts.append({"type": "text", "content": content})
        else:
            posts.append(
                {"type": "image", "src": url_for("new_feed", filename=filename)}
            )
    return render_template("index.html", posts=posts)


@app.route("/process_post", methods=["POST"])
def process_post():
    post_content = request.form.get("filename")

    # Check if the content is an image
    if os.path.splitext(post_content)[1].lower() in [".jpg", ".jpeg", ".png", ".webp"]:
        print("Image detected")
        # Assuming the content is an URL to an image
        gpt_response = query_gpt_image(post_content)
    else:
        print("Text detected")
        # Handle as text
        gpt_response = query_gpt(post_content)

    return jsonify({"result": gpt_response})


@app.route("/new_feed/<filename>")
def new_feed(filename):
    return send_from_directory(NEW_FEED_PATH, filename)


if __name__ == "__main__":
    app.run(debug=True, port=5005)
