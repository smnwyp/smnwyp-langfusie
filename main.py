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