import os
from dotenv import load_dotenv
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
from appwrite.input_file import InputFile
import uuid

# Initialize the Appwrite client
load_dotenv()  # This loads the environment variables from .env file
appwrite_url = os.getenv("VITE_APPWRITE_URL")
appwrite_project_id = os.getenv("VITE_APPWRITE_PROJECT_ID")
appwrite_post_collection_id = os.getenv("VITE_APPWRITE_POST_COLLECTION_ID")
appwrite_bucket_id = os.getenv("VITE_APPWRITE_BUCKET_ID")
appwrite_database_id = os.getenv("VITE_APPWRITE_DATABASE_ID")
# hardcoding creator for now
creator = os.getenv("APPWRITE_CREATOR_ID")

client = Client()
client.set_endpoint(appwrite_url)
client.set_project(appwrite_project_id)

# Initialize the Appwrite services
database = Databases(client)
storage = Storage(client)


def upload_image(file_path):
    # Create an InputFile object
    file = InputFile.from_path(file_path)
    file_id = str(uuid.uuid4())

    # Upload the image to Appwrite storage
    result = storage.create_file(
        bucket_id=appwrite_bucket_id,
        file_id=file_id,
        file=file,
    )
    image_id = result["$id"]
    image_url = f"{appwrite_url}/storage/buckets/{appwrite_bucket_id}/files/{image_id}/view?project={appwrite_project_id}"
    return image_url, image_id


def read_caption_from_file(file_path):
    with open(file_path, "r") as file:
        caption = file.read().strip()
    return caption


def create_post(image_url, image_id, caption):
    # Create a document in the posts collection
    data = {
        "imageUrl": image_url,
        "imageId": image_id,
        "caption": caption,
        "creator": creator,
    }
    document_id = str(uuid.uuid4())
    post = database.create_document(
        database_id=appwrite_database_id,
        collection_id=appwrite_post_collection_id,
        document_id=document_id,
        data=data,
    )
    return post
