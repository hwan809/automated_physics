from hwpapi.core import App
from hwpapi.dataclasses import CharShape
from datetime import datetime

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
import base64

def create_hwp(teamname, teammates, title, image_loc):
    app = App()
    app.open("resource/base.hwpx")

    base_words = [
        ("(실험 제목)", title),
        ("(팀명)", teamname),
        ("(팀원 명단)", ', '.join(teammates))
    ]

    now = datetime.now()
    formatted_date = now.strftime("%Y년 %m월 %d일")
    days_of_week = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    weekday = now.weekday()
    base_words.append(("(실험 일시)", f"{formatted_date} {days_of_week[weekday]}"))

    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0.3,
        max_tokens=2056
    )

    with open(image_loc, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    message = HumanMessage(
        content=[
            {"type": "text", "text": "나는 {} 라는 주제로 탐구 보고서를 작성하고 있어. \
            각 항목을 키와 값의 쌍으로 구성된 딕셔너리 형태로 작성해 줘. python 코드로 작성하지 마.\
            항목은 실험 목표, 준비물, 이론적 배경, 실험 방법, 실험 결과, 결론, 논의, 참고 문헌 이야. 이미지를 참고하여 작성해. \
            우리의 목표는 보고서가 최대한 길게 작성되는 것이야. \
            실험 목표와 준비물을 제외한 각 항목을 최소 7문장 이상, 500글자 이상으로 길게 작성해. \
            번호를 매길 경우 줄바꿈을 한 번씩, 문단이 바뀔 때는 줄바꿈을 두 번씩 해. (줄바꿈: \\n) \
            한 항목에 문단이 적어도 2개 이상이여야 해. \
            준비물은 쉼표로 구분하여 작성하고, 리스트 형태로 표시하지 마. \
            실험 방법은 번호를 매겨 줄바꿈하거나, 불렛 포인트 작성법으로 작성해. \
            그 외에도 여러 가지 항목을 나열해야 하는 경우, (ex) 첫째, 둘째) 줄바꿈해. \
            딕셔너리 말고 다른 답변을 앞 뒤로 추가하지 마. ".format(title)},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
            },
        ],
    )
    response = model.invoke([message])

    dic = eval(response.content)
    print(dic)

    base_words.append(("(실험 목표)", dic['실험 목표']))
    base_words.append(("(준비물)", dic['준비물']))
    base_words.append(("(이론적 배경)", dic['이론적 배경']))
    base_words.append(("(실험 방법)", dic['실험 방법']))
    base_words.append(("(실험 결과)", dic['실험 결과']))
    base_words.append(("(결론)", dic['결론']))
    base_words.append(("(논의)", dic['논의']))
    base_words.append(("(참고 문헌)", dic['참고 문헌']))

    for old, new in base_words:
        app.replace_all(old, new, new_charshape=CharShape(text_color="#000000"))

    app.save('output/' + ', '.join(teammates) + '_' + title + '.hwpx')

    app.close()
    app.quit()