import os
from dotenv import load_dotenv


def get_openai_api_key():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    return api_key


if __name__ == "__main__":
    api_key = get_openai_api_key()
    print(api_key)
