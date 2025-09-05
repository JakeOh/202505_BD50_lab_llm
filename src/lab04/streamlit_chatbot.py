import streamlit as st
from openai import OpenAI

from src.utils import get_openai_api_key


def initialize_client():
    api_key = get_openai_api_key()
    if not api_key:  # 환경 변수에서 OpenAI API 키를 가져오지 못하면
        st.info('API 키가 없습니다.')
        st.stop()  # streamlit 앱을 종료

    # OpenAI 객체 생성
    client = OpenAI(api_key=api_key)

    return client


def get_gpt_response(client, messages):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        temperature=0.9,
        messages=messages,
    )

    return response.choices[0].message.content


def main():
    client = initialize_client()  # OpenAI 클라이언트 객체 생성

    st.title('첫번째 챗봇')

    # st.session_state: streamlit 앱이 실행 중에 유지되어야 할 값을 저장하는 객체.
    # 실행 중에 유지되어야 할 값들을 key-value 아이템으로 저장.
    if 'messages' not in st.session_state:
        # 'messages' 키가 session_state에 없으면,
        # messages를 키로 초기값 리스트를 session_state에 저장.
        st.session_state['messages'] = [
            {'role': 'assistant', 'content': '무엇을 도와드릴까요?'}
        ]

    # for msg in st.session_state['messages']:
    for msg in st.session_state.messages:
        st.chat_message(msg['role']).write(msg['content'])

    user_input = st.chat_input('입력하세요...')
    if user_input:  # chat_input에 입력한 내용이 있으면
        # 사용자가 입력한 내용을 'user' 아이콘과 함께 출력.
        st.chat_message('user').write(user_input)

        # session_state에 저장하고 있는 messages 리스트에 사용자 메시지를 추가
        st.session_state.messages.append({
            'role': 'user', 'content': user_input
        })

        answer = get_gpt_response(client, st.session_state.messages)

        # assistant의 답변을 출력.
        st.chat_message('assistant').write(answer)

        # session_state에 저장하고 있던 messages 리스트에 비서의 답변을 추가
        st.session_state.messages.append({
            'role': 'assistant', 'content': answer
        })


if __name__ == '__main__':
    main()
