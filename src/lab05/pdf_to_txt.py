import pymupdf


def main():
    # 원본 PDF 파일 이름과 경로
    pdf_file = './data/sample.pdf'
    # PDF 파일에서 추출한 텍스트를 저장할 파일 이름과 경로
    txt_file = './output/sample.txt'

    with pymupdf.open(pdf_file) as document:
        # PDF 문서에서 한 페이지씩 텍스트를 추출
        full_text = ''
        for page in document:
            full_text += page.get_text()
            full_text += '\n\n' + '-' * 50 + '\n\n'
        print(full_text)

    with open(txt_file, mode='wt', encoding='utf-8') as f:
        f.write(full_text)


if __name__ == '__main__':
    main()
