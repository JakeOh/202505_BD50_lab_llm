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

    text = ''  # 이미지 퀴즈들을 저장할 문자열 변수.

    # ./images 폴더 안에 있는 모든 jpg 파일 이름을 하나씩 가져옴.
    for i, g in enumerate(glob('./images/*.jpg')):
        # i: 0, 1, 2, ...
        # g: ./images 폴더의 jpg 파일 이름. (예) ./images/cafe1.jpg
        # 이미지 파일 하나씩 메시지 프롬프트를 만들어 GPT 요청을 보내고, 응답 내용(문제와 정답)을 출력.
        try:
            quiz = make_image_quiz(client, g)
            print(quiz)
            seperator = f'\n## 문제 {i + 1}\n'  # 문제 번호는 1부터 시작.
            text += seperator
            text += f'![image]({g})\n'  # 이미지를 md 파일에 추가
            text += quiz + '\n'  # 퀴즈 문제와 정답을 추가
        except Exception as e:
            print(e)
            continue  # 다음 jpg 이미지를 가져옴.


    # md 파일에서는 '\n'이 줄바꿈으로 인식되지 않음. md 파일에서 줄바꿈을 사용하려면 '<br>' 태그를 사용해야 함.
    text = text.replace('\n', '<br>')  # text에서 '\n'을 '<br>'로 변경.
    # md 파일을 작성
    with open(file='./image_quiz.md', mode='wt', encoding='utf-8') as f:
        f.write(text)


if __name__ == '__main__':
    main()
