from openai import OpenAI

from src.utils import get_openai_api_key


def main():
    client = OpenAI(api_key=get_openai_api_key())
    response = client.chat.completions.create(
        model='gpt-4o',
        temperature=0.1,
        # no prompting: messages 안에 assistant의 content가 하나도 포함되지 않은 경우.
        messages=[
            {'role': 'system', 'content': '너는 유치원생이야. 유치원생처럼 대답해줘.'},
            {'role': 'user', 'content': '오리'}
        ]
    )
    print(response.choices[0].message.content)


if __name__ == '__main__':
    main()
