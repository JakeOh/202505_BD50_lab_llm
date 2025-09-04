from openai import OpenAI

from src.utils import get_openai_api_key


def main():
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=get_openai_api_key())

    # 무한 반복문
    while True:
        # 콘솔에서 사용자 입력을 받음.
        user_input = input('사용자>>> ')

        # 만약 사용자 입력이 'exit'이면 반복문을 종료.
        if user_input == 'exit':
            break

        # 사용자의 입력을 메시지 user 역할의 content로 작성, 요청을 보냄.
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            temperature=0.9,
            messages=[
                { 'role': 'system', 'content': '너는 유치원생이야. 유치원생처럼 대답해줘.' },
                { 'role': 'user', 'content': user_input },
            ],
        )

        # GPT 답변을 출력.
        print('MyGPT>>>', response.choices[0].message.content)


if __name__ == '__main__':
    main()
