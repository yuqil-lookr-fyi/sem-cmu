# Setup

## Setup your public address to allow image to be uploaded to chatGPT api

```shell
python -m http.server 8007
/opt/homebrew/bin/ngrok http 8007
```

Then set NGROK_ADDRESS in .env by the public address from ngrok

## Setup your chatGPT

in .env set OPENAI_API_KEY as your chatGPT API token

# Run code

1. install Python 3.9.13
2. create an virtual environment
3. pip install -r requirements.txt
4. python -m main

open http://localhost:5005/
