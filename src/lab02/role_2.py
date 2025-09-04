from openai import OpenAI

from src.utils import get_openai_api_key


def main():
    client = OpenAI(api_key=get_openai_api_key())
    response = client.chat.completions.create(
        model='gpt-4o',
        temperature=0.9,
        messages=[
            {
                'role': 'system',
                'content': '너는 배트맨 영화의 조커야. 조커 캐릭터에 맞게 대답해줘.'
            },
            {
                'role': 'user',
                'content': '세상에서 누가 제일 예쁘니?'
            }
        ]
    )
    print(response.choices[0].message.content)
    #> system 역할의 role_1.py과 다르게 content를 바꾸면 생성되는 답변도 다르게 생성됨.
    #> system role을 잘 설정할 수록 원하는 답변을 얻기가 쉬어짐.


# 현재 스크립트를 메인으로 실행할 때
if __name__ == '__main__':
    main()
