# flask_app/routes.py
from flask import request, jsonify
from db import get_db

def configure_routes(app):
    
    @app.route('/')
    def index():
        return 'Welcome to the Quiz System!'

    @app.route('/api/quiz', methods=['POST'])
    def add_quiz():
        data = request.json
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO QuizQuestions (QuestionText, CorrectAnswer) VALUES (%s, %s)",
                        (data['question_text'], data['correct_answer']))
            db.commit()
            return {"message": "Quiz added successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @app.route('/api/quiz', methods=['GET', 'POST'])
    def manage_quiz():
        db = get_db()
        cursor = db.cursor()

        if request.method == 'POST':
            # 새로운 퀴즈 데이터를 저장하는 로직
            data = request.json
            try:
                cursor.execute("INSERT INTO QuizQuestions (QuestionText, CorrectAnswer) VALUES (%s, %s)",
                            (data['question_text'], data['correct_answer']))
                db.commit()
                return {"message": "Quiz added successfully"}, 200
            except Exception as e:
                return {"error": str(e)}, 500
        else:
            # 퀴즈 데이터를 반환하는 로직
            cursor.execute("SELECT * FROM QuizQuestions")
            quizzes = cursor.fetchall()
            return jsonify(quizzes)

    # flask_app/routes.py 내의 추가 엔드포인트
    @app.route('/api/quiz', methods=['GET'])
    def get_quizzes():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM QuizQuestions")
        quizzes = cursor.fetchall()
        return jsonify(quizzes)

    @app.route('/api/quiz/<int:quiz_id>', methods=['PUT'])
    def update_quiz(quiz_id):
        data = request.json
        db = get_db()
        cursor = db.cursor()
        print(quiz_id, data)
        cursor.execute("UPDATE QuizQuestions SET QuestionText = %s, CorrectAnswer = %s WHERE QuestionID = %s",
                    (data['question_text'], data['correct_answer'], quiz_id))
        db.commit()
        return {"message": "Quiz updated successfully"}, 200

    @app.route('/api/quiz/<int:quiz_id>', methods=['DELETE'])
    def delete_quiz(quiz_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM QuizQuestions WHERE id = %s", (quiz_id,))
        db.commit()
        return {"message": "Quiz deleted successfully"}, 200

    # flask_app/routes.py
    @app.route('/api/devices', methods=['GET'])
    def get_devices():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Devices")
        devices = cursor.fetchall()
        return jsonify(devices)

    # flask_app/routes.py
    @app.route('/api/devices/reset/<int:device_id>', methods=['POST'])
    def reset_device(device_id):
        db = get_db()
        cursor = db.cursor()
        try:
            # 장비 상태를 재설정하는 로직 (예: 상태를 '초기화'로 설정)
            cursor.execute("UPDATE Devices SET Status = '초기화' WHERE id = %s", (device_id,))
            db.commit()
            return {"message": f"Device {device_id} reset successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    # flask_app/routes.py
    @app.route('/api/quiz/responses/<int:quiz_id>', methods=['GET'])
    def get_quiz_responses(quiz_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT qr.DeviceID as device_id, (qq.CorrectAnswer = qr.SelectedAnswer) as is_correct
            FROM QuizResponses qr
            JOIN QuizQuestions qq ON qr.QuestionID = qq.id
            WHERE qr.QuestionID = %s
        """, (quiz_id,))
        responses = cursor.fetchall()
        return jsonify(responses)

    @app.route('/api/devices/command/<int:device_id>', methods=['POST'])
    def send_command_to_device(device_id):
        data = request.json
        command = data.get("command")
        # 장비에 명령어를 보내는 로직
        # 예: MQTT 또는 다른 프로토콜을 사용하여 장비에 명령어 전송
        return {"message": f"Command sent to device {device_id}"}, 200


    @app.route('/api/quiz/activate/<int:quiz_id>', methods=['POST'])
    def activate_quiz(quiz_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("UPDATE QuizQuestions SET IsActive = TRUE WHERE QuestionID = %s", (quiz_id,))
            db.commit()
            return {"message": "Quiz activated"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @app.route('/api/quiz/results/<int:quiz_id>', methods=['GET'])
    def get_quiz_results(quiz_id):
        db = get_db()
        cursor = db.cursor()
        try:
            # 정답 개수 계산
            cursor.execute("""
                SELECT COUNT(*) AS correct_count
                FROM QuizResponses
                JOIN QuizQuestions ON QuizResponses.QuestionID = QuizQuestions.QuestionID
                WHERE QuizResponses.QuestionID = %s AND QuizResponses.SelectedAnswer = QuizQuestions.CorrectAnswer
            """, (quiz_id,))
            correct_count = cursor.fetchone()['correct_count']

            # 오답 개수 계산
            cursor.execute("""
                SELECT COUNT(*) AS incorrect_count
                FROM QuizResponses
                JOIN QuizQuestions ON QuizResponses.QuestionID = QuizQuestions.QuestionID
                WHERE QuizResponses.QuestionID = %s AND QuizResponses.SelectedAnswer != QuizQuestions.CorrectAnswer
            """, (quiz_id,))
            incorrect_count = cursor.fetchone()['incorrect_count']

            return jsonify({"correct_count": correct_count, "incorrect_count": incorrect_count})
        except Exception as e:
            return {"error": str(e)}, 500
        