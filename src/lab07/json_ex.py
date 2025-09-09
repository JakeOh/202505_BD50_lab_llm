import json
# json 모듈: 직렬화(serialize), 역직렬화(de-serialize)
# JSON: JavaScript Object Notation(자바스크립트 객체 표현)
# 속성(property) 이름과 속성의 값으로 객체를 표현. - 파이썬의 dict와 유사한 개념.
# 직렬화(serialization): 객체 --> JSON 형식의 문자열 변환.
# 역직렬화(de-serialization): JSON 형식의 문자열 --> 객체 변환.
# json.dumps(object): 객체를 직렬화한 JSON 형식의 문자열을 반환. (예) dict -> str
# json.loads(str): JSON 형식의 문자열을 객체로 만들어서 반환. (예) str -> dict

# 정수 3개를 갖는 dict 객체
score = {'korean': 90, 'english': 100, 'math': 80}
score_str = json.dumps(score)  # 직렬화: 객체 -> 문자열
print(score_str)

# JSON 형식의 문자열
student_str = '{"no": 1, "name": "오쌤", "score": 100}'
student = json.loads(student_str)  # 역직렬화: 문자열 -> 객체(dict)
print(type(student))
print(student['no'], student['name'], student['score'])