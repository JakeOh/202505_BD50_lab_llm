from datetime import datetime


def get_current_time():
    # 현재 시간 정보를 원하는 문자열 포맷으로 변환
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return now


# chat.completion 메시지를 요청할 때 함께 보내는 툴(도구) 리스트.
# GPT에서 필요할 때 호출할 수 있도록 선언한 도구 리스트
tools = [
    {
        'type': 'function',  # 도구 타입: 함수
        'function': {
            'name': 'get_current_time',  # 함수 이름
            'description': '현재 날짜와 시간을 문자열로 리턴.'  # 함수 설명
        }  # 함수 설명
    }
]


def main():
    print(get_current_time())


if __name__ == '__main__':
    main()
