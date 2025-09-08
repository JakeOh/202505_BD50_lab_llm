import os
import pymupdf
from openai import OpenAI

from src.utils import get_openai_api_key


def pdf_to_text(pdf_file, header_height=80, footer_height=80):
    """pdf_file을 읽어서 헤더/푸터 제외한 영역에서 텍스트만 추출, TXT 형식으로 저장한 후 저장한 파일의 경로를 리턴."""

    # PyMuPDF 모듈을 사용해서 PDF 파일을 오픈.
    with pymupdf.open(pdf_file) as document:
        full_text = ''
        for page in document:  # 열린 PDF 파일에서 한 페이지씩 반복
            rect = page.rect
            clip = (0, header_height, rect.width, rect.height - footer_height)
            # 헤더/푸터를 제외한 영역에서 텍스트를 추출.
            full_text += page.get_text(clip=clip)
            full_text += '\n\n' + '-' * 50 + '\n\n'

    # 텍스트 파일로 저장(PDF 파일과 같은 이름으로, 확장자만 txt로 변경)
    base_name = os.path.basename(pdf_file)  # 경로를 제외한 파일 이름(sample.pdf)만 리턴.
    file_name = os.path.splitext(base_name)[0] # ['smaple', 'pdf'] 리스트에서 첫번째 원소.
    txt_file = f'./output/{file_name}.txt'
    with open(file=txt_file, mode='wt', encoding='utf-8')as f:
        f.write(full_text)

    return txt_file  # 저장된 TXT 파일의 경로(이름)을 리턴.


def summarize_text(txt_file):
    """txt_file을 읽어서 GPT API를 사용하기 위한 메시지 프롬프트를 작성, API 사용해서 문서 요약."""
    with open(file=txt_file, mode='rt', encoding='utf-8') as f:
        txt = f.read()

    system_prompt = f'''너는 문서를 요약하는 비서야.
    아래의 글을 읽고, 저자의 목적과 주장을 파악해서 주요 내용을 요약해줘.
    요약하는 포맷은 다음과 같아.
    # 제목
    ## 논문의 목적(5문장 내외)
    ## 저자의 주장(20문장 내외)
    ## 저장 소개
    
    ===== 아래 텍스트 ===
    
    {txt}
    '''

    client = OpenAI(api_key=get_openai_api_key())
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        temperature=0.1,
        messages=[
            {'role': 'system', 'content': system_prompt}
        ]
    )

    return response.choices[0].message.content


def summarize_pdf(pdf_file, output_file):
    """pdf_file의 내용을 요약해서 output_file에 저장."""
    # pdf_file 에서 텍스트를 추출하고, 저장한 텍스트 파일의 경로를 리턴받음.
    txt_file = pdf_to_text(pdf_file)
    print(txt_file, '저장됨!')

    # txt_file의 내용을 프롬프트로 작성 GPT 사용
    summary = summarize_text(txt_file)
    print(summary)

    # GPT 요약 내용을 파일에 저장
    with open(file=output_file, mode='wt', encoding='utf-8') as f:
        f.write(summary)


def main():
    pdf_file = './data/sample.pdf'
    pdf_summary_file = './output/sample_summary.txt'
    summarize_pdf(pdf_file, pdf_summary_file)
    print('PDF 요약 성공!')

if __name__ == '__main__':
    main()
