import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI


def main():
    # .env 파일의 api_key 정보를 환경 변수로 로딩.
    load_dotenv()

    # LLM 모델 클라이언트 객체 생성
    model = ChatOpenAI(model='gpt-4o-mini')

    # Streamlit 앱 타이틀
    st.title('LangChain Streamlit Chatbot')

    # session_state에 messages 속성(property)이 없는 경우, 새로 생성함.
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # session_state에 저장된 메시지 이력을 전부 출력.
    for msg in st.session_state.messages:
        # 시스템 메시지를 제외한 AI 메시지와 사용자 메시지만 출력하자.
        if isinstance(msg, AIMessage):  # msg가 AIMessage 클래스의 인스턴스이면
            # 비서 아이콘과 함께 메시지를 출력
            st.chat_message('assistant').write(msg.content)
        elif isinstance(msg, HumanMessage):  # msg가 HumanMessage 인스턴스이면
            # 사용자 아이콘과 함께 메시지를 출력
            st.chat_message('user').write(msg.content)

    # 사용자 채팅 메시지 입력 상자
    prompt = st.chat_input('무엇을 도와드릴까요?')
    if prompt:  # 사용자 입력한 내용이 있으면
        # session_state의 messages 속성에 사용자가 입력한 텍스트를 HumanMessage 객체로 추가.
        st.session_state.messages.append(HumanMessage(content=prompt))

        # 사용자 아이콘과 함께 사용자의 채팅 입력을 화면에 출력.
        st.chat_message('user').write(prompt)



if __name__ == '__main__':
    main()
