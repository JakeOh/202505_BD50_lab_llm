import base64
from glob import glob

from openai import OpenAI

from src.utils import get_openai_api_key


def base64encode_image(image_file):
    with open(file=image_file, mode='rb') as f:
        data = f.read()
        return base64.b64encode(data).decode(encoding='utf-8')


def make_image_quiz(client, image_file):
    quiz_prompt = '''제공한 이미지를 가지고 다음과 같은 형식으로 퀴즈를 만들어줘.
    정답은 (1) ~ (4) 중 하나만 해당하도록 만들어줘. 아래는 문제 예시야.
    ===== 예시 =====
    Q. 다음 이미지에 대한 설명으로 옳지 않은 것은?
    (1) 카페에서 빵을 사는 사람들이 있다.
    (2) 맨 앞의 사람은 빨간색 셔츠를 입고 있다.
    (3) 탁자에 앉아 있는 사람은 노트북을 사용하고 있다.
    (4) 점원은 커피를 만들고 있다.
    정답: (4). 점원은 주문을 받고 있다.
    (주의: 정답은 (1) ~ (4) 중 하나만 선택되도록 출제해줘.)
    '''
    base64_encoded = base64encode_image(image_file)
    messages = [
        {
            'role': 'user',
            'content': [
                {'type': 'text', 'text': quiz_prompt},
                {
                    'type': 'image_url',
                    'image_url': {'url': f'data:image/jpeg;base64,{base64_encoded}'}
                }
            ]
        }
    ]
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages
    )
    return response.choices[0].message.content


def main():
    # OpenAI 객체 생성
    client = OpenAI(api_key=get_openai_api_key())

    for g in glob('./images/*.jpg'):
        # 이미지 파일 하나씩 메시지 프롬프트를 만들어 GPT 요청을 보내고, 응답 내용(문제와 정답)을 출력.
        quiz = make_image_quiz(client, g)
        print(quiz)


if __name__ == '__main__':
    main()
