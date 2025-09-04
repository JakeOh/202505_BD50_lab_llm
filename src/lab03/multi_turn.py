from openai import OpenAI

from src.utils import get_openai_api_key


def get_gpt_response(client, messages):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        temperature=0.9,
        messages=messages
    )
    return response.choices[0].message.content


def main():
    # 초기 메시지 템플릿
    messages = [
        { 'role': 'system', 'content': '너는 아주 뛰어난 비서야.' },
    ]

    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=get_openai_api_key())

    while True:
        # 콘솔에서 사용자 입력을 받음.
        user_input = input('사용자>>> ')
        if user_input == 'exit':
            break

        # 사용자 입력한 텍스트를 user 역할 메시지 content로 메시지 템플릿에 추가.
        messages.append({ 'role': 'user', 'content': user_input })
        # print(messages)

        # GPT 채팅 요청을 보내고, GPT가 생성한 답변을 받음.
        response = get_gpt_response(client, messages)

        # GPT가 생성한 답변을 출력
        print('MyGTP>>>', response)

        # GPT 생성한 답변을 다음 질문 이전의 프롬프트로 사용하기 위해서 messages에 추가.
        messages.append({ 'role': 'assistant', 'content': response })
        # print(messages)


if __name__ == '__main__':
    main()
