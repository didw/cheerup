# flask_app/app.py
from flask import Flask
from db import init_db_connection
from routes import configure_routes

app = Flask(__name__)

# 데이터베이스 연결 초기화
init_db_connection(app)

# 경로 설정
configure_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
