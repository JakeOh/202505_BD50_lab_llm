import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

from src.lab08.langchain_tools import tools, tool_dict


def get_ai_response(model, messages):
    response = model.stream(input=messages)

    gathered = None
    for chunk in response:
        yield chunk

        # 파편화된(조각난) AI의 응답들을 하나로 합침.
        if gathered is None:
            gathered = chunk
        else:
            gathered += chunk

    print('gathered:', gathered)
    # AI 응답에 content가 없고 tool_calls가 포함된 경우.
    if gathered.tool_calls:
        # 채팅 이력(messages)에 도구 호출을 요청하는 AI 메시지를 추가.
        st.session_state.messages.append(gathered)

        # AI가 요청한 도구 목록들에서 함수를 순서대로 호출.
        for tool_call in gathered.tool_calls:
            fn = tool_dict.get(tool_call['name'])  # 함수 이름으로 함수 객체 찾음.
            tool_msg = fn.invoke(tool_call)  # 함수를 호출 -> Tool Message를 반환.
            st.session_state.messages.append(tool_msg)  # 도구 메시지를 대화 이력에 추가.

        # 도구 메시지가 포함된 메시지들을 AI에게 보냄 -> AI 함수 호출 결과를 바탕으로 답변을 생성해서 줌.
        for chunk in get_ai_response(model, st.session_state.messages):
            yield chunk


def main():
    # .env 파일의 api_key 정보를 환경 변수로 로딩.
    load_dotenv()

    # LLM 모델 클라이언트 객체 생성
    model = ChatOpenAI(model='gpt-4o-mini')

    # LLM 모델과 도구 목록(list)을 바인딩.
    model_with_tools = model.bind_tools(tools=tools)

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

        # GPT에게 질문을 함.
        response = get_ai_response(model_with_tools, st.session_state.messages)
        print('response:', response)

        # write_stream: generator 타입 객체를 반복하면서 타이핑하듯이 화면에 출력하고, 출력 완료된 문자열를 리턴.
        ai_answer = st.chat_message('assistant').write_stream(response)
        print('ai_answer:', ai_answer)

        # AI의 답변을 다음 질문의 맥락에서 사용하기 위해서 대화 내용을 저장.
        st.session_state.messages.append(AIMessage(content=ai_answer))


if __name__ == '__main__':
    main()
