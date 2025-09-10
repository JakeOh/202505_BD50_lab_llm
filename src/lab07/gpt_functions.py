from datetime import datetime
import pytz


def get_current_time(timezone='Asia/Seoul'):
    # 시간대(timezone) 문자열을 아규먼트로 주면 timezone 클래스 객체 타입을 생성 리턴.
    tz = pytz.timezone(timezone)
    # 현재 시간 정보를 원하는 문자열 포맷으로 변환
    now = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
    return f'{now} {timezone}'


# chat.completion 메시지를 요청할 때 함께 보내는 툴(도구) 리스트.
# GPT에서 필요할 때 호출할 수 있도록 선언한 도구 리스트
tools = [
    {
        'type': 'function',  # 도구 타입: 함수
        'function': {
            'name': 'get_current_time',  # 함수 이름
            'description': '해당 시간대의 현재 날짜와 시간을 문자열로 리턴.',  # 함수 설명
            'parameters': {
                'type': 'object',
                'properties': {
                    'timezone': {'type': 'string',
                                 'description': '현재 날짜와 시간을 반환하기 위한 시간대(예: Asia/Seoul)'},  # timezone 파라미터
                },  # 파라미터들의 dict
                'required': ['timezone'],  # parameters.properties 중에서 필수 파라미터의 목록.
            },  # 파라미터들에 대한 설명
        }  # 함수 설명
    },
]



if __name__ == '__main__':
    print(get_current_time())
    print(get_current_time('Europe/London'))
    print(get_current_time('America/New_York'))
    print(get_current_time('America/Los_Angeles'))
