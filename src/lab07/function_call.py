from openai import OpenAI

from src.utils import get_openai_api_key
from src.lab07.time_util import tools, get_current_time


def get_gpt_response(client, messages):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        tools=tools,
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

        tool_calls = response.choices[0].message.tool_calls
        if tool_calls:  # tool_calls가 있으면(if tool_calls != None)
            # GPT에서 우리가 제공한 도구 목록 중에서 함수의 호출을 요청한 경우
            tool_call_id = tool_calls[0].id  # 도구 호출 첫번째 목록의 아이디
            function_name = tool_calls[0].function.name  # 도구 호출 첫번째 목록의 함수 이름
            if function_name == 'get_current_time':
                # 도구 목록의 함수를 호출해서 그 실행 결과를 메시지 프롬프트에 추가.
                messages.append({
                    'role': 'function',
                    'tool_call_id': tool_call_id,
                    'name': function_name,
                    'content': get_current_time(),  # 함수 호출 -> 리턴 값을 'content'에 저장.
                })

                # 도구 호출 결과를 포함한 메시지 프롬프트를 사용해서 다시 GPT 요청을 보냄.
                response = get_gpt_response(client, messages)
                print(response)

        # 챗봇에서 이전 질문에 대한 답변들을 기억해서 문맥에 맞는 답변을 유도가 위해서
        messages.append({'role': 'assistant', 'content': response.choices[0].message.content})


if __name__ == '__main__':
    main()
