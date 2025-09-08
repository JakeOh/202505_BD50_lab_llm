from io import BytesIO

import requests
from PIL import Image
from openai import OpenAI

from src.utils import get_openai_api_key


def main():
    # OpenAI 객체 생성
    client = OpenAI(api_key=get_openai_api_key())

    # GPT 이미지 생성 요청을 보내고, 응답을 받음.
    response = client.images.generate(
        model='dall-e-3',  # 이미지 생성 인공지능 모델
        prompt='아이티윌 빅데이터 전문 강사 오쌤, 브래드 피트와 비슷하게.',  # 이미지를 생성하기 위한 프롬프트
        size='1024x1024',  # 생성할 이미지의 크기
        quality='standard',  # 생성할 이미지 화질
        n=1
    )
    # print(response)  #> ImagesResponse 객체
    url = response.data[0].url  # GPT 생성한 이미지 URL
    print(url)

    # 생성된 이미지 URL 주소로 GET 방식 요청(request)을 보내고 응답을 받음.
    url_resp = requests.get(url)
    print(url_resp)  #> requests.Response 객체, 응답 코드(200 - 성공).
    img_data = BytesIO(url_resp.content)  # 응답에 포함된 컨텐트를 Bytes 객체로 읽음.
    img = Image.open(img_data)  # 이미지 바이너리 데이터로, pillow 패키지의 Image 클래서 객체 생성.
    img.save('./output/generated_image.jpg', format='JPEG')
    img.show()  # 이미지 출력


if __name__ == '__main__':
    # 이미지를 생성하기 위한 프롬프트를 작성, GPT 사용해서 이미지 생성.
    main()
