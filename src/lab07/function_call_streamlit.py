import streamlit as st
from openai import OpenAI

from src.lab07.gpt_functions import tools, get_current_time
from src.lab07.gpt_functions import get_yf_stock_info, get_yf_stock_history, get_yf_stock_recommendations
from src.utils import get_openai_api_key


def mylog(msg=''):
    print(msg)
    print('-' * 100)
    print()  # 줄바꿈


def get_gpt_response(client, messages):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        tools=tools,  # GPT가 호출할 수 있는 도구 목록
    )
    return response


def main():
    client = OpenAI(api_key=get_openai_api_key())

    st.title('My Chatbot')  # Streamlit 앱 페이지 상단의 타이틀.

    # st.session_state: Streamlit 앱이 실행되는 동안 유지되어야 할 값들을 dict 형태로 저장하기 위한 객체.
    # session_state에 'messages' 키가 없으면 시스템 초기 메시지를 설정.
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {'role': 'system', 'content': '너는 유능한 AI 비서야.'},  # dict
        ]

    # session_state에 저장된 messages(기존의 대화 내용들)를 화면에 출력.
    for msg in st.session_state.messages:
        # 시스템 메시지는 출력하지 않고, 사용자(user)와 비서(assistant) 메시지만 화면에 출력.
        if msg['role'] in ('user', 'assistant'):
            st.chat_message(msg['role']).write(msg['content'])

    user_input = st.chat_input('무엇을 도와드릴까요?')
    if user_input:  # 사용자가 입력한 내용이 있으면
        # 사용자의 입력 내용을 session_state.messages 리스트에 추가(append)
        st.session_state.messages.append({'role': 'user', 'content': user_input})

        # 사용자의 입력 내용을 화면에 출력
        st.chat_message('user').write(user_input)


if __name__ == '__main__':
    main()
