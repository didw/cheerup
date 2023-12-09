# admin_interface/app.py
import sys
import os
import time
import streamlit as st
import requests

# 현재 스크립트의 디렉토리 경로를 구합니다.
current_dir = os.path.dirname(os.path.abspath(__file__))

# 프로젝트의 루트 디렉토리 경로를 구합니다.
project_root = os.path.dirname(current_dir)

# 프로젝트 루트 디렉토리를 sys.path에 추가합니다.
sys.path.append(project_root)

from mqtt_client.send_command import send_command_to_device

API_BASE_URL = "http://localhost:5000/api"

# admin_interface/app.py 내의 add_quiz 함수
def add_quiz():
    st.subheader("새 퀴즈 추가")
    question_text = st.text_area("문제 내용")
    
    answer_type = st.radio("답변 유형 선택", ('A-D', 'O-X'))

    if answer_type == 'A-D':
        correct_answer = st.selectbox("정답", ["A", "B", "C", "D"])
    else:
        correct_answer = st.selectbox("정답", ["O", "X"])

    if st.button("퀴즈 추가"):
        response = requests.post(f"{API_BASE_URL}/quiz", json={
            "question_text": question_text,
            "correct_answer": correct_answer
        })
        if response.status_code == 200:
            st.success("퀴즈가 추가되었습니다.")
        else:
            st.error("퀴즈 추가에 실패했습니다.")

# admin_interface/app.py 내의 manage_quiz 함수
def manage_quiz():
    st.subheader("퀴즈 관리")
    quizzes = get_quizzes()

    for i, quiz in enumerate(quizzes):
        print(quiz)
        with st.expander(f"ID: {quiz['id']} - 문제: {quiz['question_text']}"):
            updated_text = st.text_area(f"문제 수정 {i}", value=quiz['question_text'])
            if quiz['correct_answer'] in ["O", "X"]:
                updated_answer = st.selectbox(f"정답 수정 {i}", ["O", "X"], index=["O", "X"].index(quiz['correct_answer']), key=f"answer_{i}")
            else:
                updated_answer = st.selectbox(f"정답 수정 {i}", ["A", "B", "C", "D"], index=["A", "B", "C", "D"].index(quiz['correct_answer']), key=f"answer_{i}")
            if st.button(f"ID {quiz['id']} 수정", key=f"update_{i}"):
                response = requests.put(f"{API_BASE_URL}/quiz/{quiz['id']}", json={
                    "question_text": updated_text,
                    "correct_answer": updated_answer
                })
                if response.status_code == 200:
                    st.success("퀴즈가 수정되었습니다.")
                else:
                    st.error("퀴즈 수정에 실패했습니다.")
            if st.button(f"ID {quiz['id']} 삭제", key=f"delete_{i}"):
                response = requests.delete(f"{API_BASE_URL}/quiz/{quiz['id']}")
                if response.status_code == 200:
                    st.success("퀴즈가 삭제되었습니다.")
                else:
                    st.error("퀴즈 삭제에 실패했습니다.")

def start_quiz():
    st.subheader("퀴즈 시작")
    quiz_id = st.selectbox("퀴즈 선택", options=get_quiz_ids())
    quiz_duration = st.number_input("퀴즈 지속 시간 (초)", min_value=5, max_value=300, value=60)

    if st.button("퀴즈 시작"):
        # Flask API로 퀴즈 활성화 요청
        requests.post(f"{API_BASE_URL}/quiz/activate/{quiz_id}")

        # 카운트다운 시작
        with st.empty():
            for remaining in range(quiz_duration, 0, -1):
                st.write(f"{remaining}초 남음")
                time.sleep(1)
            st.write("응답 마감!")

        # 퀴즈 결과 요청 및 표시
        results = requests.get(f"{API_BASE_URL}/quiz/results/{quiz_id}").json()
        correct_count = results['correct_count']
        incorrect_count = results['incorrect_count']

        st.write("### 퀴즈 결과")
        st.write(f"정답 개수: {correct_count}")
        st.write(f"오답 개수: {incorrect_count}")

        # 결과 애니메이션 표시 (Streamlit은 직접적인 애니메이션 지원이 제한적임)
        # 대체 방안으로 Streamlit 컴포넌트 라이브러리 사용 가능


def view_responses():
    st.subheader("퀴즈 응답 조회")
    quiz_id = st.selectbox("퀴즈 선택", options=get_quiz_ids())
    if quiz_id:
        if st.button("결과 조회"):
            responses = requests.get(f"{API_BASE_URL}/quiz/responses/{quiz_id}").json()
            correct_responses = [resp for resp in responses if resp['is_correct']]
            correct_count = len(correct_responses)
            total_count = len(responses)

            st.write(f"정답률: {correct_count / total_count * 100:.2f}% ({correct_count}/{total_count})")
            for response in correct_responses:
                st.write(f"Device {response['device_id']} - 정답")

            if st.button("정답 디바이스에게 명령어 보내기"):
                for device_id in [resp['device_id'] for resp in correct_responses]:
                    send_command_to_device(device_id, "some_command")

# admin_interface/app.py 내의 get_quiz_ids 함수
def get_quiz_ids():
    response = requests.get(f"{API_BASE_URL}/quiz")
    if response.status_code == 200:
        quizzes = response.json()
        return [quiz[0] for quiz in quizzes]
    else:
        st.error("퀴즈 정보를 가져오는 데 실패했습니다.")
        return []

# admin_interface/app.py 내의 get_quizzes 함수
def get_quizzes():
    response = requests.get(f"{API_BASE_URL}/quiz")
    if response.status_code == 200:
        res = response.json()
        res = [{'id': quiz[0], 'question_text': quiz[1], 'correct_answer': quiz[2]} for quiz in res]
        return res
    else:
        st.error("퀴즈 정보를 가져오는 데 실패했습니다.")
        return []


# admin_interface/app.py 내의 manage_devices 함수
def manage_devices():
    st.subheader("장비 관리")
    devices = requests.get(f"{API_BASE_URL}/devices").json()

    if devices:
        for device in devices:
            st.write(f"Device ID: {device[0].strip()}, 상태: {device[1]}")
            if st.button(f"Device {device[0].strip()} 재설정"):
                # 장비 재설정을 위한 API 호출
                requests.post(f"{API_BASE_URL}/devices/reset/{device[0]}")
    else:
        st.write("등록된 장비가 없습니다.")


def main():
    st.title("퀴즈 시스템 관리자 대시보드")

    menu = ["홈", "퀴즈 시작", "퀴즈 관리", "퀴즈 응답 조회", "장비 관리"]
    choice = st.sidebar.selectbox("메뉴", menu)

    if choice == "홈":
        st.header("환영합니다!")
        st.write("""
        ### 퀴즈 시스템 관리자 대시보드 사용 방법

        - **퀴즈 관리**: 새로운 퀴즈를 추가하거나 기존 퀴즈를 수정 및 삭제할 수 있습니다.
            - '새 퀴즈 추가'를 클릭하여 새로운 퀴즈를 추가할 수 있습니다.
            - 각 퀴즈 옆의 '수정' 및 '삭제' 버튼을 사용하여 퀴즈를 관리할 수 있습니다.

        - **퀴즈 응답 조회**: 각 퀴즈에 대한 응답을 조회하고, 퀴즈의 정답률을 확인할 수 있습니다.
            - 드롭다운 메뉴에서 퀴즈를 선택한 후 '결과 조회' 버튼을 클릭합니다.
            - 정답을 맞춘 디바이스에 추가 명령어를 보낼 수 있습니다.

        - **장비 관리**: 연결된 모든 장비의 상태를 확인하고, 장비를 제어할 수 있습니다.
            - 각 장비의 상태를 확인할 수 있으며, '재설정' 버튼으로 장비를 초기화할 수 있습니다.
        """)
    elif choice == "퀴즈 시작":
        start_quiz()
    elif choice == "퀴즈 관리":
        add_quiz()
        manage_quiz()
    elif choice == "퀴즈 응답 조회":
        view_responses()
    elif choice == "장비 관리":
        manage_devices()

if __name__ == '__main__':
    main()
