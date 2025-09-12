import dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI


def main():
    # LangChain의 MessageHistory를 이용한 대화 내용 저장.
    dotenv.load_dotenv()

    store = {}  # 비어있는 dict 객체 생성.
    #> key(세션 아이디)-value(MessageHistory) 아이템을 저장하는 dict.
    #> MessageHistory에 대화 내용을 저장하는 것은 개발자가 아니라 LangChain에서 담당.

    # 지역 함수(local function)
    def get_session_history(session_id):
        """session_id를 키(key)로 해서 저장된 대화 기록(MessageHistory)를 반환.
        LangChain에서 대화 내용을 저장하기 위한 객체를 반환받기 위해서 사용할 함수."""
        if session_id not in store:  # session_id 키가 store 딕셔너리에 없으면
            store[session_id] = InMemoryChatMessageHistory()  # 대화 내용을 메모리에 저장하는 객체를 생성/저장

        return store[session_id]  # InMemoryChatMessageHistory 객체를 리턴.

    model = ChatOpenAI(model='gpt-4o-mini')  # LLM 선택.

    # LangChain의 MessageHistory 기능을 사용하기 위해서는 RunnableWithMessageHistory 객체를 생성해야 함.
    # RunnableWithMessageHistory(LLM 모델, MessageHistory를 리턴하는 콜백)
    runnable = RunnableWithMessageHistory(model, get_session_history)

    # 설정 딕셔너리 - 세션 아이디를 저장하고 있는 설정 객체
    config = {'configurable': {'session_id': 'abc_123'}}

    while True:
        user_input = input('User> ').strip()
        if user_input == '':
            continue
        if user_input == 'exit':
            break

        # AI가 생성한 답변을 한꺼번에 받아서 출력.
        # ai_message = runnable.invoke(input=user_input, config=config)
        # print('AI>', ai_message.content)

        # AI의 답변을 스트리밍 방식으로 출력.
        ai_stream = runnable.stream(input=user_input, config=config)
        for msg in ai_stream:
            print(msg.content, end='')
        print()



if __name__ == '__main__':
    main()
