import streamlit as st


def main():
    st.title('챗봇 테스트')

    messages = [
        {'role': 'user', 'content': '무엇을 도와드릴까요?'}
    ]

    for msg in messages:
        st.chat_message(msg['role']).write(msg['content'])

    user_input = st.chat_input('질문을 입력하세요...')
    if user_input:
        st.chat_message('user').write(user_input)
        messages.append({
            'role': 'user', 'content': user_input
        })

        st.chat_message('assistant').write(f'답변 - {user_input}')
        messages.append({
            'role': 'assistant', 'content': f'답변 - {user_input}'
        })


if __name__ == '__main__':
    main()
