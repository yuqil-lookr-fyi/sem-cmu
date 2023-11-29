import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # This loads the environment variables from .env file
api_key = os.getenv("OPENAI_API_KEY")  # Ensure this environment variable is set
public_ip_address = os.getenv(
    "NGROK_ADDRESS"
)  # Ensure this environment variable is set

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=api_key,
)


def query_gpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Indicate with 'Yes' or 'No' whether the text and any accompanying image (if present) are suitable for autistic patients who are native speakers of the text's language (e.g., Indian patients for Hindi text). Use the format: [Yes/No]: [Reason] [Translation]. \n Content: {prompt}",
                }
            ],
            max_tokens=150,
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def query_gpt_image_prompt(image_url, prompt=""):
    try:
        image_url = f"{public_ip_address}new_feed/{image_url}"
        print(image_url)
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",  # Ensure this is the correct model for your use case
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Indicate with 'Yes' or 'No' whether the text and any accompanying image (if present) are suitable for autistic patients who are native speakers of the text's language (e.g., Indian patients for Hindi text). Use the format: [Yes/No]: [Reason] [Translation]. \n Content: {prompt}",
                        },
                        {
                            "type": "image_url",
                            "image_url": image_url,
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
