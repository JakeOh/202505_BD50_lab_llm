import json
from openai import OpenAI

from src.utils import get_openai_api_key
from src.lab07.gpt_functions import tools, get_current_time
from src.lab07.gpt_functions import get_yf_stock_info, get_yf_stock_history, get_yf_stock_recommendations


def get_gpt_response(client, messages):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        tools=tools,  # GPT가 필요로 할 때 호출할 수 있는 도구 목록
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
            # GPT가 여러 함수를 차례로 실행하려고 요청을 했을 때
            for tool_call in tool_calls:  # tool_calls 리스트의 아이템들을 순서대로 반복하면서
                tool_call_id = tool_call.id  # 도구 호출 목록의 아이디
                function_name = tool_call.function.name  # 도구 호출 목록의 함수 이름.
                # json.loads(str) -> dict: 역직렬화(de-serialization)
                arguments = json.loads(tool_call.function.arguments)  # 함수를 호출할 때 필요한 아규먼트들.
                # get_current_time 함수 호출을 요청한 경우
                if function_name == 'get_current_time':
                    function_result = get_current_time(arguments['timezone'])  # 함수 호출 결과를 저장
                elif function_name == 'get_yf_stock_info':
                    function_result = get_yf_stock_info(arguments['ticker'])
                elif function_name == 'get_yf_stock_history':
                    function_result = get_yf_stock_history(arguments['ticker'], arguments['period'])
                elif function_name == 'get_yf_stock_recommendations':
                    function_result = get_yf_stock_recommendations(arguments['ticker'])

                # 도구 목록의 함수를 호출해서 그 실행 결과를 메시지 프롬프트에 추가.
                messages.append({
                    'role': 'function',
                    'tool_call_id': tool_call_id,
                    'name': function_name,
                    'content': function_result,  # 함수 호출 -> 리턴 값을 'content'에 저장.
                })

            # 간혹 GPT가 불필요하게 도구 호출 요청을 반복하는 경우가 있음.
            # GPT의 이런 실수를 방지하기 위해서 system 프롬프트를 추가하는 트릭을 사용.
            messages.append({'role': 'system', 'content': '주어진 결과로 답변을 만들어줘.'})

            # 도구 호출 결과를 포함한 메시지 프롬프트를 사용해서 다시 GPT 요청을 보냄.
            # -> 함수 호출 결과(function 역할의 content)를 사용한 답변을 생성해서 보낼 줄 것으로 예상.
            response = get_gpt_response(client, messages)
            print(response)

        # 챗봇에서 이전 질문에 대한 답변들을 기억해서 문맥에 맞는 답변을 유도가 위해서
        messages.append({'role': 'assistant', 'content': response.choices[0].message.content})


if __name__ == '__main__':
    main()
