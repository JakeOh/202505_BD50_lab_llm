from openai import OpenAI

from src.utils import get_openai_api_key


def file_to_txt(filename, mode='rt', encoding='utf-8'):
    """ 파일 filename을 읽어서 그 내용을 문자열로 리턴. """
    with open(filename, mode=mode, encoding=encoding) as f:
        txt = f.read()
    return txt


def get_gpt_response(message):
    client = OpenAI(api_key=get_openai_api_key())
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        temperature=0.1,
        messages=[{'role': 'system', 'content': message}]
    )
    return response.choices[0].message.content


def write_summary(filename, summary, mode='wt', encoding='utf-8'):
    """파일 filename에 summary를 텍스트 파이로 작성."""
    with open(filename, mode=mode, encoding=encoding) as f:
        f.write(summary)


def main():
    # 기사가 저장된 파일 이름과 경로
    article_file = './data/AI_article.txt'
    # GPT가 요약한 내용을 저장할 파일 이름과 경로
    article_summary_file = './output/AI_article_summary.txt'

    txt = file_to_txt(article_file)
    # print(txt)

    # GPT에게 요청할 요약 방법
    system_prompt = f'''너는 글을 요약하는 비서야.
    아래의 글을 일고 저자의 주장과 내용을 요약해.
    작성해야 하는 포맷은 다음과 같아.
    # 제목
    ## 부제목
    ## 저자의 주장(10문장 이내)
    ## 저자 소개
    
    ===== 이하 텍스트 ===
    
    {txt}
    '''

    summary = get_gpt_response(system_prompt)
    print(summary)

    # 요약 내용을 파일 저장
    write_summary(article_summary_file, summary)


if __name__ == '__main__':
    main()
