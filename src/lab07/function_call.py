from openai import OpenAI

from src.utils import get_openai_api_key


def get_gpt_response(client, messages):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
    )
    return response  # response.choices[0].message.content


def main():
    # OpenAI 객체 생성
    client = OpenAI(api_key=get_openai_api_key())

    # 초기 메시지 프롬프트
    messages = [{'role': 'system', 'content': '너는 사용자의 질문에 답하는 유능한 AI 비서야.'}]

    while True:  # 무한 루프
        user_input = input('사용자>>> ')
        if user_input.strip() == '':
            continue  # 루프를 다시 반복
        if user_input.strip() == 'exit':
            break  # 무한 루프를 종료

        messages.append({'role': 'user', 'content': user_input})
        response = get_gpt_response(client, messages)
        print(response)

        # 챗봇에서 이전 질문에 대한 답변들을 기억해서 문맥에 맞는 답변을 유도가 위해서
        messages.append({'role': 'assistant', 'content': response.choices[0].message.content})


if __name__ == '__main__':
    main()
