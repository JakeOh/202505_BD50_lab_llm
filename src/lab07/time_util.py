from datetime import datetime


def get_current_time():
    # 현재 시간 정보를 원하는 문자열 포맷으로 변환
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return now


def main():
    print(get_current_time())


if __name__ == '__main__':
    main()
