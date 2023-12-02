# admin_interface/app.py
import streamlit as st
import requests

API_BASE_URL = "http://localhost:5000/api"

def add_quiz():
    st.subheader("새 퀴즈 추가")
    question_text = st.text_area("문제 내용")
    correct_answer = st.selectbox("정답", ["A", "B", "C", "D"])
    if st.button("퀴즈 추가"):
        # API 호출하여 퀴즈 추가
        pass

def manage_quiz():
    st.subheader("퀴즈 관리")
    # API 호출하여 퀴즈 목록 조회
    # 퀴즈 수정 및 삭제 기능 구현
    pass

def view_responses():
    st.subheader("퀴즈 응답 조회")
    # API 호출하여 퀴즈 응답 조회
    pass

def manage_devices():
    st.subheader("장비 관리")
    # API 호출하여 장비 상태 조회 및 제어
    pass

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
