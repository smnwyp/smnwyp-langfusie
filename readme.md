# how to spring up local langfuse server

## 1. get langfuse docker

### 1.1 pull docker image
follow https://langfuse.com/docs/deployment/local#getting-started
```
git clone https://github.com/langfuse/langfuse.git
cd langfuse
```
note that, server is by default served at `http://localhost:3000` (see `docker-compose.yml`)

### 1.2 set up sso
go to your google cloud console, create a new project, create oauth2 credentials
and get the following values:
```
AUTH_GOOGLE_CLIENT_ID
AUTH_GOOGLE_CLIENT_SECRET
```

### 1.3 set up SSO env vars in langfuse `docker-compose.yml`
follow https://langfuse.com/docs/deployment/self-host#sso
basically add 4 following env var in `langfuse-server` section in `docker-compose.yml`:
```
environment:
      - ... # other env vars
      - AUTH_GOOGLE_CLIENT_ID=
      - AUTH_GOOGLE_CLIENT_SECRET=
      - AUTH_GOOGLE_ALLOW_ACCOUNT_LINKING=true
      - AUTH_GOOGLE_ALLOWED_DOMAINS=google.com
```

### 1.4 start langfuse server
```
# Start the server and database
docker compose up
```

## 2. start langfuse application

### 2.1 set up `.env`
create an `.env` file in the root of your project, and add the following env vars:
```
LANGFUSE_PUBLIC_KEY = ""
LANGFUSE_SECRET_KEY = ""
LANGFUSE_HOST = "http://localhost:3000"
OPENAI_API_KEY = ""
```
langfuse related keys could be found in the langfuse UI (http://localhost:3000)


### 2.2 run llm and visualize tracing info on langfuse dashboard

minimalistic snippet:
```commandline
import time
from dotenv import load_dotenv

from langfuse.decorators import observe
from langfuse.openai import openai  # OpenAI integration

load_dotenv()

@observe()
def story():
    return openai.chat.completions.create(
        model="gpt-4o",
        max_tokens=100,
        messages=[
            {"role": "system", "content": "You are a great storyteller."},
            {"role": "user", "content": "Once upon a time in a galaxy far, far away..."}
        ],
    ).choices[0].message.content


@observe()
def main():
    print(story())


@observe()
def wait():
    time.sleep(1)


@observe()
def capitalize(input: str):
    return input.upper()


@observe()
def main_fn(query: str):
    wait()
    capitalized = capitalize(query)
    return f"Q:{capitalized}; A: nice too meet you!"


if __name__ == "__main__":
    main_fn(query="hi there")
```
run the script, and then visit `http://localhost:3000` to see the monitoring and tracking board in action.

## more resources on langfuse usecase
https://langfuse.com/docs/sdk/python/example
