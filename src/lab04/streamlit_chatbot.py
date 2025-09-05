import streamlit as st


def main():
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

        # assistant의 답변을 출력.
        st.chat_message('assistant').write(f'답변: {user_input}')

        # session_state에 저장하고 있던 messages 리스트에 비서의 답변을 추가
        st.session_state.messages.append({
            'role': 'assistant', 'content': f'답변: {user_input}'
        })


if __name__ == '__main__':
    main()
