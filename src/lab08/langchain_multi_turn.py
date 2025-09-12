import dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI


def main():
    # LangChain을 이용한 multi-turn 채팅(대화 내용을 기억하는 채팅)
    dotenv.load_dotenv()  # .env 파일의 key=value를 OS 환경 변수로 로딩
    model = ChatOpenAI(model='gpt-4o-mini')  # OpenAI GPT를 사용하기 위한 객체
    messages = [SystemMessage(content='너는 AI 비서야.')]  # 초기 메시지

    while True:
        user_input = input('사용자> ')
        if user_input.strip() == '':
            continue
        if user_input.strip() == 'exit':
            break

        # 사용자가 입력한 내용으로 HumanMessage를 생성하고 messages에 추가
        messages.append(HumanMessage(content=user_input.strip()))

        # AI 모델에게 질문을 보냄.
        ai_message = model.invoke(input=messages)

        # AIMessage를 messages 리스트에 추가
        messages.append(ai_message)

        # AI 답변을 출력
        print('AI>', ai_message.content)


if __name__ == '__main__':
    main()
