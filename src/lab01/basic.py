from openai import OpenAI

from src.utils import get_openai_api_key

if __name__ == '__main__':
    # OpenAI 클라이언트 객체 생성(OpenAI에서 발급받은 API 키를 아규먼트로 전달)
    client = OpenAI(api_key=get_openai_api_key())

    # 클라이언트 객체를 사용해서 chat completions 요청을 보냄.
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        temperature=0.5,
        messages=[
            {
                'role': 'system',
                'content': '너는 나를 도와주는 비서야.'
            },
            {
                'role': 'user',
                'content': '나는 지금 누구랑 대화하고 있어?'
            }
        ]
    )
    print(response)
