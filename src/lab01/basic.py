from openai import OpenAI

from src.utils import get_openai_api_key

if __name__ == '__main__':
    # OpenAI 클라이언트 객체 생성(OpenAI에서 발급받은 API 키를 아규먼트로 전달)
    client = OpenAI(api_key=get_openai_api_key())

    # 클라이언트 객체를 사용해서 chat completions 요청을 보냄.
    response = client.chat.completions.create(
        model='gpt-4o-mini',  # OpenAI에서 제공하는 LLM 모델(gpt-4o, gpt-4o-mini, gpt-5, gpt-5-mini, ...)
        temperature=0.9,  # temperature: 온도가 높으면 창의적이지만 일관되지 않은 답변이 생성.
        # 온도가 낮으면 일관된(비슷한) 답변이 생성.

        # messages: 프롬프트(prompt). 역할(role)과 내용(content)을 가지고 있는 dict를 아이템으로 하는 리스트.
        # role(역할): system(ChatGPT), user(사용자), assistant(비서)
        messages=[
            {
                'role': 'system',
                'content': '너는 나를 도와주는 비서야.'
            },
            {
                'role': 'user',
                'content': '나는 지금 누구랑 대화하고 있어?'
            }
        ]
    )
    print(response)  #> ChatCompletion 객체
    print('-' * 10)
    print(response.choices[0])  # Choice 객체
    print('-' * 10)
    print(response.choices[0].message)  # ChatCompletionMessage 객체
    print('-' * 10)
    print(response.choices[0].message.content)  # GPT가 생성한 답변

