import os
from dotenv import load_dotenv


def get_openai_api_key():
    # .env 파일의 내용을 읽어서 OS 환경 변수(key-value)로 저장.
    load_dotenv()
    # OS 환경 변수로 저장된 값을 가져옴.
    api_key = os.getenv("OPENAI_API_KEY")
    return api_key


if __name__ == "__main__":
    api_key = get_openai_api_key()
    print(api_key)
