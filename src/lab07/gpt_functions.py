from datetime import datetime
import pytz
import yfinance as yf


def get_current_time(timezone='Asia/Seoul'):
    # 시간대(timezone) 문자열을 아규먼트로 주면 timezone 클래스 객체 타입을 생성 리턴.
    tz = pytz.timezone(timezone)
    # 현재 시간 정보를 원하는 문자열 포맷으로 변환
    now = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
    return f'{now} {timezone}'


def get_yf_stock_info(ticker):
    """ticker 문자열을 아규먼트로 받아서 Ticker 객체를 생성하고, 그 기업의 정보(info)를 문자열 형태로 리턴."""
    stock = yf.Ticker(ticker)  # ticker 문자열을 사용해서 Ticker 객체 생성.
    info = stock.info  #> dict
    return str(info)  # dict 객체를 문자열로 변환해서 리턴.


def get_yf_stock_history(ticker, period):
    """ticker 문자열과 주가 정보를 조회할 period 문자열을 아규먼트로 전달받아서
    해당 기간 동안의 매일 주가 정보를 Markdown 형식의 문자열로 리턴."""
    stock = yf.Ticker(ticker)  # Ticker 객체 생성
    history = stock.history(period=period)  # 현재 시점을 기준으로 지난 period 동안의 매일 주가 DataFrame.
    return history.to_markdown()  # DataFrame을 Markdown 형식의 문자열로 변환해서 리턴.


def get_yf_stock_recommendations(ticker):
    """ticker에 해당하는 기업의 지난 4개월간 애널리스트들의 추천(매수, 매도, 유지) 데이터를 리턴."""
    stock = yf.Ticker(ticker)  # Ticker 객체 생성
    return stock.recommendations.to_markdown()  # recommendations 데이터프레임을 Markdown 형식의 문자열로 변환해서 리턴.


# chat.completion 메시지를 요청할 때 함께 보내는 툴(도구) 리스트.
# GPT에서 필요할 때 호출할 수 있도록 선언한 도구 리스트
tools = [
    # get_current_time 정보
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

    # get_yf_stock_info 정보
    {},

    # get_yf_stock_history 정보
    {},

    # get_yf_stock_recommendations 정보
    {},
]



if __name__ == '__main__':
    # print(get_current_time())
    # print(get_current_time('Europe/London'))
    # print(get_current_time('America/New_York'))
    # print(get_current_time('America/Los_Angeles'))

    # stock_info = get_yf_stock_info('GOOGL')
    # print(stock_info)

    # stock_history = get_yf_stock_history('GOOGL', '3d')
    # print(stock_history)

    stock_recommendations = get_yf_stock_recommendations('GOOGL')
    print(stock_recommendations)
