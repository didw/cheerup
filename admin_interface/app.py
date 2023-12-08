# admin_interface/app.py
import streamlit as st
import requests

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

    for i, quiz in enumerate(quizzes, start=1):
        with st.expander(f"ID: {quiz['id']} - 문제: {quiz['question_text']}"):
            updated_text = st.text_area(f"문제 수정 {i}", value=quiz['question_text'])
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

# admin_interface/app.py 내의 view_responses 함수
def view_responses():
    st.subheader("퀴즈 응답 조회")
    quiz_id = st.selectbox("퀴즈 선택", options=get_quiz_ids())
    if quiz_id:
        if st.button("결과 조회"):
            # 선택한 퀴즈에 대한 응답 결과 요청
            responses = requests.get(f"{API_BASE_URL}/quiz/responses/{quiz_id}").json()
            correct_responses = [resp for resp in responses if resp['is_correct']]
            correct_count = len(correct_responses)
            total_count = len(responses)

            # 결과 표시
            st.write(f"정답률: {correct_count / total_count * 100:.2f}% ({correct_count}/{total_count})")
            for response in correct_responses:
                st.write(f"Device {response['device_id']} - 정답")

            # 정답 디바이스에게 명령어 보내기
            if st.button("정답 디바이스에게 명령어 보내기"):
                for device_id in [resp['device_id'] for resp in correct_responses]:
                    requests.post(f"{API_BASE_URL}/devices/command/{device_id}", json={"command": "some_command"})

# admin_interface/app.py 내의 get_quiz_ids 함수
def get_quiz_ids():
    response = requests.get(f"{API_BASE_URL}/quiz")
    if response.status_code == 200:
        quizzes = response.json()
        return [quiz['id'] for quiz in quizzes]
    else:
        st.error("퀴즈 정보를 가져오는 데 실패했습니다.")
        return []

# admin_interface/app.py 내의 get_quizzes 함수
def get_quizzes():
    response = requests.get(f"{API_BASE_URL}/quiz")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("퀴즈 정보를 가져오는 데 실패했습니다.")
        return []


# admin_interface/app.py 내의 manage_devices 함수
def manage_devices():
    st.subheader("장비 관리")
    devices = requests.get(f"{API_BASE_URL}/devices").json()

    if devices:
        for device in devices:
            st.write(f"Device ID: {device['id']}, 상태: {device['status']}")
            if st.button(f"Device {device['id']} 재설정"):
                # 장비 재설정을 위한 API 호출
                requests.post(f"{API_BASE_URL}/devices/reset/{device['id']}")
    else:
        st.write("등록된 장비가 없습니다.")


def main():
    st.title("퀴즈 시스템 관리자 대시보드")

    menu = ["홈", "퀴즈 관리", "퀴즈 응답 조회", "장비 관리"]
    choice = st.sidebar.selectbox("메뉴", menu)

    if choice == "홈":
        st.write("환영합니다!")
    elif choice == "퀴즈 관리":
        add_quiz()
        manage_quiz()
    elif choice == "퀴즈 응답 조회":
        view_responses()
    elif choice == "장비 관리":
        manage_devices()

if __name__ == '__main__':
    main()
