from datetime import datetime

import pytz
import yfinance as yf
from langchain_core.tools import tool
from pydantic import BaseModel, Field


@tool
def get_current_time(timezone: str, location: str) -> str:
    """해당 timezone의 현재 시간을 문자열로 리턴.

    Args:
        timezone (str): 현재 시간 정보를 얻기 위한 타임 존. (예: Asia/Seoul)
        location (str): 현재 시간 정보를 찾기 위한 도시 이름. 타임 존의 도시명과 다를 수 있음.
    Returns:
        "%Y-%m-%d %H:%M:%S timezone(location)" 형식의 문자열.
    """
    try:
        tz = pytz.timezone(timezone)  # timezone 인스턴스 생성
        now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")  # 현재 시간(datetime 인스턴스) -> 문자열
        result = f'{now} {timezone}({location})'
    except pytz.UnknownTimeZoneError as e:
        result = f'알 수 없는 시간대: {timezone}'

    return result


# get_yf_stock_history 함수의 파라미터 타입으로 사용하기 위한 클래스.
class StockHistoryArgs(BaseModel):
    ticker: str = Field(..., title='주식 코드',
                        description='주식 데이터를 검색하기 위한 주식 코드(예: AAPL, AMZN)')
    period: str = Field(..., title='기간',
                        description='주식 데이터 조회 기간(예: 1d, 1mo, 1y)')


@tool
def get_yf_stock_history(input: StockHistoryArgs) -> str:
    """Yahoo Finance를 이용해서 period(기간)동안 ticker(주식 코드) 종목의 주식 데이터를 마크다운 형식으로 리턴."""
    ticker = yf.Ticker(input.ticker)  # Ticker 인스턴스 생성
    history = ticker.history(period=input.period)  # 주식 데이터프레임

    return history.to_markdown()  # pandas.DataFrame -> markdown 형식의 문자열


# @tool 함수들을 원소로 갖는 리스트 -> AI 모델과 바인딩.
tools = [
    get_yf_stock_history,
    get_current_time,
]

# AIMessage의 tool_calls에 포함된 함수 이름으로 함수 객체를 쉽게 찾기 위한 딕셔너리
# key - 함수 이름, value - 함수 객체.
tool_dict = {
    'get_yf_stock_history': get_yf_stock_history,
    'get_current_time': get_current_time,
}
