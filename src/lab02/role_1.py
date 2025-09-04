from openai import OpenAI

from src.utils import get_openai_api_key


def main():
    client = OpenAI(api_key=get_openai_api_key())
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        temperature=0.1,
        messages=[
            {
                'role': 'system',
                'content': '너는 백설공주 이야기의 마법거울이야. 마법 거울 캐릭터에 맞게 대답해줘.'
            },
            {
                'role': 'user',
                'content': '거울아, 거울아. 세상에서 누가 제일 예쁘니?'
            }
        ]
    )
    print(response.choices[0].message.content)


if __name__ == '__main__':
    main()
