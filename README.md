# QuizSystemProject

## 프로젝트 개요
QuizSystemProject는 MQTT를 사용하는 WiFi 아두이노 장비를 통해 퀴즈를 진행하는 시스템입니다. 이 프로젝트는 Flask 기반의 중간 어플리케이션, Streamlit을 사용한 관리자 인터페이스, MQTT 클라이언트, 그리고 MariaDB 데이터베이스로 구성되어 있습니다.

## 기능
- 아두이노 장비에서 퀴즈 응답 수신
- 관리자 인터페이스를 통한 퀴즈 관리
- Flask 서버를 통한 중앙 데이터 처리
- MQTT를 통한 실시간 통신
- MariaDB를 사용한 데이터 저장 및 관리

## 설치 및 실행 방법

### 필요 조건
- Python 3.6 이상
- MariaDB 서버
- MQTT 브로커

### 설치
각 구성요소의 의존성을 설치하기 위해 다음 명령어를 실행하세요:

```bash
pip install -r admin_interface/requirements.txt
pip install -r flask_app/requirements.txt
pip install -r mqtt_client/requirements.txt
```

### 데이터베이스 설정
MariaDB에 init_db.sql과 schema.sql 스크립트를 사용하여 데이터베이스를 초기화하세요:

```bash
mysql -u username -p QuizSystemDB < database/init_db.sql
mysql -u username -p QuizSystemDB < database/schema.sql
```

### 실행
각 애플리케이션을 별도의 터미널에서 다음과 같이 실행하세요:

```bash
# Streamlit 관리자 인터페이스 실행
streamlit run admin_interface/app.py

# Flask 서버 실행
python flask_app/app.py

# MQTT 클라이언트 실행
python mqtt_client/client.py
```

### 프로젝트 구조
```graphql
QuizSystemProject/
│
├── admin_interface/          # Streamlit 관리자 인터페이스
│   ├── app.py                # Streamlit 애플리케이션 메인 파일
│   └── requirements.txt      # Streamlit 관련 의존성 목록
│
├── flask_app/                # Flask 중간 어플리케이션
│   ├── app.py                # Flask 애플리케이션 메인 파일
│   ├── requirements.txt      # Flask 관련 의존성 목록
│   ├── routes.py             # Flask 라우트 정의
│   └── db.py                 # 데이터베이스 연결 및 관리
│
├── mqtt_client/              # MQTT 클라이언트
│   ├── client.py             # MQTT 클라이언트 로직
│   └── requirements.txt      # MQTT 관련 의존성 목록
│
├── database/                 # 데이터베이스 스키마 및 초기화 스크립트
│   ├── init_db.sql           # 데이터베이스 초기화 SQL 스크립트
│   └── schema.sql            # 데이터베이스 스키마 정의
│
├── docs/                     # 프로젝트 문서
│   ├── setup.md              # 설치 및 설정 가이드
│   └── api_documentation.md  # API 문서화
│
├── tests/                    # 테스트 코드
│   └── test_flask_app.py     # Flask 애플리케이션 테스트
│
└── README.md                 # 프로젝트 설명 및 사용 방법
```
