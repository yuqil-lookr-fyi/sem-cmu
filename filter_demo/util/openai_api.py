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
                    "content": f"Is this content safe for autistic patients? only answer yes or no with 1 sentence reason: {prompt}",
                }
            ],
            max_tokens=150,
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def query_gpt_image(image_url):
    try:
        image_url = f"{public_ip_address}{image_url}"
        print(image_url)
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",  # Ensure this is the correct model for your use case
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Is this content safe for autistic patients? only answer yes or no with 1 sentence reason",
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
